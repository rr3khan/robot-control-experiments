"""
Experiment Logger

Logs robot state, control commands, and performance metrics to CSV files.
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any, Optional
import threading


class ExperimentLogger:
    """Logger for robotics experiments."""
    
    def __init__(self, experiment_id: str = None, output_dir: str = './logs'):
        """
        Initialize the experiment logger.
        
        Args:
            experiment_id: Unique identifier for the experiment
            output_dir: Directory to save log files
        """
        self.experiment_id = experiment_id or datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # CSV file path
        self.csv_path = os.path.join(output_dir, f'experiment_{self.experiment_id}.csv')
        
        # CSV headers
        self.headers = [
            'timestamp',
            'experiment_id',
            'controller_type',
            'x',
            'y',
            'theta',
            'linear_velocity',
            'angular_velocity',
            'target_x',
            'target_y',
            'target_theta',
            'control_linear',
            'control_angular',
            'position_error',
            'orientation_error'
        ]
        
        # Initialize CSV file
        self.file = None
        self.writer = None
        self.lock = threading.Lock()
        self._initialize_csv()
        
        print(f"Experiment logger initialized: {self.csv_path}")
    
    def _initialize_csv(self):
        """Initialize CSV file with headers."""
        self.file = open(self.csv_path, 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=self.headers)
        self.writer.writeheader()
        self.file.flush()
    
    def log(self, data: Dict[str, Any]):
        """
        Log experiment data.
        
        Args:
            data: Dictionary containing experiment data
        """
        with self.lock:
            try:
                # Ensure all headers are present
                row = {header: data.get(header, '') for header in self.headers}
                self.writer.writerow(row)
                self.file.flush()
            except Exception as e:
                print(f"Error logging data: {e}")
    
    def log_state_and_control(
        self,
        timestamp: float,
        controller_type: str,
        state: Dict[str, float],
        target: Dict[str, float],
        control: tuple
    ):
        """
        Log robot state and control signals.
        
        Args:
            timestamp: Current timestamp
            controller_type: Name of the controller
            state: Robot state dictionary
            target: Target state dictionary
            control: Control output tuple (linear, angular)
        """
        # Calculate errors
        import math
        dx = target.get('x', 0) - state.get('x', 0)
        dy = target.get('y', 0) - state.get('y', 0)
        position_error = math.sqrt(dx*dx + dy*dy)
        
        theta_diff = target.get('theta', 0) - state.get('theta', 0)
        orientation_error = math.atan2(math.sin(theta_diff), math.cos(theta_diff))
        
        data = {
            'timestamp': timestamp,
            'experiment_id': self.experiment_id,
            'controller_type': controller_type,
            'x': state.get('x', 0),
            'y': state.get('y', 0),
            'theta': state.get('theta', 0),
            'linear_velocity': state.get('v', 0),
            'angular_velocity': state.get('omega', 0),
            'target_x': target.get('x', 0),
            'target_y': target.get('y', 0),
            'target_theta': target.get('theta', 0),
            'control_linear': control[0],
            'control_angular': control[1],
            'position_error': position_error,
            'orientation_error': orientation_error
        }
        
        self.log(data)
    
    def close(self):
        """Close the log file."""
        with self.lock:
            if self.file:
                self.file.close()
                print(f"Experiment log saved: {self.csv_path}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class ROS2ExperimentLogger:
    """ROS 2 wrapper for experiment logging."""
    
    def __init__(self, node, experiment_id: str = None, output_dir: str = './logs'):
        """
        Initialize ROS 2 experiment logger.
        
        Args:
            node: ROS 2 node instance
            experiment_id: Unique identifier for the experiment
            output_dir: Directory to save log files
        """
        self.node = node
        self.logger = ExperimentLogger(experiment_id, output_dir)
        
        # Subscribe to experiment log topic
        from robot_control_interfaces.msg import ExperimentLog
        self.sub = node.create_subscription(
            ExperimentLog,
            'experiment_log',
            self.log_callback,
            10
        )
    
    def log_callback(self, msg):
        """Process experiment log messages."""
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        
        data = {
            'timestamp': timestamp,
            'experiment_id': msg.experiment_id,
            'controller_type': msg.controller_type,
            'x': msg.pose.x,
            'y': msg.pose.y,
            'theta': msg.pose.theta,
            'linear_velocity': msg.velocity.linear.x,
            'angular_velocity': msg.velocity.angular.z,
            'target_x': msg.target_pose.x,
            'target_y': msg.target_pose.y,
            'target_theta': msg.target_pose.theta,
            'control_linear': msg.control_linear,
            'control_angular': msg.control_angular,
            'position_error': msg.position_error,
            'orientation_error': msg.orientation_error
        }
        
        self.logger.log(data)
    
    def close(self):
        """Close the logger."""
        self.logger.close()
