#!/usr/bin/env python3
"""
Quick Start Demo

Demonstrates the robot control system with a simple trajectory.
"""

import rclpy
from rclpy.node import Node
from robot_control_interfaces.msg import RobotState, ControlCommand
import time
import math


class QuickDemo(Node):
    """Quick demo node."""
    
    def __init__(self):
        super().__init__('quick_demo')
        
        # Publishers
        self.cmd_pub = self.create_publisher(ControlCommand, 'control_command', 10)
        
        # Subscribers
        self.state_sub = self.create_subscription(
            RobotState,
            'robot_state',
            self.state_callback,
            10
        )
        
        self.current_state = None
        self.get_logger().info('Quick demo started - Robot will move in a square pattern')
    
    def state_callback(self, msg):
        """Store robot state."""
        self.current_state = msg
    
    def send_command(self, linear, angular, duration):
        """Send velocity command for specified duration."""
        cmd = ControlCommand()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.linear_velocity = linear
        cmd.angular_velocity = angular
        cmd.control_mode = 0
        
        start_time = time.time()
        while time.time() - start_time < duration:
            self.cmd_pub.publish(cmd)
            time.sleep(0.02)  # 50 Hz
    
    def run_demo(self):
        """Run the demo sequence."""
        self.get_logger().info('Waiting for robot state...')
        while self.current_state is None:
            rclpy.spin_once(self, timeout_sec=0.1)
        
        self.get_logger().info('Moving forward...')
        self.send_command(0.3, 0.0, 3.0)  # Forward for 3 seconds
        
        self.get_logger().info('Turning left...')
        self.send_command(0.0, 1.57, 1.0)  # Turn 90 degrees
        
        self.get_logger().info('Moving forward...')
        self.send_command(0.3, 0.0, 3.0)
        
        self.get_logger().info('Turning left...')
        self.send_command(0.0, 1.57, 1.0)
        
        self.get_logger().info('Moving forward...')
        self.send_command(0.3, 0.0, 3.0)
        
        self.get_logger().info('Turning left...')
        self.send_command(0.0, 1.57, 1.0)
        
        self.get_logger().info('Moving forward...')
        self.send_command(0.3, 0.0, 3.0)
        
        self.get_logger().info('Stopping...')
        self.send_command(0.0, 0.0, 1.0)
        
        self.get_logger().info('Demo complete!')


def main(args=None):
    rclpy.init(args=args)
    node = QuickDemo()
    
    try:
        node.run_demo()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
