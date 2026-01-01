"""
PID Controller for Differential Drive Robot

Implements a PID controller for position and orientation control.
"""

import math
from typing import Tuple, Dict, Any
from .base_controller import Controller


class PIDController(Controller):
    """PID controller for differential drive robot."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize PID controller.
        
        Config parameters:
            kp_linear: Proportional gain for linear velocity
            ki_linear: Integral gain for linear velocity
            kd_linear: Derivative gain for linear velocity
            kp_angular: Proportional gain for angular velocity
            ki_angular: Integral gain for angular velocity
            kd_angular: Derivative gain for angular velocity
            max_linear_vel: Maximum linear velocity
            max_angular_vel: Maximum angular velocity
        """
        default_config = {
            'kp_linear': 1.0,
            'ki_linear': 0.0,
            'kd_linear': 0.1,
            'kp_angular': 2.0,
            'ki_angular': 0.0,
            'kd_angular': 0.2,
            'max_linear_vel': 0.5,
            'max_angular_vel': 2.0,
            'position_tolerance': 0.05,
            'orientation_tolerance': 0.1
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(default_config)
        
    def reset(self):
        """Reset controller state."""
        self.error_sum_linear = 0.0
        self.error_sum_angular = 0.0
        self.prev_error_linear = 0.0
        self.prev_error_angular = 0.0
    
    def get_name(self) -> str:
        """Return controller name."""
        return "PID"
    
    def compute_control(self, state: Dict[str, float], target: Dict[str, float]) -> Tuple[float, float]:
        """
        Compute PID control output.
        
        Args:
            state: Current state with keys: x, y, theta, v, omega
            target: Target state with keys: x, y, theta
        
        Returns:
            Tuple of (linear_velocity, angular_velocity)
        """
        # Extract state and target
        x, y, theta = state['x'], state['y'], state['theta']
        target_x, target_y = target['x'], target['y']
        target_theta = target.get('theta', 0.0)
        
        # Calculate position error
        dx = target_x - x
        dy = target_y - y
        distance_error = math.sqrt(dx*dx + dy*dy)
        
        # Calculate angle to target
        angle_to_target = math.atan2(dy, dx)
        
        # Calculate angular error (normalized to [-pi, pi])
        angular_error = self._normalize_angle(angle_to_target - theta)
        
        # If we're close to target, focus on orientation
        if distance_error < self.config['position_tolerance']:
            angular_error = self._normalize_angle(target_theta - theta)
            distance_error = 0.0
        
        # PID for linear velocity
        self.error_sum_linear += distance_error
        error_diff_linear = distance_error - self.prev_error_linear
        
        linear_vel = (
            self.config['kp_linear'] * distance_error +
            self.config['ki_linear'] * self.error_sum_linear +
            self.config['kd_linear'] * error_diff_linear
        )
        
        # PID for angular velocity
        self.error_sum_angular += angular_error
        error_diff_angular = angular_error - self.prev_error_angular
        
        angular_vel = (
            self.config['kp_angular'] * angular_error +
            self.config['ki_angular'] * self.error_sum_angular +
            self.config['kd_angular'] * error_diff_angular
        )
        
        # Update previous errors
        self.prev_error_linear = distance_error
        self.prev_error_angular = angular_error
        
        # Apply limits
        linear_vel = max(-self.config['max_linear_vel'], 
                        min(self.config['max_linear_vel'], linear_vel))
        angular_vel = max(-self.config['max_angular_vel'], 
                         min(self.config['max_angular_vel'], angular_vel))
        
        return linear_vel, angular_vel
    
    def _normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-pi, pi]."""
        return math.atan2(math.sin(angle), math.cos(angle))
