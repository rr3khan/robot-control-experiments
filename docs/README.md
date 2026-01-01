# Documentation Index

Welcome to the Robot Control Experiments documentation!

## 📚 Documentation Overview

This directory contains comprehensive documentation for the robotics control experimentation playground.

## 🚀 Getting Started

**Start here if you're new to the project:**

1. **[Getting Started Guide](GETTING_STARTED.md)** - Installation, first experiment, and basic usage
2. **[Example Workflow](EXAMPLE_WORKFLOW.md)** - Complete step-by-step walkthrough of a full experiment

## 📖 Core Documentation

### Architecture & Design
- **[Architecture Overview](ARCHITECTURE.md)** - System architecture, design decisions, and technology choices

### Development Guides
- **[Adding Controllers](ADDING_CONTROLLERS.md)** - How to implement custom control algorithms

### Code Examples
- **[control_node_example.py](control_node_example.py)** - Example ROS 2 node for robot control

## 📁 Quick Reference

### Directory Structure
```
docs/
├── README.md                    # This file
├── GETTING_STARTED.md          # Installation and first steps
├── ARCHITECTURE.md             # System design documentation
├── EXAMPLE_WORKFLOW.md         # Complete workflow example
├── ADDING_CONTROLLERS.md       # Controller development guide
└── control_node_example.py     # Example control node
```

### Key Concepts

#### Controllers
Controllers implement control algorithms (PID, Pure Pursuit, MPC, etc.) using a common interface:
```python
from python_controllers import Controller

class MyController(Controller):
    def compute_control(self, state, target):
        # Your control logic
        return linear_vel, angular_vel
```

#### Robot Simulation
Differential drive robot with kinematic model:
- Forward kinematics based on wheel velocities
- Publishes state at 50 Hz
- Configurable wheel radius and base width

#### Experiment Logging
CSV-based logging with schema:
- Timestamp, positions, velocities
- Control signals
- Target positions
- Error metrics

#### Analysis
Python tools for:
- Trajectory plotting
- Error analysis
- Performance metrics
- Multi-experiment comparison

## 🎯 Common Tasks

### Run an Experiment
```bash
# 1. Start simulation
ros2 run robot_simulation diff_drive_sim

# 2. Run control node
python3 docs/control_node_example.py data/config_pid.yaml
```

### Analyze Results
```bash
python3 analysis/analysis_utils.py logs/experiment_*.csv
```

### Add a New Controller
See [ADDING_CONTROLLERS.md](ADDING_CONTROLLERS.md)

### Visualize in Unity
See [../unity_integration/README.md](../unity_integration/README.md)

## 📊 Example Use Cases

### 1. Tuning PID Parameters
1. Run experiment with baseline parameters
2. Analyze performance metrics
3. Adjust gains in config file
4. Run again and compare results

### 2. Comparing Controllers
1. Implement multiple controllers
2. Run same trajectory with each
3. Use `compare_experiments()` to visualize differences
4. Choose best controller for your use case

### 3. Path Following
1. Define waypoints in config file
2. Choose appropriate controller (PID, Pure Pursuit)
3. Run experiment
4. Analyze trajectory accuracy

### 4. Performance Optimization
1. Log multiple experiments with different parameters
2. Compute statistics (mean error, max error, settling time)
3. Plot performance surfaces
4. Find optimal parameters

## 🔧 Configuration Files

### Main Config (`data/config_pid.yaml`)
```yaml
controller:
  type: "PID"
  config:
    kp_linear: 1.0
    # ... other parameters

robot:
  wheel_radius: 0.05
  wheel_base: 0.3

experiment:
  waypoints:
    - [1.0, 0.0, 0.0]
    # ... more waypoints
```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
source /workspace/ros2_ws/install/setup.bash
export PYTHONPATH=/workspace:$PYTHONPATH
```

**No ROS Topics**
```bash
ros2 node list
ros2 topic list
```

**Docker Issues**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for more troubleshooting tips.

## 🤝 Contributing

When adding new features:

1. **Controllers**: Follow the `Controller` interface
2. **Documentation**: Update relevant guides
3. **Examples**: Add example configs and usage
4. **Tests**: Include unit tests where applicable

## 📚 Additional Resources

### ROS 2
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [rclpy API Reference](https://docs.ros2.org/latest/api/rclpy/)

### Control Theory
- [Modern Control Engineering](https://www.pearson.com/us/higher-education/program/Ogata-Modern-Control-Engineering-5th-Edition/PGM241613.html)
- [Robot Modeling and Control](http://www.diag.uniroma1.it/~deluca/rob1_en/material_rob1_en_SICILIANO_BOOK.pdf)

### Unity Integration
- [Unity Documentation](https://docs.unity3d.com/)
- [ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector)

## 📝 Documentation Standards

When writing documentation:
- Use clear, concise language
- Include code examples
- Provide expected outputs
- Add troubleshooting sections
- Keep it up-to-date with code changes

## 🎓 Learning Path

**Beginner:**
1. Read Getting Started Guide
2. Follow Example Workflow
3. Run existing experiments
4. Modify PID parameters

**Intermediate:**
5. Read Architecture Overview
6. Implement custom controller
7. Compare controller performance
8. Integrate Unity visualization

**Advanced:**
9. Add sensor simulation
10. Implement advanced controllers (MPC, RL)
11. Multi-robot coordination
12. Hardware integration

## 📞 Support

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: See main README.md

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details.

---

**Quick Navigation:**
- [← Back to Main README](../README.md)
- [Getting Started →](GETTING_STARTED.md)
- [Architecture →](ARCHITECTURE.md)
- [Example Workflow →](EXAMPLE_WORKFLOW.md)
