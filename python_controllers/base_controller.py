"""
Base Controller Interface

Defines the abstract interface that all controllers must implement.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any


class Controller(ABC):
    """Abstract base class for robot controllers."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the controller.
        
        Args:
            config: Configuration dictionary for the controller
        """
        self.config = config or {}
        self.reset()
    
    @abstractmethod
    def compute_control(self, state: Dict[str, float], target: Dict[str, float]) -> Tuple[float, float]:
        """
        Compute control output based on current state and target.
        
        Args:
            state: Current robot state (x, y, theta, v, omega)
            target: Target state (x, y, theta)
        
        Returns:
            Tuple of (linear_velocity, angular_velocity)
        """
        pass
    
    @abstractmethod
    def reset(self):
        """Reset controller internal state."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the controller name."""
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """Return the controller configuration."""
        return self.config
