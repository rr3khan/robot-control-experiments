# Control command for differential drive robot
std_msgs/Header header

# Velocity commands
float64 linear_velocity  # m/s
float64 angular_velocity # rad/s

# Alternative: Direct wheel velocities
float64 left_wheel_velocity  # rad/s
float64 right_wheel_velocity # rad/s

# Control mode: 0 = velocity, 1 = wheel velocities
int8 control_mode
