import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import select

settings = termios.tcgetattr(sys.stdin)

class KeyboardTeleop(Node):

    def __init__(self, name='python_publisher'):
        super().__init__(node_name=name)

        self.count = 0
        self.count_reset = 100

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Valori correnti iniziali
        self.linear_x = 0.0
        self.angular_z = 0.0

        # Passi di incremento/decremento
        self.linear_step = 0.2   # velocità incrementa o decrementa di 0.05 m/s
        self.angular_step = 0.1   # angolo incrementa o decrementa di 0.1 rad

        self.max_linear = 1.0    # max velocità (m/s)
        self.min_linear = -1.0    # min velocità

        self.max_angular = 0.7    # max angolo (rad)
        self.min_angular = -0.7   # min angolo

        self.declare_parameter("timer_period", 0.1)
        self.period = self.get_parameter("timer_period").get_parameter_value().double_value
        self.timer = self.create_timer(self.period, self.listen_to_keyboard)

        self.get_logger().info("Keyboard to /cmd_vel ready. Use W/A/S/D to change velocity and angle. X to reset. Q to quit.")

    def listen_to_keyboard(self):
        key = get_key()

        if key == 'w':
            self.linear_x += self.linear_step
        elif key == 's':
            self.linear_x -= self.linear_step
        elif key == 'd':
            self.angular_z -= self.angular_step
        elif key == 'a':
            self.angular_z += self.angular_step
        elif key == 'x':
            self.linear_x = 0.0
            self.angular_z = 0.0
        elif key == 'q':
            self.destroy_node()
            rclpy.shutdown()
            return
        elif key == '\x03':  # Ctrl+C
            self.destroy_node()
            rclpy.shutdown()
            return

        # Limita valori
        self.linear_x = max(min(self.linear_x, self.max_linear), self.min_linear)
        self.angular_z = max(min(self.angular_z, self.max_angular), self.min_angular)

        twist_msg = Twist()
        twist_msg.linear.x = self.linear_x
        twist_msg.angular.z = self.angular_z

        self.cmd_vel_pub.publish(twist_msg)

        self.count = self.count + 1
        if self.count >= self.count_reset:
            self.get_logger().info(f"cmd_vel published: v_x={self.linear_x:.2f}, z_angle={self.angular_z:.2f}")
            self.count = 0
 
def get_key():
    try:
        tty.setraw(sys.stdin.fileno())  
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  # Timeout di 0.1 secondi
        if rlist:
            key = sys.stdin.read(1)  # Legge 1 carattere
        else:
            key = ''
    finally:
        # Ripristina le impostazioni del terminale in caso di errore
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
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