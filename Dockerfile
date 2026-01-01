# ROS 2 Humble Docker Image for Robotics Control Experiments
FROM ros:humble

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    ros-humble-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace
COPY ros2_ws /workspace/ros2_ws

# Install Python dependencies
COPY requirements.txt /workspace/
RUN pip3 install -r /workspace/requirements.txt

# Source ROS 2 setup
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Set environment variables
ENV ROS_DOMAIN_ID=42
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Build workspace (will be done on first run)
CMD ["/bin/bash"]
