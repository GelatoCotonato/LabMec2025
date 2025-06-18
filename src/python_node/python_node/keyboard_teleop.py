import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import sys
import termios
import tty
import select

settings = termios.tcgetattr(sys.stdin)

class PythonPublisher(Node):

    def __init__(self, name='python_publisher'):
        super().__init__(node_name=name)

        self.left_thrust_pub = self.create_publisher(Float64,
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_thrust_pub = self.create_publisher(Float64,
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
        self.left_angle_pub = self.create_publisher(Float64,
            '/wamv/left/thruster/joint/cmd_pos', 10)
        self.right_angle_pub = self.create_publisher(Float64,
            '/wamv/right/thruster/joint/cmd_pos', 10)
        self.enable_deadband_pub = self.create_publisher(Bool,
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 10)
        self.joint_states_pub = self.create_publisher(JointState,
            '/joint_states', 10)
        
        # Initial values
        self.thrust = 0.0
        self.angle = 0.0

        self.joint_names = ['left_chassis_engine_joint', 'left_engine_propeller_joint',
                            'right_chassis_engine_joint', 'right_engine_propeller_joint']
        self.i=0

        self.declare_parameter("timer_period",0.1)
        self.period = self.get_parameter("timer_period").get_parameter_value().double_value
        self.timer = self.create_timer(self.period, self.listen_to_keyboard)

        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_deadband_pub.publish(deadband_msg)
        self.get_logger().info("Keyboard controller ready. Use W/A/S/D to move. Q to quit.")

    def listen_to_keyboard(self):
        self.i=self.i+1
        key = get_key()

        if key == 'w':
            self.thrust += 1
        elif key == 's':
            self.thrust -= 1
        elif key == 'x':
            self.thrust = 0.0
        elif key == 'a':
            self.angle -= 0.1
        elif key == 'd':
            self.angle += 0.1
        elif key == 'q':
            self.angle = 0.5  # sharp left
        elif key == 'e':
            self.angle = -0.5  # sharp right
        elif key == 'z':
            self.angle = 0.0
        elif key == '\x03':  # Ctrl+C
            self.destroy_node()
            rclpy.shutdown()
            return

        # Clamp values
        self.thrust = max(min(self.thrust, 100.0), -100.0)
        self.angle = max(min(self.angle, 1.57), -1.57)

        # Publish values
        thrust_msg = Float64()
        thrust_msg.data = self.thrust

        angle_msg = Float64()
        angle_msg.data = self.angle

        self.left_thrust_pub.publish(thrust_msg)
        self.right_thrust_pub.publish(thrust_msg)
        self.left_angle_pub.publish(angle_msg)
        self.right_angle_pub.publish(angle_msg)

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        angle_l = self.angle       
        thrust_l = self.thrust
        angle_r = self.angle   
        thrust_r = self.thrust
        msg.position = [angle_l, thrust_l, angle_r, thrust_r]
        self.joint_states_pub.publish(msg)

        if self.i>100:
            self.get_logger().info(f"Thrust: {self.thrust:.2f}, Angle: {self.angle:.2f}")
            self.i=0


def get_key():
    try:
        tty.setraw(sys.stdin.fileno())  # Imposta il terminale in modalità raw (nessun buffering)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  # Timeout di 0.1 secondi
        if rlist:
            key = sys.stdin.read(1)  # Legge 1 carattere
        else:
            key = ''
    finally:
        # Ripristina le impostazioni del terminale anche in caso di errore
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    rclpy.init(args=args)
    node = PythonPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down.")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()