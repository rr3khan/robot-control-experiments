# Unity Integration Guide

This directory contains resources for integrating Unity with the ROS 2 robotics control system.

## Overview

Unity is used for physics simulation and 3D visualization of the robot. It communicates with ROS 2 via a TCP bridge that sends robot state and receives control commands.

## Communication Protocol

### TCP Connection
- **Host**: `localhost` (or Docker container IP)
- **Port**: `10000`
- **Format**: JSON messages with newline delimiters

### Message Types

#### State Message (ROS → Unity)
Sent from ROS to Unity to update robot visualization:
```json
{
  "type": "state",
  "x": 0.0,
  "y": 0.0,
  "theta": 0.0,
  "linear_vel": 0.0,
  "angular_vel": 0.0
}
```

#### Control Message (Unity → ROS)
Sent from Unity to ROS for manual control or testing:
```json
{
  "type": "control",
  "linear_velocity": 0.5,
  "angular_velocity": 0.2
}
```

## Unity Setup Instructions

### 1. Create Unity Project
1. Create a new Unity 3D project (Unity 2021.3 LTS or newer recommended)
2. Set up a scene with:
   - Ground plane
   - Directional light
   - Main camera

### 2. Create Robot GameObject
1. Create a Cylinder or use a prefab for the robot body
2. Add wheel GameObjects as children
3. Apply physics components (Rigidbody, Colliders)

### 3. Add Communication Script
Copy the provided `RobotController.cs` script to your Unity project's Scripts folder.

### 4. Configure the Script
1. Attach `RobotController.cs` to your robot GameObject
2. Set the ROS bridge IP address (localhost or Docker IP)
3. Set the port (default: 10000)

## Example Unity Scripts

See the `unity_scripts/` directory for:
- `RobotController.cs` - Main robot control and TCP communication
- `CameraFollow.cs` - Camera that follows the robot
- `WaypointMarker.cs` - Visual markers for target positions

## Coordinate System Conversion

Unity uses a left-handed coordinate system, while ROS uses right-handed:
- Unity X → ROS X (forward)
- Unity Z → ROS Y (left)
- Unity Y → ROS Z (up, typically ignored for 2D)

The provided scripts handle this conversion automatically.

## Testing Connection

1. Start the ROS 2 system:
   ```bash
   docker-compose up
   ```

2. In the container, run the bridge:
   ```bash
   ros2 run unity_bridge tcp_bridge
   ```

3. Press Play in Unity - you should see "Connected to ROS" in the console

## Troubleshooting

- **Connection refused**: Ensure ROS bridge is running and firewall allows connections
- **No state updates**: Check ROS topics with `ros2 topic list` and `ros2 topic echo /robot_state`
- **Incorrect coordinates**: Verify coordinate system conversion in the Unity scripts

## Advanced Features

### Physics Simulation
Configure Unity's physics settings for realistic robot dynamics:
- Mass, drag, and angular drag on Rigidbody
- Friction on colliders for wheel-ground interaction

### Sensor Simulation
Add simulated sensors to the robot:
- Ray-cast based lidar/sonar
- Camera feeds for vision
- IMU data from physics simulation

### Multiple Robots
Instantiate multiple robot prefabs and manage separate TCP connections for each.
