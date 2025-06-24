# This node receives velocity commands and computes thrust values and joint states using PID controllers

import rclpy
from python_node.PIDController import PIDController
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Bool
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState

class WamvController(Node):
    def __init__(self):
        super().__init__('wamv_controller')

        # Maximum thrust value
        max_thrust = 30*2780.29  # [N]

        # PID with proper output saturation
        self.pid_surge = PIDController(kp=400.0, ki = 150, kd=10.0, output_limits=(-max_thrust, max_thrust))
        self.pid_yaw = PIDController(kp=50.0, ki = 0.01, kd= 40.0, output_limits=(-max_thrust, max_thrust))

        # Control timestep
        self.dt = 0.1 # [s]
        self.timer = self.create_timer(self.dt, self.update)

        # Defining subscribers to get reference signal and feedback respectively
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odometry/filtered', self.odom_callback, 10)

        # Defining publishers for thruster control
        self.joint_states_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.left_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
        self.left_angle_pub = self.create_publisher(Float64, '/wamv/left/thruster/joint/cmd_pos', 10)
        self.right_angle_pub = self.create_publisher(Float64, '/wamv/right/thruster/joint/cmd_pos', 10)
        self.enable_left_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/left_engine_propeller_joint/enable_deadband', 1)
        self.enable_right_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 1)

        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_left_deadband_pub.publish(deadband_msg)
        self.enable_right_deadband_pub.publish(deadband_msg)
        self.left_angle_pub.publish(Float64(data=0.0))
        self.right_angle_pub.publish(Float64(data=0.0))

        # Target values
        self.target_linear = 0.0
        self.target_angular = 0.0

        # Current values
        self.current_linear = 0.0
        self.current_angular = 0.0

    def odom_callback(self, msg):
        self.current_linear = msg.twist.twist.linear.x
        self.current_angular = msg.twist.twist.angular.z

    def cmd_vel_callback(self, msg):
        self.target_linear = msg.linear.x
        self.target_angular = msg.angular.z

    def update(self):

        # Getting velocity errors
        surge_error = self.target_linear - self.current_linear
        yaw_error = self.target_angular - self.current_angular
    
        # Computing control inputs
        thrust_cmd = self.pid_surge.compute(surge_error, self.dt)
        yaw_cmd = self.pid_yaw.compute(yaw_error, self.dt)
        left_thrust = thrust_cmd - yaw_cmd
        right_thrust = thrust_cmd + yaw_cmd

        # Getting JointState message
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name =  ['left_chassis_engine_joint',
                    'left_engine_propeller_joint',
                    'right_chassis_engine_joint',
                    'right_engine_propeller_joint']
        js.position = [
            0.0,
            left_thrust,
            0.0,
            right_thrust
        ]

        # Publishing thrust values and joint states
        self.left_thrust_pub.publish(Float64(data=left_thrust))
        self.right_thrust_pub.publish(Float64(data=right_thrust))   
        self.joint_states_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = WamvController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()