#!/bin/bash
# Helper script to build ROS 2 workspace

set -e

echo "=================================="
echo "Building ROS 2 Workspace"
echo "=================================="

cd /workspace/ros2_ws

echo "Running colcon build..."
colcon build --symlink-install

echo ""
echo "Build complete!"
echo "Run: source install/setup.bash"
echo ""
