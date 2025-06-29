#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool
from nav_msgs.msg import Odometry

class ThrusterGuardian(Node):
    def __init__(self):
        super().__init__('thruster_guardian')
        
        # Soglie di velocità per considerare fermo il robot
        self.declare_parameter('velocity_threshold', 0.01)  # m/s
        self.declare_parameter('angular_threshold', 0.01)   # rad/s
        
        # Sottoscrittori
        self.odom_sub = self.create_subscription(
            Odometry, 
            '/odometry/filtered', 
            self.odom_callback, 
            10
        )
        
        # Pubblicatori (sovrascrivono i comandi)
        self.left_thrust_pub = self.create_publisher(
            Float64, 
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 
            10
        )
        self.right_thrust_pub = self.create_publisher(
            Float64, 
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 
            10
        )
        
        # Stato
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.last_movement_time = self.get_clock().now()
        
        # Timer di controllo
        self.timer = self.create_timer(0.1, self.monitor_and_control)
    
    def odom_callback(self, msg):
        self.current_linear = msg.twist.twist.linear.x
        self.current_angular = msg.twist.twist.angular.z
        
        # Registra l'ultimo movimento
        vel_thresh = self.get_parameter('velocity_threshold').value
        ang_thresh = self.get_parameter('angular_threshold').value
        
        if abs(self.current_linear) > vel_thresh or abs(self.current_angular) > ang_thresh:
            self.last_movement_time = self.get_clock().now()
    
    def monitor_and_control(self):
        # Calcola tempo dall'ultimo movimento
        current_time = self.get_clock().now()
        time_since_last_move = (current_time - self.last_movement_time).nanoseconds * 1e-9
        
        # Se non c'è movimento da 2 secondi, forza le eliche a fermarsi
        if time_since_last_move > 2.0:
            self.left_thrust_pub.publish(Float64(data=0.0))
            self.right_thrust_pub.publish(Float64(data=0.0))
            self.get_logger().info('Forzato arresto eliche per inattività', throttle_duration_sec=5.0)

def main():
    rclpy.init()
    node = ThrusterGuardian()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()