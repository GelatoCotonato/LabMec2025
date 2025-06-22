# This node captures keyboard input and sends the corresponding velocity commands to the /cmd_vel topic.

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, termios, tty, select

settings = termios.tcgetattr(sys.stdin)

class KeyboardTeleop(Node):

    def __init__(self, name='keyboard_teleop'):
        super().__init__(node_name=name)

        # Counter variable used to periodically print the current velocity values to the terminal
        self.count = 0
        self.count_reset = 100

        # Defining /cmd_vel publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Initial values of linear and angular velocities
        self.linear_x = 0.0  # [m/s]
        self.angular_z = 0.0 # [rad/s]

        # Incremental steps for linear and angular velocities
        self.linear_step = 0.2  
        self.angular_step = 0.1 

        # Maximum and minimum values of velocities
        self.max_linear = 1.0    
        self.min_linear = -1.0   
        self.max_angular = 0.7   
        self.min_angular = -0.7  

        # Defining timer for the user command input
        self.declare_parameter("timer_period", 0.1)
        self.period = self.get_parameter("timer_period").get_parameter_value().double_value
        self.timer = self.create_timer(self.period, self.listen_to_keyboard)

        self.get_logger().info("Keyboard to /cmd_vel ready. Use W/A/S/D to change velocity and angle. X to reset. Q to quit.")

    def listen_to_keyboard(self):

        # Getting the key command
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

        self.linear_x = max(min(self.linear_x, self.max_linear), self.min_linear)
        self.angular_z = max(min(self.angular_z, self.max_angular), self.min_angular)

        # Building the message
        twist_msg = Twist()
        twist_msg.linear.x = self.linear_x
        twist_msg.angular.z = self.angular_z

        # Publishing the topic
        self.cmd_vel_pub.publish(twist_msg)

        self.count = self.count + 1
        if self.count >= self.count_reset:
            self.get_logger().info(f"cmd_vel published: v_x={self.linear_x:.2f}, z_angle={self.angular_z:.2f}")
            self.count = 0
 
def get_key():
    try:
        tty.setraw(sys.stdin.fileno())
        # Timeout of 0.1 second
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1) 
        if rlist:
            # Reading one char
            key = sys.stdin.read(1)  
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