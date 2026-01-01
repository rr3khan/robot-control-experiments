# Complete Example Workflow

This document provides a complete, end-to-end example of running a robot control experiment from start to finish.

## Scenario

We'll create an experiment where a differential drive robot follows a square path using PID control, log the results, and analyze the performance.

## Prerequisites

- Docker and Docker Compose installed
- Repository cloned locally

## Step-by-Step Walkthrough

### 1. Setup Environment

```bash
# Navigate to project directory
cd robot-control-experiments

# Start Docker container
docker-compose up -d

# Enter the container
docker-compose exec ros2 bash
```

You should now be inside the container at `/workspace`.

### 2. Build ROS 2 Workspace

```bash
# Use the provided build script
./scripts/build_ros.sh

# Source the workspace
source /workspace/ros2_ws/install/setup.bash
```

Expected output:
```
==================================
Building ROS 2 Workspace
==================================
Running colcon build...
Starting >>> robot_control_interfaces
Finished <<< robot_control_interfaces [5.2s]
Starting >>> robot_simulation
Starting >>> unity_bridge
Finished <<< robot_simulation [2.1s]
Finished <<< unity_bridge [2.2s]

Build complete!
```

### 3. Start Robot Simulation

Open a new terminal (Terminal 1):
```bash
docker-compose exec ros2 bash
source /workspace/ros2_ws/install/setup.bash
ros2 run robot_simulation diff_drive_sim
```

Expected output:
```
[INFO] [1234567890.123456789] [diff_drive_sim]: Differential drive simulation started (rate: 50.0 Hz)
```

### 4. (Optional) Start Unity Bridge

If you want to visualize in Unity, open another terminal (Terminal 2):
```bash
docker-compose exec ros2 bash
source /workspace/ros2_ws/install/setup.bash
ros2 run unity_bridge tcp_bridge
```

Expected output:
```
[INFO] [1234567890.123456789] [unity_tcp_bridge]: Unity TCP Bridge started on 0.0.0.0:10000
[INFO] [1234567890.123456789] [unity_tcp_bridge]: Waiting for Unity connection...
```

### 5. Verify Topics

Open another terminal (Terminal 3) to check that everything is working:
```bash
docker-compose exec ros2 bash
source /workspace/ros2_ws/install/setup.bash

# List all topics
ros2 topic list
```

You should see:
```
/control_command
/parameter_events
/robot_state
/rosout
```

Check the robot state:
```bash
ros2 topic echo /robot_state --once
```

Output:
```yaml
header:
  stamp:
    sec: 1234567890
    nanosec: 123456789
  frame_id: world
pose:
  x: 0.0
  y: 0.0
  theta: 0.0
velocity:
  linear:
    x: 0.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 0.0
left_wheel_velocity: 0.0
right_wheel_velocity: 0.0
battery_level: 100.0
```

### 6. Start Experiment Logger

In Terminal 3:
```bash
python3 -c "
import rclpy
from python_controllers.experiment_logger import ROS2ExperimentLogger
import sys

rclpy.init()
node = rclpy.create_node('logger_node')
logger = ROS2ExperimentLogger(
    node, 
    experiment_id='square_path_pid', 
    output_dir='/workspace/logs'
)

print('Logger started. Press Ctrl+C to stop.')

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

Expected output:
```
Experiment logger initialized: /workspace/logs/experiment_square_path_pid.csv
Logger started. Press Ctrl+C to stop.
```

### 7. Run Control Experiment

Open another terminal (Terminal 4):
```bash
docker-compose exec ros2 bash
source /workspace/ros2_ws/install/setup.bash

# Run the control node
python3 /workspace/docs/control_node_example.py /workspace/data/config_pid.yaml
```

Expected output:
```
[INFO] [1234567890.123456789] [control_node]: Control node started with PID controller
[INFO] [1234567890.123456789] [control_node]: Experiment ID: pid_test_001
[INFO] [1234567891.234567890] [control_node]: Reached waypoint 1, moving to next
[INFO] [1234567895.345678901] [control_node]: Reached waypoint 2, moving to next
[INFO] [1234567899.456789012] [control_node]: Reached waypoint 3, moving to next
[INFO] [1234567903.567890123] [control_node]: All waypoints reached!
```

### 8. Monitor Progress

While the experiment is running, in another terminal, you can monitor:

```bash
# Watch robot position update
ros2 topic echo /robot_state | grep -A 3 "pose:"

# Monitor control commands
ros2 topic echo /control_command | grep -A 2 "velocity"
```

### 9. Stop Experiment

After the robot completes the waypoints (or press Ctrl+C):
1. Stop the control node (Terminal 4) - Ctrl+C
2. Stop the logger (Terminal 3) - Ctrl+C
3. Stop Unity bridge if running (Terminal 2) - Ctrl+C
4. Stop simulation (Terminal 1) - Ctrl+C

### 10. Analyze Results

```bash
# Navigate to logs directory
cd /workspace/logs

# List experiment files
ls -lh

# You should see: experiment_square_path_pid.csv

# Run analysis
python3 /workspace/analysis/analysis_utils.py experiment_square_path_pid.csv
```

Expected output:
```
============================================================
EXPERIMENT STATISTICS
============================================================
Experiment ID: square_path_pid
Controller: PID
Duration: 15.32 s

Position Error:
  Mean: 0.0523 m
  Max:  0.2341 m
  Final: 0.0089 m

Orientation Error:
  Mean: 0.0891 rad (5.11°)
  Max:  0.3142 rad (18.01°)
  Final: 0.0123 rad (0.70°)
============================================================

Report saved to: /workspace/logs/experiment_square_path_pid_report.png
```

### 11. View Generated Plots

Exit the container and view the plots:
```bash
# Exit container
exit

# Plots are in the logs directory (mounted from host)
ls logs/

# Open the report image
# On Linux:
xdg-open logs/experiment_square_path_pid_report.png

# On macOS:
open logs/experiment_square_path_pid_report.png

# On Windows:
start logs/experiment_square_path_pid_report.png
```

### 12. Run Another Experiment with Different Parameters

Edit the configuration:
```bash
# Back in the container
docker-compose exec ros2 bash

# Edit PID gains
nano /workspace/data/config_pid.yaml
```

Change:
```yaml
controller:
  config:
    kp_linear: 2.0  # Increased from 1.0
    kp_angular: 3.0  # Increased from 2.0
```

Run the experiment again with a different ID:
```bash
# Update experiment ID in config
sed -i 's/pid_test_001/pid_test_002/' /workspace/data/config_pid.yaml

# Repeat steps 3-10
```

### 13. Compare Experiments

```bash
python3 -c "
from analysis import compare_experiments

compare_experiments([
    '/workspace/logs/experiment_square_path_pid.csv',
    '/workspace/logs/experiment_pid_test_002.csv'
], output_path='/workspace/logs/comparison.png')
"
```

### 14. Export Results

```bash
# Copy logs to a results directory
mkdir -p results
cp logs/*.csv results/
cp logs/*.png results/

# Create a summary
cat > results/SUMMARY.txt << EOF
Experiment Comparison Summary
=============================

Test 1: Default PID Parameters
- Kp_linear: 1.0
- Kp_angular: 2.0
- Mean position error: 0.052m

Test 2: Aggressive PID Parameters
- Kp_linear: 2.0
- Kp_angular: 3.0
- Mean position error: 0.034m

Conclusion: Higher gains resulted in 35% reduction in position error
EOF

# View summary
cat results/SUMMARY.txt
```

## Alternative: Using the Launch File

Instead of starting nodes individually, you can use the launch file:

```bash
# Terminal 1: Start simulation and bridge
ros2 launch robot_simulation experiment.launch.py

# Terminal 2: Start logger and control
# (manually start these as shown above)
```

## Alternative: Quick Demo

For a quick test without configuration:

```bash
# Start simulation
ros2 run robot_simulation diff_drive_sim &

# Wait 2 seconds
sleep 2

# Run quick demo
python3 /workspace/scripts/quick_demo.py
```

This will make the robot move in a square pattern with hardcoded commands.

## Troubleshooting

### No topics visible
```bash
# Check if nodes are running
ros2 node list

# Check ROS domain
echo $ROS_DOMAIN_ID
# Should be 42

# Restart simulation
ros2 run robot_simulation diff_drive_sim
```

### Python import errors
```bash
# Make sure workspace is sourced
source /workspace/ros2_ws/install/setup.bash

# Add python_controllers to path
export PYTHONPATH=/workspace:$PYTHONPATH
```

### Container issues
```bash
# Outside container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

Now that you've run a basic experiment:

1. **Modify PID gains** to see how they affect performance
2. **Add new waypoints** to test more complex paths
3. **Create a custom controller** (see `docs/ADDING_CONTROLLERS.md`)
4. **Integrate Unity** for 3D visualization
5. **Collect data** from multiple experiments for comparison
6. **Implement a new controller** (Pure Pursuit, MPC, etc.)

## Summary

You've successfully:
- ✅ Set up the Docker environment
- ✅ Built the ROS 2 workspace
- ✅ Run a robot simulation
- ✅ Executed a PID control experiment
- ✅ Logged experiment data to CSV
- ✅ Analyzed and visualized results
- ✅ Compared multiple experiments

This is the foundation for all robotics control experiments in this system!
