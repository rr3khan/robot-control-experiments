# Robot Control Experiments

A modular robotics control experimentation playground combining Unity for physics simulation, ROS 2 (Humble) for middleware, and Python for control algorithms. This project provides a clean, extensible architecture for testing and comparing different robot control strategies.

## 🎯 Features

- **Modular Architecture**: Clean separation between simulation, control, and analysis
- **Swappable Controllers**: Easy-to-extend controller interface (PID implemented)
- **Differential Drive Robot**: Kinematic model with configurable parameters
- **Unity Integration**: 3D visualization and physics simulation via TCP bridge
- **ROS 2 Middleware**: Robust communication using ROS 2 Humble
- **Experiment Logging**: CSV-based data logging for analysis
- **Analysis Tools**: Python scripts for plotting and performance comparison
- **Docker Support**: Containerized ROS 2 environment for reproducibility

## 📁 Project Structure

```
robot-control-experiments/
├── ros2_ws/                    # ROS 2 workspace
│   └── src/
│       ├── robot_control_interfaces/  # Custom ROS 2 messages
│       ├── robot_simulation/          # Differential drive simulation
│       └── unity_bridge/              # Unity ↔ ROS communication
├── python_controllers/         # Control algorithms
│   ├── base_controller.py     # Abstract controller interface
│   ├── pid_controller.py      # PID controller implementation
│   ├── controller_factory.py  # Factory for creating controllers
│   └── experiment_logger.py   # CSV logging utilities
├── unity_integration/          # Unity integration resources
│   ├── unity_scripts/         # C# scripts for Unity
│   └── README.md              # Unity setup guide
├── analysis/                   # Data analysis scripts
│   ├── analysis_utils.py      # Analysis and plotting tools
│   └── plot_trajectory.py     # Quick trajectory plotting
├── data/                       # Configuration files
│   └── config_pid.yaml        # Example PID configuration
├── docs/                       # Documentation and examples
│   └── control_node_example.py # Example control node
├── logs/                       # Experiment logs (CSV)
├── Dockerfile                  # ROS 2 Docker image
├── docker-compose.yml          # Docker orchestration
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- [Task](https://taskfile.dev/) (optional but recommended for simplified workflow)
- (Optional) Unity 2021.3 LTS or newer for 3D visualization

### 1. Clone the Repository

```bash
git clone https://github.com/rr3khan/robot-control-experiments.git
cd robot-control-experiments
```

### 2. Quick Setup (Using Taskfile - Recommended)

The easiest way to get started is using the Taskfile:

```bash
# Install Task if you haven't already
# Windows (using Chocolatey): choco install go-task
# macOS (using Homebrew): brew install go-task/tap/go-task
# Linux: See https://taskfile.dev/installation/

# One command to start everything and open a configured shell
task dev
```

This single command will:
- Start Docker containers
- Build the ROS 2 workspace
- Open a bash shell with the ROS environment already sourced

### 2. Manual Setup (Alternative)

If you prefer not to use Taskfile:

```bash
# Start containers and build workspace
docker-compose up -d
docker-compose exec ros2 bash -c "cd /workspace/ros2_ws && colcon build --symlink-install && source install/setup.bash"

# Open a shell
docker-compose exec ros2 bash
cd /workspace/ros2_ws
source install/setup.bash
```

### 3. Run Robot Simulation

Open three terminals (using `task shell` in each, or `docker-compose exec ros2 bash`):

**Terminal 1 - Robot Simulation:**
```bash
# Inside container (helper function):
ros_run_sim

# Or from host:
task run-sim

# Or manually:
ros2 run robot_simulation diff_drive_sim
```

**Terminal 2 - Control Node:**
```bash
# Inside container (helper function):
ros_run_control

# Or from host:
task run-control

# Or manually:
python3 /workspace/docs/control_node_example.py /workspace/data/config_pid.yaml
```

**Terminal 3 - Experiment Logger:**
```bash
# In Python console
from python_controllers.experiment_logger import ROS2ExperimentLogger
import rclpy
rclpy.init()
node = rclpy.create_node('logger_node')
logger = ROS2ExperimentLogger(node, experiment_id='test_001', output_dir='/workspace/logs')
rclpy.spin(node)
```

### 4. (Optional) Connect Unity

See [Unity Integration Guide](unity_integration/README.md) for detailed setup.

```bash
# Inside container (helper function):
ros_run_unity_bridge

# Or from host:
task run-unity-bridge

# Or manually:
ros2 run unity_bridge tcp_bridge
```

## 🛠️ Helper Commands Inside Container

When you're inside the Docker container, you have access to convenient helper functions (automatically loaded):

```bash
ros_build          # Build ROS workspace
ros_source         # Source ROS workspace environment
ros_setup          # Build and source workspace (all-in-one)
ros_run_sim        # Run robot simulation
ros_run_control    # Run control node
ros_run_unity_bridge # Run Unity bridge
ros_test           # Run ROS tests
ros_clean         # Clean build artifacts
```

These functions automatically handle sourcing the ROS environment, so you don't need to manually `cd` and `source` every time!

## 🎮 Control Algorithms

### Implemented Controllers

#### PID Controller
- Position and orientation control for differential drive robots
- Configurable gains (Kp, Ki, Kd) for linear and angular control
- Velocity limits and tolerances

### Adding Custom Controllers

1. Create a new controller class inheriting from `Controller`:

```python
from python_controllers.base_controller import Controller

class MyController(Controller):
    def compute_control(self, state, target):
        # Your control logic here
        return linear_vel, angular_vel
    
    def reset(self):
        # Reset internal state
        pass
    
    def get_name(self):
        return "MyController"
```

2. Register it with the factory:

```python
from python_controllers.controller_factory import ControllerFactory
ControllerFactory.register_controller('MyController', MyController)
```

## 📊 Data Analysis

### Analyze Experiment Results

```bash
# Generate full analysis report
python3 analysis/analysis_utils.py logs/experiment_20240101_120000.csv

# Quick trajectory plot
python3 analysis/plot_trajectory.py logs/experiment_20240101_120000.csv
```

### Compare Multiple Experiments

```python
from analysis import compare_experiments

compare_experiments([
    'logs/experiment_pid.csv',
    'logs/experiment_custom.csv'
], output_path='comparison.png')
```

## 🔧 Configuration

Edit `data/config_pid.yaml` to customize:

- Controller gains (Kp, Ki, Kd)
- Robot parameters (wheel radius, base width)
- Velocity limits
- Target waypoints
- Update rate

Example:

```yaml
controller:
  type: "PID"
  config:
    kp_linear: 1.0
    ki_linear: 0.0
    kd_linear: 0.1

robot:
  wheel_radius: 0.05  # 5 cm
  wheel_base: 0.3     # 30 cm

experiment:
  waypoints:
    - [1.0, 0.0, 0.0]
    - [1.0, 1.0, 1.57]
```

## 📝 ROS 2 Topics

| Topic | Message Type | Description |
|-------|-------------|-------------|
| `/robot_state` | `RobotState` | Current robot state (pose, velocity) |
| `/control_command` | `ControlCommand` | Control commands (velocities) |
| `/experiment_log` | `ExperimentLog` | Experiment data for logging |

## 🧪 Running Tests

```bash
# Using Taskfile (recommended)
task test

# Or manually inside ROS 2 container
cd /workspace/ros2_ws
source install/setup.bash
colcon test
colcon test-result --verbose
```

## 🐳 Docker Commands

### Using Taskfile (Recommended)

```bash
# Complete setup and open shell
task dev

# Start containers and build workspace
task up

# Open shell with ROS environment sourced
task shell

# Run simulation
task run-sim

# Run control node
task run-control

# View logs
task logs

# Stop containers
task down

# Rebuild containers
task rebuild

# Clean build artifacts
task clean

# Run tests
task test

# See all available tasks
task --list
```

**Note:** When inside the container, use the `ros_*` helper functions (e.g., `ros_run_sim`) instead of `task` commands. Task commands are for use from the host machine.

### Manual Docker Commands

```bash
# Start services
docker-compose up -d

# Access container
docker-compose exec ros2 bash

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose build
```

## 🤝 Contributing

Contributions are welcome! Areas for expansion:

- Additional controllers (MPC, Pure Pursuit, Stanley, etc.)
- Sensor simulation (lidar, camera, IMU)
- Multi-robot coordination
- Path planning algorithms
- Advanced analysis tools

## 📚 Documentation

- [Unity Integration Guide](unity_integration/README.md)
- [Controller Development Guide](docs/CONTROLLERS.md) (coming soon)
- [ROS 2 Messages Reference](docs/MESSAGES.md) (coming soon)

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- ROS 2 Humble
- Unity Technologies
- Open source robotics community

## 📧 Contact

For questions or suggestions, please open an issue on GitHub. 
