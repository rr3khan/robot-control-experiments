"""
Unity TCP Bridge for ROS 2

Provides a TCP server that Unity can connect to for bidirectional communication.
Converts between Unity's coordinate system and ROS messages.
"""

import rclpy
from rclpy.node import Node
from robot_control_interfaces.msg import RobotState, ControlCommand
import socket
import json
import threading
import time


class UnityTCPBridge(Node):
    """ROS 2 node that bridges Unity via TCP socket."""
    
    def __init__(self):
        super().__init__('unity_tcp_bridge')
        
        # Parameters
        self.declare_parameter('host', '0.0.0.0')
        self.declare_parameter('port', 10000)
        self.declare_parameter('buffer_size', 4096)
        
        self.host = self.get_parameter('host').value
        self.port = self.get_parameter('port').value
        self.buffer_size = self.get_parameter('buffer_size').value
        
        # ROS Publishers and Subscribers
        self.cmd_pub = self.create_publisher(ControlCommand, 'control_command', 10)
        self.state_sub = self.create_subscription(
            RobotState,
            'robot_state',
            self.state_callback,
            10
        )
        
        # TCP server
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.running = False
        
        # Latest robot state
        self.latest_state = None
        
        # Start TCP server in a separate thread
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()
        
        self.get_logger().info(f'Unity TCP Bridge started on {self.host}:{self.port}')
    
    def state_callback(self, msg):
        """Store latest robot state."""
        self.latest_state = msg
    
    def run_server(self):
        """Run TCP server to accept Unity connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.running = True
            
            self.get_logger().info('Waiting for Unity connection...')
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    self.client_socket, self.client_address = self.server_socket.accept()
                    self.get_logger().info(f'Unity connected from {self.client_address}')
                    
                    self.handle_client()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    self.get_logger().error(f'Server error: {e}')
                    
        except Exception as e:
            self.get_logger().error(f'Failed to start server: {e}')
        finally:
            self.cleanup()
    
    def handle_client(self):
        """Handle communication with connected Unity client."""
        try:
            while self.running:
                # Send state to Unity
                if self.latest_state is not None:
                    state_data = {
                        'type': 'state',
                        'x': self.latest_state.pose.x,
                        'y': self.latest_state.pose.y,
                        'theta': self.latest_state.pose.theta,
                        'linear_vel': self.latest_state.velocity.linear.x,
                        'angular_vel': self.latest_state.velocity.angular.z,
                    }
                    self.send_json(state_data)
                
                # Receive commands from Unity
                self.client_socket.settimeout(0.01)
                try:
                    data = self.client_socket.recv(self.buffer_size)
                    if not data:
                        break
                    
                    cmd_data = json.loads(data.decode('utf-8'))
                    
                    if cmd_data.get('type') == 'control':
                        # Create and publish control command
                        cmd_msg = ControlCommand()
                        cmd_msg.header.stamp = self.get_clock().now().to_msg()
                        cmd_msg.linear_velocity = cmd_data.get('linear_velocity', 0.0)
                        cmd_msg.angular_velocity = cmd_data.get('angular_velocity', 0.0)
                        cmd_msg.control_mode = 0
                        
                        self.cmd_pub.publish(cmd_msg)
                        
                except socket.timeout:
                    pass
                except json.JSONDecodeError:
                    self.get_logger().warn('Invalid JSON received from Unity')
                
                time.sleep(0.02)  # 50 Hz update rate
                
        except Exception as e:
            self.get_logger().error(f'Client handling error: {e}')
        finally:
            self.get_logger().info('Unity disconnected')
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
    
    def send_json(self, data):
        """Send JSON data to Unity."""
        try:
            json_str = json.dumps(data) + '\n'
            self.client_socket.sendall(json_str.encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f'Failed to send data: {e}')
    
    def cleanup(self):
        """Clean up sockets."""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()


def main(args=None):
    rclpy.init(args=args)
    node = UnityTCPBridge()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cleanup()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
