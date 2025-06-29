import rclpy
from python_node.PIDController import PIDController
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Bool
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
import numpy as np

class WamvController(Node):
    def __init__(self):
        super().__init__('wamv_controller')

        # Parametri configurabili
        self.declare_parameter('deadzone_threshold', 10.0)  # Soglia minima di spinta
        self.declare_parameter('smoothing_factor', 0.7)     # Fattore di smoothing
        self.declare_parameter('min_thrust', 5.0)           # Forza minima applicabile
        self.declare_parameter('error_deadzone', 0.02)      # Deadzone per l'errore di velocità
        self.declare_parameter('max_integral', 100.0)       # Limite anti-windup
        
        # Stato interno
        self.filtered_left_thrust = 0.0
        self.filtered_right_thrust = 0.0
        self.last_target_nonzero = False

        # Massima spinta
        max_thrust = 2780.29  # [N]

        # Controllori PID con anti-windup
        self.pid_surge = PIDController(
            kp=400.0, 
            ki=140.0, 
            kd=10.0, 
            output_limits=(-max_thrust, max_thrust))
        self.pid_yaw = PIDController(
            kp=50.0, 
            ki=0.01, 
            kd=40.0, 
            output_limits=(-max_thrust, max_thrust))

        # Timestep di controllo
        self.dt = 0.1
        self.timer = self.create_timer(self.dt, self.update)

        # Subscribers
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odometry/filtered', self.odom_callback, 10)

        # Publishers
        self.joint_states_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.left_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_thrust_pub = self.create_publisher(Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
        self.left_angle_pub = self.create_publisher(Float64, '/wamv/left/thruster/joint/cmd_pos', 10)
        self.right_angle_pub = self.create_publisher(Float64, '/wamv/right/thruster/joint/cmd_pos', 10)
        self.enable_left_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/left_engine_propeller_joint/enable_deadband', 1)
        self.enable_right_deadband_pub = self.create_publisher(Bool, '/model/wamv/joint/right_engine_propeller_joint/enable_deadband', 1)

        # Abilita deadzone integrata e resetta angoli
        deadband_msg = Bool()
        deadband_msg.data = True
        self.enable_left_deadband_pub.publish(deadband_msg)
        self.enable_right_deadband_pub.publish(deadband_msg)
        self.left_angle_pub.publish(Float64(data=0.0))
        self.right_angle_pub.publish(Float64(data=0.0))

        # Valori target e correnti
        self.target_linear = 0.0
        self.target_angular = 0.0
        self.current_linear = 0.0
        self.current_angular = 0.0

        # Tracciamento tempo
        self.last_time = self.get_clock().now()

    def odom_callback(self, msg):
        self.current_linear = msg.twist.twist.linear.x
        self.current_angular = msg.twist.twist.angular.z

    def cmd_vel_callback(self, msg):
        self.target_linear = msg.linear.x
        self.target_angular = msg.angular.z
        
        # Registra quando riceviamo un comando non zero
        if abs(msg.linear.x) > 0.001 or abs(msg.angular.z) > 0.001:
            self.last_target_nonzero = True
        else:
            self.last_target_nonzero = False

    def apply_deadzone(self, value, threshold):
        """Applica deadzone al valore"""
        return 0.0 if abs(value) < threshold else value

    def apply_smoothing(self, new_value, last_value, alpha):
        """Filtro esponenziale"""
        return alpha * new_value + (1.0 - alpha) * last_value

    def update(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds * 1e-9
        dt = max(dt, 0.001)  # Evita dt=0
        self.last_time = current_time

        # Recupera parametri
        deadzone_threshold = self.get_parameter('deadzone_threshold').value
        smoothing_factor = self.get_parameter('smoothing_factor').value
        min_thrust = self.get_parameter('min_thrust').value
        error_deadzone = self.get_parameter('error_deadzone').value
        max_integral = self.get_parameter('max_integral').value

        # Calcola errori con deadzone
        surge_error = self.target_linear - self.current_linear
        yaw_error = self.target_angular - self.current_angular
        
        # Applica deadzone agli errori per evitare micro-aggiustamenti
        surge_error = self.apply_deadzone(surge_error, error_deadzone)
        yaw_error = self.apply_deadzone(yaw_error, error_deadzone)

        # Calcola uscite PID
        thrust_cmd = self.pid_surge.compute(surge_error, dt)
        yaw_cmd = self.pid_yaw.compute(yaw_error, dt)
        
        # Anti-windup: limita l'integrale
        self.pid_surge.integral = np.clip(self.pid_surge.integral, -max_integral, max_integral)
        self.pid_yaw.integral = np.clip(self.pid_yaw.integral, -max_integral, max_integral)

        # Calcolo spinta grezza
        left_thrust_raw = thrust_cmd - yaw_cmd
        right_thrust_raw = thrust_cmd + yaw_cmd

        # Applica deadzone
        left_thrust = self.apply_deadzone(left_thrust_raw, deadzone_threshold)
        right_thrust = self.apply_deadzone(right_thrust_raw, deadzone_threshold)

        # Filtraggio
        self.filtered_left_thrust = self.apply_smoothing(
            left_thrust, self.filtered_left_thrust, smoothing_factor)
        self.filtered_right_thrust = self.apply_smoothing(
            right_thrust, self.filtered_right_thrust, smoothing_factor)

        # Elimina micro-spinte
        if abs(self.filtered_left_thrust) < min_thrust:
            left_thrust_final = 0.0
        else:
            left_thrust_final = self.filtered_left_thrust
            
        if abs(self.filtered_right_thrust) < min_thrust:
            right_thrust_final = 0.0
        else:
            right_thrust_final = self.filtered_right_thrust

        # Reset completo quando non c'è movimento richiesto
        if not self.last_target_nonzero and abs(self.current_linear) < 0.01 and abs(self.current_angular) < 0.01:
            left_thrust_final = 0.0
            right_thrust_final = 0.0
            self.pid_surge.reset()
            self.pid_yaw.reset()
            self.filtered_left_thrust = 0.0
            self.filtered_right_thrust = 0.0

        # Pubblica i comandi
        self.left_thrust_pub.publish(Float64(data=left_thrust_final))
        self.right_thrust_pub.publish(Float64(data=right_thrust_final))
        
        # Pubblica stati giunto (solo per visualizzazione)
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [
            'left_chassis_engine_joint',
            'left_engine_propeller_joint',
            'right_chassis_engine_joint',
            'right_engine_propeller_joint'
        ]
        js.position = [0.0, left_thrust_final, 0.0, right_thrust_final]
        self.joint_states_pub.publish(js)
        
        # Log di debug
        self.get_logger().debug(
            f"Thrust: L={left_thrust_final:.1f}, R={right_thrust_final:.1f} | "
            f"Target: lin={self.target_linear:.2f}, ang={self.target_angular:.2f} | "
            f"Current: lin={self.current_linear:.2f}, ang={self.current_angular:.2f}",
            throttle_duration_sec=1.0
        )

def main(args=None):
    rclpy.init(args=args)
    node = WamvController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()