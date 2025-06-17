import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, Bool

class ThrusterController(Node):
    def __init__(self):
        super().__init__('thruster_controller')
        
        self.declare_parameter("topic_name","/joint_states")
        name_of_topic = self.get_parameter("topic_name").get_parameter_value().string_value

        self.pub = self.create_subscription(JointState, name_of_topic, self.msg_callback, 100)
        
        # Publishers
        self.left_thrust_pub = self.create_publisher(Float64, 
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 100)
        self.right_thrust_pub = self.create_publisher(Float64,
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 100)
        self.left_angle_pub = self.create_publisher(Float64,
            '/wamv/left/thruster/joint/cmd_pos', 100)
        self.right_angle_pub = self.create_publisher(Float64,
            '/wamv/right/thruster/joint/cmd_pos', 100)
        self.enable_deadband_pub = self.create_publisher(Bool,
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 100)
        
        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_deadband_pub.publish(deadband_msg)

    def msg_callback(self, msg):
        try:
            # Estrai i valori 
            left_angle = msg.position[0]
            left_thrust = msg.position[1]
            right_angle = msg.position[2]
            right_thrust = msg.position[3]
            
            # Pubblica i valori
            self.publish_thruster_command(left_angle, left_thrust, right_angle, right_thrust)
            
        except IndexError:
            self.get_logger().error("Formato joint_states non valido!")

    def publish_thruster_command(self, left_angle, left_thrust, right_angle, right_thrust):

        self.left_thrust_pub.publish(Float64(data=left_thrust))
        self.right_thrust_pub.publish(Float64(data=right_thrust))
        
        self.left_angle_pub.publish(Float64(data=left_angle))
        self.right_angle_pub.publish(Float64(data=right_angle))
        
        # self.get_logger().debug(f"Comandi inviati: L_thrust={left_thrust}, R_thrust={right_thrust}, L_angle={left_angle}, R_angle={right_angle}")

def main(args=None):
    rclpy.init(args=args)
    controller = ThrusterController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()