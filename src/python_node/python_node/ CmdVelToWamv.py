import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class CmdVelToWamv(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_wamv')
        
        # Parametri regolabili
        self.declare_parameters(namespace='',
            parameters=[
                ('max_thrust', 100.0),  # Massima spinta in N
                ('max_angle', 0.785),   # Angolo massimo thruster (45°)
                ('linear_gain', 1.0),   # Guadagno per velocità lineare
                ('angular_gain', 1.0)   # Guadagno per velocità angolare
            ])
        
        # Subscriber a /cmd_vel (da Nav2)
        self.sub = self.create_subscription(
            Twist, '/cmd_vel', self.convert, 10)
        
        # Publisher per Gazebo
        self.left_angle_pub = self.create_publisher(
            Float64, '/wamv/left/thruster/joint/cmd_pos', 10)
        self.right_angle_pub = self.create_publisher(
            Float64, '/wamv/right/thruster/joint/cmd_pos', 10)
        self.left_thrust_pub = self.create_publisher(
            Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_thrust_pub = self.create_publisher(
            Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
    
    def convert(self, msg):
        # Recupera parametri
        max_thrust = self.get_parameter('max_thrust').value
        max_angle = self.get_parameter('max_angle').value
        linear_gain = self.get_parameter('linear_gain').value
        angular_gain = self.get_parameter('angular_gain').value
        
        # Calcola angoli thruster (sterzo)
        angle = Float64()
        angle.data = max_angle * angular_gain * msg.angular.z
        
        # Calcola spinta base
        base_thrust = max_thrust * linear_gain * msg.linear.x
        
        # Applica modello differenziale
        left_thrust = Float64()
        right_thrust = Float64()
        left_thrust.data = base_thrust - (0.5 * base_thrust * msg.angular.z)
        right_thrust.data = base_thrust + (0.5 * base_thrust * msg.angular.z)
        
        # Pubblica i comandi
        self.left_angle_pub.publish(angle)
        self.right_angle_pub.publish(angle)
        self.left_thrust_pub.publish(left_thrust)
        self.right_thrust_pub.publish(right_thrust)

def main():
    rclpy.init()
    node = CmdVelToWamv()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()