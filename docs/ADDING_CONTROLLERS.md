# Example: Adding a New Controller

This guide demonstrates how to add a custom controller to the system.

## Step 1: Create Controller Class

Create a new file `python_controllers/pure_pursuit_controller.py`:

```python
"""
Pure Pursuit Controller

A path-following controller that uses the Pure Pursuit algorithm.
"""

import math
from typing import Tuple, Dict, Any, List
from .base_controller import Controller


class PurePursuitController(Controller):
    """Pure Pursuit controller for path following."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Pure Pursuit controller.
        
        Config parameters:
            lookahead_distance: Distance to look ahead on path (m)
            max_linear_vel: Maximum linear velocity (m/s)
            path: List of waypoints [[x, y], ...]
        """
        default_config = {
            'lookahead_distance': 0.5,
            'max_linear_vel': 0.5,
            'path': []
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(default_config)
        self.path = self.config.get('path', [])
        self.current_waypoint_idx = 0
    
    def reset(self):
        """Reset controller state."""
        self.current_waypoint_idx = 0
    
    def get_name(self) -> str:
        """Return controller name."""
        return "PurePursuit"
    
    def compute_control(self, state: Dict[str, float], target: Dict[str, float]) -> Tuple[float, float]:
        """
        Compute Pure Pursuit control.
        
        Args:
            state: Current state with keys: x, y, theta, v, omega
            target: Target state (not used, follows path instead)
        
        Returns:
            Tuple of (linear_velocity, angular_velocity)
        """
        if not self.path:
            return 0.0, 0.0
        
        # Find lookahead point
        lookahead_point = self._find_lookahead_point(state)
        
        if lookahead_point is None:
            return 0.0, 0.0
        
        # Calculate angle to lookahead point
        dx = lookahead_point[0] - state['x']
        dy = lookahead_point[1] - state['y']
        
        angle_to_lookahead = math.atan2(dy, dx)
        angle_diff = self._normalize_angle(angle_to_lookahead - state['theta'])
        
        # Pure pursuit geometry
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Calculate curvature
        curvature = 2 * math.sin(angle_diff) / distance if distance > 0 else 0
        
        # Control outputs
        linear_vel = self.config['max_linear_vel']
        angular_vel = linear_vel * curvature
        
        return linear_vel, angular_vel
    
    def _find_lookahead_point(self, state: Dict[str, float]):
        """Find the lookahead point on the path."""
        lookahead = self.config['lookahead_distance']
        
        # Find closest point on path
        min_dist = float('inf')
        closest_idx = 0
        
        for i, waypoint in enumerate(self.path):
            dx = waypoint[0] - state['x']
            dy = waypoint[1] - state['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        # Find point at lookahead distance
        for i in range(closest_idx, len(self.path)):
            waypoint = self.path[i]
            dx = waypoint[0] - state['x']
            dy = waypoint[1] - state['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist >= lookahead:
                return waypoint
        
        # Return last point if we're near the end
        return self.path[-1] if self.path else None
    
    def _normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-pi, pi]."""
        return math.atan2(math.sin(angle), math.cos(angle))
```

## Step 2: Register the Controller

Add to `python_controllers/controller_factory.py`:

```python
from .pure_pursuit_controller import PurePursuitController

class ControllerFactory:
    _controllers: Dict[str, Type[Controller]] = {
        'PID': PIDController,
        'PurePursuit': PurePursuitController,  # Add this line
    }
```

## Step 3: Update __init__.py

Add to `python_controllers/__init__.py`:

```python
from .pure_pursuit_controller import PurePursuitController

__all__ = ['Controller', 'PIDController', 'PurePursuitController', 'ControllerFactory']
```

## Step 4: Create Configuration File

Create `data/config_pure_pursuit.yaml`:

```yaml
controller:
  type: "PurePursuit"
  config:
    lookahead_distance: 0.5
    max_linear_vel: 0.5
    path:
      - [0.0, 0.0]
      - [1.0, 0.0]
      - [2.0, 0.5]
      - [3.0, 1.0]
      - [3.0, 2.0]

robot:
  wheel_radius: 0.05
  wheel_base: 0.3

experiment:
  id: "pure_pursuit_test_001"
  update_rate: 50.0
```

## Step 5: Test Your Controller

```bash
# Start simulation
ros2 run robot_simulation diff_drive_sim

# In another terminal, run your controller
python3 docs/control_node_example.py data/config_pure_pursuit.yaml
```

## Step 6: Analyze Results

```bash
python3 analysis/analysis_utils.py logs/experiment_pure_pursuit_test_001.csv
```

## Step 7: Compare with PID

```python
from analysis import compare_experiments

compare_experiments([
    'logs/experiment_pid.csv',
    'logs/experiment_pure_pursuit_test_001.csv'
], output_path='pid_vs_pure_pursuit.png')
```

## Advanced: Adding Parameters

To make your controller more configurable:

```python
class MyAdvancedController(Controller):
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'param1': 1.0,
            'param2': 2.0,
            'enable_feature_x': True,
            'mode': 'aggressive'  # or 'conservative'
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(default_config)
        
        # Initialize based on config
        if self.config['mode'] == 'aggressive':
            self.gain_multiplier = 1.5
        else:
            self.gain_multiplier = 0.8
```

## Testing Tips

1. **Unit Tests**: Test controller logic in isolation
```python
def test_pure_pursuit():
    controller = PurePursuitController({
        'lookahead_distance': 0.5,
        'path': [[0, 0], [1, 0], [2, 0]]
    })
    
    state = {'x': 0, 'y': 0, 'theta': 0, 'v': 0, 'omega': 0}
    target = {'x': 2, 'y': 0, 'theta': 0}
    
    linear, angular = controller.compute_control(state, target)
    
    assert linear > 0
    assert abs(angular) < 0.1  # Should go mostly straight
```

2. **Integration Tests**: Test with ROS nodes
3. **Performance Tests**: Compare with baseline (PID)

## Best Practices

1. **Documentation**: Add comprehensive docstrings
2. **Configuration**: Use config dict for all parameters
3. **Validation**: Validate inputs and handle edge cases
4. **Error Handling**: Gracefully handle unexpected states
5. **Testing**: Write unit tests for control logic
6. **Logging**: Use ROS logging for debugging

## Common Patterns

### State Machine Controller
```python
class StateMachineController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.state = 'IDLE'
    
    def compute_control(self, state, target):
        if self.state == 'IDLE':
            return self._idle_control()
        elif self.state == 'APPROACHING':
            return self._approach_control(state, target)
        elif self.state == 'ALIGNING':
            return self._align_control(state, target)
```

### Hybrid Controller
```python
class HybridController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.pid = PIDController(config['pid'])
        self.mpc = MPCController(config['mpc'])
    
    def compute_control(self, state, target):
        # Use MPC for planning, PID for execution
        waypoint = self.mpc.get_next_waypoint(state, target)
        return self.pid.compute_control(state, waypoint)
```

### Adaptive Controller
```python
class AdaptiveController(Controller):
    def compute_control(self, state, target):
        # Adjust gains based on error
        error = self._compute_error(state, target)
        
        if error > self.config['high_error_threshold']:
            gain = self.config['high_gain']
        else:
            gain = self.config['low_gain']
        
        # Use adaptive gain...
```

## Resources

- [Pure Pursuit Algorithm](https://www.ri.cmu.edu/pub_files/pub3/coulter_r_craig_1992_1/coulter_r_craig_1992_1.pdf)
- [ROS 2 Python Client Library](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [Control Theory Basics](https://www.cds.caltech.edu/~murray/courses/cds101/fa02/caltech/astrom-ch1.pdf)
