#!/bin/bash
# Helper script to run a complete experiment

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <config.yaml>"
    exit 1
fi

CONFIG_FILE=$1

echo "=================================="
echo "Starting Robot Control Experiment"
echo "=================================="
echo "Config: $CONFIG_FILE"
echo ""

# Source ROS 2
source /opt/ros/humble/setup.bash
source /workspace/ros2_ws/install/setup.bash

# Start robot simulation in background
echo "Starting robot simulation..."
ros2 run robot_simulation diff_drive_sim &
SIM_PID=$!
sleep 2

# Start Unity bridge in background
echo "Starting Unity bridge..."
ros2 run unity_bridge tcp_bridge &
BRIDGE_PID=$!
sleep 2

# Start experiment logger in background
echo "Starting experiment logger..."
python3 -c "
import rclpy
from python_controllers.experiment_logger import ROS2ExperimentLogger
import sys

rclpy.init()
node = rclpy.create_node('logger_node')
logger = ROS2ExperimentLogger(node, experiment_id='auto', output_dir='/workspace/logs')

try:
    rclpy.spin(node)
except KeyboardInterrupt:
    pass
finally:
    logger.close()
    node.destroy_node()
    rclpy.shutdown()
" &
LOGGER_PID=$!
sleep 2

# Run control node
echo "Starting control node..."
python3 /workspace/docs/control_node_example.py $CONFIG_FILE

# Cleanup
echo ""
echo "Stopping all processes..."
kill $SIM_PID $BRIDGE_PID $LOGGER_PID 2>/dev/null || true

echo "Experiment complete!"
