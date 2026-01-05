"""
Differential Drive Robot Simulation Node

Simulates a differential drive robot's kinematics and publishes state information.
Subscribes to control commands and updates robot state accordingly.
"""

import rclpy
from rclpy.node import Node
from robot_control_interfaces.msg import RobotState, ControlCommand
import math


class DifferentialDriveRobot:
    """Kinematic model for a differential drive robot."""
    
    def __init__(self, wheel_radius=0.05, wheel_base=0.3):
        """
        Initialize the differential drive robot.
        
        Args:
            wheel_radius: Radius of the wheels in meters (default: 0.05m = 5cm)
            wheel_base: Distance between wheels in meters (default: 0.3m = 30cm)
        """
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base
        
        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v = 0.0  # linear velocity
        self.omega = 0.0  # angular velocity
        self.left_wheel_vel = 0.0
        self.right_wheel_vel = 0.0
    
    def update(self, left_wheel_vel, right_wheel_vel, dt):
        """
        Update robot state based on wheel velocities.
        
        Args:
            left_wheel_vel: Left wheel angular velocity (rad/s)
            right_wheel_vel: Right wheel angular velocity (rad/s)
            dt: Time step in seconds
        """
        self.left_wheel_vel = left_wheel_vel
        self.right_wheel_vel = right_wheel_vel
        
        # Calculate linear and angular velocities
        v_left = left_wheel_vel * self.wheel_radius
        v_right = right_wheel_vel * self.wheel_radius
        
        self.v = (v_right + v_left) / 2.0
        self.omega = (v_right - v_left) / self.wheel_base
        
        # Update pose using differential drive kinematics
        if abs(self.omega) < 1e-6:
            # Moving straight
            self.x += self.v * math.cos(self.theta) * dt
            self.y += self.v * math.sin(self.theta) * dt
        else:
            # Circular motion
            radius = self.v / self.omega
            icc_x = self.x - radius * math.sin(self.theta)
            icc_y = self.y + radius * math.cos(self.theta)
            
            d_theta = self.omega * dt
            # Store original position before updating
            old_x = self.x
            old_y = self.y
            self.x = math.cos(d_theta) * (old_x - icc_x) - math.sin(d_theta) * (old_y - icc_y) + icc_x
            self.y = math.sin(d_theta) * (old_x - icc_x) + math.cos(d_theta) * (old_y - icc_y) + icc_y
            self.theta += d_theta
        
        # Normalize theta to [-pi, pi]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
    
    def set_velocity(self, linear_vel, angular_vel):
        """
        Set robot velocity commands and convert to wheel velocities.
        
        Args:
            linear_vel: Desired linear velocity (m/s)
            angular_vel: Desired angular velocity (rad/s)
        """
        self.v = linear_vel
        self.omega = angular_vel
        
        # Convert to wheel velocities
        v_left = linear_vel - (angular_vel * self.wheel_base) / 2.0
        v_right = linear_vel + (angular_vel * self.wheel_base) / 2.0
        
        self.left_wheel_vel = v_left / self.wheel_radius
        self.right_wheel_vel = v_right / self.wheel_radius


class DiffDriveSimNode(Node):
    """ROS 2 node for differential drive robot simulation."""
    
    def __init__(self):
        super().__init__('diff_drive_sim')
        
        # Parameters
        self.declare_parameter('update_rate', 50.0)
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('wheel_base', 0.3)
        
        update_rate = self.get_parameter('update_rate').value
        wheel_radius = self.get_parameter('wheel_radius').value
        wheel_base = self.get_parameter('wheel_base').value
        
        # Initialize robot model
        self.robot = DifferentialDriveRobot(wheel_radius, wheel_base)
        
        # Publishers
        self.state_pub = self.create_publisher(RobotState, 'robot_state', 10)
        
        # Subscribers
        self.cmd_sub = self.create_subscription(
            ControlCommand,
            'control_command',
            self.control_callback,
            10
        )
        
        # Timer for state updates
        self.dt = 1.0 / update_rate
        self.timer = self.create_timer(self.dt, self.update_callback)
        
        self.get_logger().info(f'Differential drive simulation started (rate: {update_rate} Hz)')
    
    def control_callback(self, msg):
        """Process control commands."""
        if msg.control_mode == 0:
            # Velocity control mode
            self.robot.set_velocity(msg.linear_velocity, msg.angular_velocity)
        elif msg.control_mode == 1:
            # Direct wheel velocity control
            self.robot.left_wheel_vel = msg.left_wheel_velocity
            self.robot.right_wheel_vel = msg.right_wheel_velocity
    
    def update_callback(self):
        """Update robot state and publish."""
        # Update robot kinematics
        self.robot.update(
            self.robot.left_wheel_vel,
            self.robot.right_wheel_vel,
            self.dt
        )
        
        # Publish state
        state_msg = RobotState()
        state_msg.header.stamp = self.get_clock().now().to_msg()
        state_msg.header.frame_id = 'world'
        
        state_msg.pose.x = self.robot.x
        state_msg.pose.y = self.robot.y
        state_msg.pose.theta = self.robot.theta
        
        state_msg.velocity.linear.x = self.robot.v
        state_msg.velocity.angular.z = self.robot.omega
        
        state_msg.left_wheel_velocity = self.robot.left_wheel_vel
        state_msg.right_wheel_velocity = self.robot.right_wheel_vel
        state_msg.battery_level = 100.0  # Placeholder
        
        self.state_pub.publish(state_msg)


def main(args=None):
    rclpy.init(args=args)
    node = DiffDriveSimNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
