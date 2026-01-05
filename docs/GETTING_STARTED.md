# Getting Started Guide

This guide will help you set up and run your first robot control experiment.

## Installation

### Option 1: Using Docker (Recommended)

1. **Install Docker and Docker Compose**
   - Docker: https://docs.docker.com/get-docker/
   - Docker Compose: https://docs.docker.com/compose/install/

2. **Clone the Repository**
   ```bash
   git clone https://github.com/rr3khan/robot-control-experiments.git
   cd robot-control-experiments
   ```

3. **Build and Start the Container**
   ```bash
   docker-compose up -d
   docker-compose exec ros2 bash
   ```

4. **Build the ROS 2 Workspace**
   Inside the container:
   ```bash
   cd /workspace/ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ```

### Option 2: Local Installation

Requirements:
- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10+

1. Install ROS 2 Humble following the [official guide](https://docs.ros.org/en/humble/Installation.html)

2. Clone and build:
   ```bash
   git clone https://github.com/rr3khan/robot-control-experiments.git
   cd robot-control-experiments
   cd ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## First Experiment

### 1. Start the Robot Simulation

In terminal 1:
```bash
ros2 run robot_simulation diff_drive_sim
```

You should see:
```
[INFO] [diff_drive_sim]: Differential drive simulation started (rate: 50.0 Hz)
```

### 2. Run the Quick Demo

In terminal 2:
```bash
python3 scripts/quick_demo.py
```

This will make the robot move in a square pattern. You should see the robot state being published:
```bash
ros2 topic echo /robot_state
```

### 3. View Available Topics

```bash
ros2 topic list
```

You should see:
- `/robot_state` - Current robot position and velocity
- `/control_command` - Control commands sent to the robot
- `/experiment_log` - Experiment data for logging

## Running a PID Control Experiment

### 1. Start Required Nodes

**Terminal 1 - Robot Simulation:**
```bash
ros2 run robot_simulation diff_drive_sim
```

**Terminal 2 - Unity Bridge (optional):**
```bash
ros2 run unity_bridge tcp_bridge
```

**Terminal 3 - Control Node:**
```bash
python3 docs/control_node_example.py data/config_pid.yaml
```

**Terminal 4 - Logger:**
```bash
python3 -c "
import rclpy
from python_controllers.experiment_logger import ROS2ExperimentLogger

rclpy.init()
node = rclpy.create_node('logger_node')
logger = ROS2ExperimentLogger(node, experiment_id='my_first_experiment', output_dir='./logs')

try:
    rclpy.spin(node)
except KeyboardInterrupt:
    pass
finally:
    logger.close()
    node.destroy_node()
    rclpy.shutdown()
"
```

### 2. Analyze Results

After the experiment completes, analyze the data:

```bash
python3 analysis/analysis_utils.py logs/experiment_my_first_experiment.csv
```

This will:
- Print performance statistics
- Generate a comprehensive report with plots
- Save plots as PNG files

## Using the Launch File

For convenience, you can start both the simulation and bridge with one command:

```bash
ros2 launch robot_simulation experiment.launch.py
```

## Customizing Your Experiment

### Modify PID Parameters

Edit `data/config_pid.yaml`:

```yaml
controller:
  config:
    kp_linear: 1.5    # Increase for faster response
    kd_linear: 0.2    # Increase for less overshoot
    kp_angular: 3.0   # Increase for faster turning
```

### Change Target Waypoints

Edit the waypoints in `data/config_pid.yaml`:

```yaml
experiment:
  waypoints:
    - [2.0, 0.0, 0.0]      # x, y, theta (in radians)
    - [2.0, 2.0, 1.57]     # 1.57 rad = 90 degrees
    - [0.0, 2.0, 3.14]     # 3.14 rad = 180 degrees
```

## Unity Visualization (Optional)

To visualize the robot in 3D:

1. See [Unity Integration Guide](unity_integration/README.md)
2. Create a Unity project
3. Add the provided C# scripts
4. Connect to the ROS bridge (default port 10000)
5. Press Play in Unity

## Troubleshooting

### "No module named 'robot_control_interfaces'"

Make sure you've sourced the ROS 2 workspace:
```bash
source /workspace/ros2_ws/install/setup.bash
```

### "Failed to connect to ROS" (Unity)

1. Check that the Unity bridge is running:
   ```bash
   ros2 run unity_bridge tcp_bridge
   ```
2. Verify the IP address in Unity matches your host
3. Check firewall settings

### Docker container won't start

```bash
# Check Docker is running
docker ps

# Rebuild the container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Topics not appearing

```bash
# Check if nodes are running
ros2 node list

# Check topic list
ros2 topic list

# Echo a specific topic
ros2 topic echo /robot_state
```

## Next Steps

1. **Implement a Custom Controller**: See `python_controllers/base_controller.py`
2. **Add Sensor Simulation**: Extend the robot model with lidar/camera
3. **Multi-Robot Experiments**: Launch multiple robot instances
4. **Path Planning**: Integrate with Nav2 or custom planners
5. **Machine Learning**: Use logged data to train RL agents

## Need Help?

- Check the [main README](../README.md)
- Review example code in `docs/`
- Open an issue on GitHub
