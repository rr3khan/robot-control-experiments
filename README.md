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
- (Optional) Unity 2021.3 LTS or newer for 3D visualization

### 1. Clone the Repository

```bash
git clone https://github.com/rr3khan/robot-control-experiments.git
cd robot-control-experiments
```

### 2. Build and Start ROS 2 Container

```bash
docker-compose up -d
docker-compose exec ros2 bash
```

### 3. Build ROS 2 Workspace

Inside the container:

```bash
cd /workspace/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 4. Run Robot Simulation

Open three terminals in the container:

**Terminal 1 - Robot Simulation:**
```bash
ros2 run robot_simulation diff_drive_sim
```

**Terminal 2 - Control Node:**
```bash
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

### 5. (Optional) Connect Unity

See [Unity Integration Guide](unity_integration/README.md) for detailed setup.

```bash
# Run Unity bridge
ros2 run unity_bridge tcp_bridge
```

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
# Inside ROS 2 container
cd /workspace/ros2_ws
colcon test
colcon test-result --verbose
```

## 🐳 Docker Commands

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
