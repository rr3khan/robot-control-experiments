# Robot state information
std_msgs/Header header

# Position (x, y in meters, theta in radians)
geometry_msgs/Pose2D pose

# Velocity (linear and angular)
geometry_msgs/Twist velocity

# Additional state
float64 left_wheel_velocity
float64 right_wheel_velocity
float64 battery_level
