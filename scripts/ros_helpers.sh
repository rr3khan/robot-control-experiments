#!/bin/bash
# ROS 2 Helper Functions
# Source this file inside the Docker container for convenient commands
# Usage: source /workspace/scripts/ros_helpers.sh

ROS_WS="/workspace/ros2_ws"

# Function to source ROS workspace
ros_source() {
    if [ -f "$ROS_WS/install/setup.bash" ]; then
        source "$ROS_WS/install/setup.bash"
        echo "✓ ROS workspace environment sourced"
    else
        echo "✗ Error: ROS workspace not built. Run 'ros_build' first."
        return 1
    fi
}

# Function to build ROS workspace
ros_build() {
    echo "Building ROS 2 workspace..."
    cd "$ROS_WS"
    colcon build --symlink-install
    echo "✓ Build complete! Run 'ros_source' to source the environment."
}

# Function to build and source in one command
ros_setup() {
    ros_build && ros_source
}

# Function to run simulation
ros_run_sim() {
    cd "$ROS_WS"
    source install/setup.bash
    ros2 run robot_simulation diff_drive_sim
}

# Function to run control node
ros_run_control() {
    cd "$ROS_WS"
    source install/setup.bash
    python3 /workspace/docs/control_node_example.py /workspace/data/config_pid.yaml
}

# Function to run Unity bridge
ros_run_unity_bridge() {
    cd "$ROS_WS"
    source install/setup.bash
    ros2 run unity_bridge tcp_bridge
}

# Function to run tests
ros_test() {
    cd "$ROS_WS"
    source install/setup.bash
    colcon test
    colcon test-result --verbose
}

# Function to clean build artifacts
ros_clean() {
    echo "Cleaning ROS workspace build artifacts..."
    rm -rf "$ROS_WS/build" "$ROS_WS/install" "$ROS_WS/log"
    echo "✓ Clean complete!"
}

# Auto-source if workspace is already built
if [ -f "$ROS_WS/install/setup.bash" ]; then
    source "$ROS_WS/install/setup.bash"
    echo "✓ ROS helpers loaded (workspace already sourced)"
else
    echo "✓ ROS helpers loaded (run 'ros_build' to build workspace)"
fi

# Show available commands
echo ""
echo "Available ROS helper commands:"
echo "  ros_build          - Build ROS workspace"
echo "  ros_source         - Source ROS workspace environment"
echo "  ros_setup          - Build and source workspace (all-in-one)"
echo "  ros_run_sim        - Run robot simulation"
echo "  ros_run_control    - Run control node"
echo "  ros_run_unity_bridge - Run Unity bridge"
echo "  ros_test           - Run ROS tests"
echo "  ros_clean          - Clean build artifacts"
echo ""

