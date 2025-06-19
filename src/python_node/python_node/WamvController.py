from python_node.PIDController import PIDController
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Bool

class WamvController(Node):
    def __init__(self):
        super().__init__('wamv_controller')

        max_thrust = 2780.29  # ((x_u + x_uu * max_velocity) * max_velocity)/2

        # PID with proper output saturation
        self.pid_surge = PIDController(kp=130.0, ki=0.0, kd=0.0, output_limits=(-max_thrust, max_thrust))
        self.pid_yaw = PIDController(kp=75.0, ki=0.1, kd=5.0, output_limits=(-max_thrust, max_thrust))

        self.dt = 0.1  # Control timestep in seconds
        self.timer = self.create_timer(self.dt, self.update)

        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # Publishers for thruster control
        self.left_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
        self.left_angle_pub = self.create_publisher(Float64, '/wamv/left/thruster/joint/cmd_pos', 10)
        self.right_angle_pub = self.create_publisher(Float64, '/wamv/right/thruster/joint/cmd_pos', 10)
        self.enable_left_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/left_engine_propeller_joint/enable_deadband', 100)
        self.enable_right_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 100)
        
        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_left_deadband_pub.publish(deadband_msg)
        self.enable_right_deadband_pub.publish(deadband_msg)
       
        self.target_linear = 0.0
        self.target_angular = 0.0

    def cmd_vel_callback(self, msg):
        self.target_linear = msg.linear.x
        self.target_angular = msg.angular.z

    def update(self):
        # Assume current speed is zero (for simplicity), so error = target
        thrust_cmd = self.pid_surge.compute(self.target_linear, self.dt)
        yaw_cmd = self.pid_yaw.compute(self.target_angular, self.dt)

        # Thruster logic (simple differential thrust model)
        left_thrust = thrust_cmd - yaw_cmd
        right_thrust = thrust_cmd + yaw_cmd

        self.left_thrust_pub.publish(Float64(data=left_thrust))
        self.right_thrust_pub.publish(Float64(data=right_thrust))

        # Set angles straight (can be adjusted for curved steering if needed)
        self.left_angle_pub.publish(Float64(data=0.0))
        self.right_angle_pub.publish(Float64(data=0.0))

def main(args=None):
    rclpy.init(args=args)
    node = WamvController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()