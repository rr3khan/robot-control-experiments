"""
Controller Factory

Factory pattern for creating and managing different controller types.
"""

from typing import Dict, Any, Type
from .base_controller import Controller
from .pid_controller import PIDController


class ControllerFactory:
    """Factory for creating controller instances."""
    
    _controllers: Dict[str, Type[Controller]] = {
        'PID': PIDController,
    }
    
    @classmethod
    def create_controller(cls, controller_type: str, config: Dict[str, Any] = None) -> Controller:
        """
        Create a controller instance.
        
        Args:
            controller_type: Type of controller to create (e.g., 'PID')
            config: Configuration dictionary for the controller
        
        Returns:
            Controller instance
        
        Raises:
            ValueError: If controller_type is not registered
        """
        if controller_type not in cls._controllers:
            raise ValueError(
                f"Unknown controller type: {controller_type}. "
                f"Available: {list(cls._controllers.keys())}"
            )
        
        controller_class = cls._controllers[controller_type]
        return controller_class(config)
    
    @classmethod
    def register_controller(cls, name: str, controller_class: Type[Controller]):
        """
        Register a new controller type.
        
        Args:
            name: Name of the controller
            controller_class: Controller class (must inherit from Controller)
        """
        if not issubclass(controller_class, Controller):
            raise TypeError(f"{controller_class} must inherit from Controller")
        
        cls._controllers[name] = controller_class
    
    @classmethod
    def list_controllers(cls) -> list:
        """List all registered controller types."""
        return list(cls._controllers.keys())
