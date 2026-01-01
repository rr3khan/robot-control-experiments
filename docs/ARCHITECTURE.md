# Architecture Overview

This document describes the architecture and design decisions of the robot control experimentation playground.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Unity (Optional)                     │
│                    Physics & Visualization                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ TCP/JSON
                            │ (Port 10000)
┌───────────────────────────▼─────────────────────────────────┐
│                      Unity Bridge Node                       │
│                   (ROS 2 TCP Bridge)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ ROS 2 Topics
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼───────┐  ┌───────▼────────┐
│ Robot          │  │  Control     │  │  Experiment    │
│ Simulation     │  │  Node        │  │  Logger        │
│ Node           │  │  (Python)    │  │  Node          │
└───────┬────────┘  └──────┬───────┘  └───────┬────────┘
        │                  │                   │
        │  /robot_state    │  /control_command │  /experiment_log
        └──────────────────┴───────────────────┴──────────┐
                                                           │
                                                    ┌──────▼──────┐
                                                    │   CSV       │
                                                    │   Logs      │
                                                    └──────┬──────┘
                                                           │
                                                    ┌──────▼──────┐
                                                    │  Analysis   │
                                                    │  Scripts    │
                                                    └─────────────┘
```

## Core Components

### 1. ROS 2 Packages

#### robot_control_interfaces
**Purpose**: Define custom ROS 2 message types

**Messages**:
- `RobotState.msg`: Complete robot state (pose, velocity, wheels)
- `ControlCommand.msg`: Control commands (linear/angular velocities)
- `ExperimentLog.msg`: Structured logging data

**Design Decision**: Separate interface package allows other packages to depend on messages without circular dependencies.

#### robot_simulation
**Purpose**: Simulate differential drive robot kinematics

**Key Class**: `DifferentialDriveRobot`
- Implements forward kinematics
- Updates pose based on wheel velocities
- Publishes state at configurable rate (default 50 Hz)

**Design Decision**: Pure kinematic simulation (no dynamics) keeps it simple and predictable. Can be extended with physics later.

#### unity_bridge
**Purpose**: Bridge between Unity and ROS 2

**Protocol**: TCP with JSON messages
- Stateless, simple to implement on Unity side
- No dependencies on Unity-specific packages
- Can be replaced with other protocols (WebSocket, etc.)

**Design Decision**: TCP instead of ROS-TCP-Endpoint for simplicity and fewer dependencies.

### 2. Python Controllers

#### Architecture Pattern: Strategy Pattern

```python
Controller (Abstract Base Class)
    ├── PIDController
    ├── PurePursuitController (future)
    ├── MPCController (future)
    └── ...

ControllerFactory (Factory Pattern)
    - create_controller(type, config)
    - register_controller(name, class)
```

**Benefits**:
- Easy to add new controllers
- Swappable at runtime
- Testable in isolation

#### PID Controller Design

Uses separate PID loops for:
1. **Linear velocity control**: Based on distance to target
2. **Angular velocity control**: Based on heading error

**Key Features**:
- Handles orientation when close to target position
- Normalizes angles to [-π, π]
- Configurable gains and limits

### 3. Experiment Logging

#### Design: Observer Pattern

```
ExperimentLog Topic (Subject)
    └── ROS2ExperimentLogger (Observer)
            └── CSV File (Sink)
```

**CSV Schema**:
```
timestamp, experiment_id, controller_type, x, y, theta, 
linear_velocity, angular_velocity, target_x, target_y, 
target_theta, control_linear, control_angular, 
position_error, orientation_error
```

**Design Decision**: CSV instead of ROS bag for:
- Simple analysis with pandas/Excel
- Human-readable
- Easy to export to other tools
- Can still be converted to bag if needed

### 4. Analysis Tools

#### Architecture: Functional + Object-Oriented

```python
ExperimentAnalyzer
    ├── plot_trajectory()
    ├── plot_errors()
    ├── plot_velocities()
    ├── compute_statistics()
    └── generate_full_report()

compare_experiments(files[])  # Functional
```

**Design Decision**: 
- OO for single experiment analysis (state management)
- Functional for comparisons (stateless)

## Communication Flow

### 1. Simulation Loop (50 Hz)
```
1. RobotSim updates kinematics
2. RobotSim publishes /robot_state
3. UnityBridge receives state
4. UnityBridge sends JSON to Unity
```

### 2. Control Loop (50 Hz)
```
1. ControlNode receives /robot_state
2. ControlNode computes control with Controller
3. ControlNode publishes /control_command
4. ControlNode publishes /experiment_log
5. RobotSim receives command
6. Logger receives log and writes CSV
```

### 3. Unity Loop (Variable)
```
1. Unity sends manual commands (optional)
2. UnityBridge publishes /control_command
3. Unity receives state from UnityBridge
4. Unity updates visualization
```

## Design Principles

### 1. Modularity
- Each component has single responsibility
- Components communicate via well-defined interfaces
- Easy to swap implementations

### 2. Extensibility
- Abstract base classes for key concepts (Controller)
- Factory pattern for object creation
- Configuration-driven behavior

### 3. Testability
- Pure functions where possible
- Dependency injection
- Small, focused classes

### 4. Documentation
- Docstrings for all public APIs
- Examples in docs/
- README files in each major directory

## Technology Choices

### ROS 2 (vs ROS 1)
**Pros**:
- Better real-time performance
- Built-in security
- Modern C++/Python
- Active development

### Docker
**Pros**:
- Consistent environment
- Easy to share
- No system pollution
- Version control

### Python for Controllers
**Pros**:
- Rapid prototyping
- Rich ecosystem (numpy, scipy)
- Easy to learn
- Integration with ML frameworks

**Cons**:
- Slower than C++
- GIL limitations

**Decision**: Performance adequate for control at 50 Hz. Can reimplement critical paths in C++ later.

### Unity (vs Gazebo)
**Pros**:
- Better graphics
- Easier to use
- More flexible
- Better for demos

**Cons**:
- Not open source
- Less robotics-specific
- Requires separate application

**Decision**: Gazebo is better for research, Unity for visualization and demos. Architecture supports both.

## Future Extensions

### Short Term
1. Add more controller types
2. Implement unit tests
3. Add launch files
4. Docker optimization

### Medium Term
1. Sensor simulation (lidar, camera)
2. Obstacle avoidance
3. Path planning integration
4. Multi-robot support

### Long Term
1. Machine learning integration
2. Hardware-in-the-loop
3. Cloud deployment
4. Web-based visualization

## Performance Considerations

### Update Rates
- **Simulation**: 50 Hz (adequate for differential drive)
- **Control**: 50 Hz (matches simulation)
- **Logging**: On-demand (every control cycle)
- **Unity**: Variable (30-60 FPS typical)

### Bottlenecks
1. **TCP Bridge**: Network latency
   - Solution: Use localhost or local network
   - Alternative: Consider shared memory

2. **Python GIL**: Single-threaded control
   - Current: Not an issue at 50 Hz
   - Future: Migrate hot paths to C++

3. **CSV Writing**: Disk I/O
   - Current: Buffered writes adequate
   - Future: Consider SQLite for larger datasets

## Security Considerations

### Docker
- Run as non-root user
- Limit network exposure
- Use secrets for any credentials

### ROS 2
- Use DDS security if deploying
- Isolate ROS network
- Validate all inputs

### Unity Bridge
- Validate JSON input
- Rate limiting
- Authentication for production

## Testing Strategy

### Unit Tests
- Controller logic
- Kinematics calculations
- Message parsing

### Integration Tests
- ROS node communication
- End-to-end workflows
- Docker build

### Manual Tests
- Unity visualization
- Real-time performance
- User workflows

## Deployment

### Development
```bash
docker-compose up
# Hot reload with --symlink-install
```

### Production (Future)
- Multi-stage Docker builds
- CI/CD pipeline
- Automated testing
- Performance monitoring
