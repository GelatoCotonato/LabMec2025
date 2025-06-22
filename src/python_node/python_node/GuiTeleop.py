# This node receives joint states from the Joint State Publisher GUI and publishes the 
# individual values of each joint.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, Bool

class GuiTeleop(Node):
    def __init__(self):
        super().__init__('gui_teleop')
        
        # Defining subscriber
        self.declare_parameter("topic_name","/joint_states")
        name_of_topic = self.get_parameter("topic_name").get_parameter_value().string_value
        self.pub = self.create_subscription(JointState, name_of_topic, self.msg_callback, 100)
        
        # Defining publishers
        self.left_thrust_pub = self.create_publisher(Float64, 
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 100)
        self.right_thrust_pub = self.create_publisher(Float64,
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 100)
        self.left_angle_pub = self.create_publisher(Float64,
            '/wamv/left/thruster/joint/cmd_pos', 100)
        self.right_angle_pub = self.create_publisher(Float64,
            '/wamv/right/thruster/joint/cmd_pos', 100)
        self.enable_left_deadband_pub = self.create_publisher(Bool,
            '/model/wamv/joint/left_engine_propeller_joint/enable_deadband', 1)
        self.enable_right_deadband_pub = self.create_publisher(Bool,
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 1)
        
        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_left_deadband_pub.publish(deadband_msg)
        self.enable_right_deadband_pub.publish(deadband_msg)

    def msg_callback(self, msg):
        try:
            # Extracting the values
            left_angle = msg.position[0]
            left_thrust = msg.position[1]
            right_angle = msg.position[2]
            right_thrust = msg.position[3]
            
            # Publishing topics
            self.publish_thruster_command(left_angle, left_thrust, right_angle, right_thrust)       
        except IndexError:
            self.get_logger().error("Formato joint_states non valido!")

    def publish_thruster_command(self, left_angle, left_thrust, right_angle, right_thrust):

        self.left_thrust_pub.publish(Float64(data=left_thrust))
        self.right_thrust_pub.publish(Float64(data=right_thrust))
        
        self.left_angle_pub.publish(Float64(data=left_angle))
        self.right_angle_pub.publish(Float64(data=right_angle))
        

def main(args=None):
    rclpy.init(args=args)
    controller = GuiTeleop()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()