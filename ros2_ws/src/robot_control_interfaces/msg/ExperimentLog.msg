# Experiment logging message
std_msgs/Header header

# Experiment metadata
string experiment_id
string controller_type

# Robot state
geometry_msgs/Pose2D pose
geometry_msgs/Twist velocity

# Control signals
float64 control_linear
float64 control_angular

# Target/setpoint
geometry_msgs/Pose2D target_pose

# Error metrics
float64 position_error
float64 orientation_error
