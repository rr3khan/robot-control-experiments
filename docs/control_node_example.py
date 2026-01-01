#!/usr/bin/env python3
"""
Example Robot Control Node

Demonstrates how to use the PID controller with the robot simulation.
"""

import rclpy
from rclpy.node import Node
from robot_control_interfaces.msg import RobotState, ControlCommand, ExperimentLog
import yaml
import sys
import os

# Add python_controllers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_controllers'))

from controller_factory import ControllerFactory


class ControlNode(Node):
    """ROS 2 node for robot control experiments."""
    
    def __init__(self, config_file):
        super().__init__('control_node')
        
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Create controller
        controller_config = self.config['controller']['config']
        controller_type = self.config['controller']['type']
        self.controller = ControllerFactory.create_controller(controller_type, controller_config)
        
        # Experiment settings
        exp_config = self.config.get('experiment', {})
        self.experiment_id = exp_config.get('id', 'default')
        self.waypoints = exp_config.get('waypoints', [[1.0, 0.0, 0.0]])
        self.current_waypoint_idx = 0
        
        # Robot state
        self.current_state = None
        
        # Publishers
        self.cmd_pub = self.create_publisher(ControlCommand, 'control_command', 10)
        self.log_pub = self.create_publisher(ExperimentLog, 'experiment_log', 10)
        
        # Subscribers
        self.state_sub = self.create_subscription(
            RobotState,
            'robot_state',
            self.state_callback,
            10
        )
        
        # Control timer
        update_rate = exp_config.get('update_rate', 50.0)
        self.timer = self.create_timer(1.0 / update_rate, self.control_loop)
        
        self.get_logger().info(f'Control node started with {controller_type} controller')
        self.get_logger().info(f'Experiment ID: {self.experiment_id}')
    
    def state_callback(self, msg):
        """Store current robot state."""
        self.current_state = {
            'x': msg.pose.x,
            'y': msg.pose.y,
            'theta': msg.pose.theta,
            'v': msg.velocity.linear.x,
            'omega': msg.velocity.angular.z
        }
    
    def control_loop(self):
        """Main control loop."""
        if self.current_state is None:
            return
        
        # Get current target waypoint
        if self.current_waypoint_idx >= len(self.waypoints):
            # Completed all waypoints
            return
        
        waypoint = self.waypoints[self.current_waypoint_idx]
        target = {
            'x': waypoint[0],
            'y': waypoint[1],
            'theta': waypoint[2] if len(waypoint) > 2 else 0.0
        }
        
        # Compute control
        linear_vel, angular_vel = self.controller.compute_control(self.current_state, target)
        
        # Publish control command
        cmd_msg = ControlCommand()
        cmd_msg.header.stamp = self.get_clock().now().to_msg()
        cmd_msg.linear_velocity = linear_vel
        cmd_msg.angular_velocity = angular_vel
        cmd_msg.control_mode = 0
        
        self.cmd_pub.publish(cmd_msg)
        
        # Publish experiment log
        log_msg = ExperimentLog()
        log_msg.header.stamp = self.get_clock().now().to_msg()
        log_msg.experiment_id = self.experiment_id
        log_msg.controller_type = self.controller.get_name()
        
        log_msg.pose.x = self.current_state['x']
        log_msg.pose.y = self.current_state['y']
        log_msg.pose.theta = self.current_state['theta']
        
        log_msg.velocity.linear.x = self.current_state['v']
        log_msg.velocity.angular.z = self.current_state['omega']
        
        log_msg.target_pose.x = target['x']
        log_msg.target_pose.y = target['y']
        log_msg.target_pose.theta = target['theta']
        
        log_msg.control_linear = linear_vel
        log_msg.control_angular = angular_vel
        
        # Calculate errors
        import math
        dx = target['x'] - self.current_state['x']
        dy = target['y'] - self.current_state['y']
        log_msg.position_error = math.sqrt(dx*dx + dy*dy)
        
        theta_diff = target['theta'] - self.current_state['theta']
        log_msg.orientation_error = math.atan2(math.sin(theta_diff), math.cos(theta_diff))
        
        self.log_pub.publish(log_msg)
        
        # Check if waypoint reached
        if log_msg.position_error < 0.1:  # 10 cm tolerance
            self.current_waypoint_idx += 1
            if self.current_waypoint_idx < len(self.waypoints):
                self.get_logger().info(f'Reached waypoint {self.current_waypoint_idx}, moving to next')
            else:
                self.get_logger().info('All waypoints reached!')


def main(args=None):
    rclpy.init(args=args)
    
    if len(sys.argv) < 2:
        print("Usage: ros2 run <package> control_node_example.py <config.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    node = ControlNode(config_file)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
