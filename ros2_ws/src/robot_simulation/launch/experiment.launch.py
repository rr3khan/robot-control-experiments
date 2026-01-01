"""
Launch file for robot control experiments

Starts the robot simulation and Unity bridge.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with robot sim and unity bridge."""
    
    return LaunchDescription([
        # Robot simulation node
        Node(
            package='robot_simulation',
            executable='diff_drive_sim',
            name='diff_drive_sim',
            output='screen',
            parameters=[{
                'update_rate': 50.0,
                'wheel_radius': 0.05,
                'wheel_base': 0.3,
            }]
        ),
        
        # Unity bridge node
        Node(
            package='unity_bridge',
            executable='tcp_bridge',
            name='unity_bridge',
            output='screen',
            parameters=[{
                'host': '0.0.0.0',
                'port': 10000,
            }]
        ),
    ])
