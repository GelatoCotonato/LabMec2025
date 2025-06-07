import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LidarNode(Node):
    def __init__(self,name='lidar_subscriber'):
        super().__init__(node_name=name)

        # Parametro topic lidar (default "lidar_topic")
        self.declare_parameter("topic_name","lidar_topic")
        self.declare_parameter("message", "LIDTOPIC")
        name_of_topic = self.get_parameter("topic_name").get_parameter_value().string_value
        self.message = self.get_parameter("message").get_parameter_value().string_value
        # Subscriber al topic lidar
        self.sub = self.create_subscription(LaserScan,name_of_topic,self.msg_callback,10)

        # Publisher cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info(f"Subscribed to LIDAR topic: {name_of_topic}")

    def msg_callback(self, msg: LaserScan):
        self.get_logger().info(f"Subscribed to LIDAR topic: {self.message}")
        # msg.ranges è la lista delle distanze
        all_more = all(r > 1.0 for r in msg.ranges if r > 0.0)  # Ignora 0.0 se sono valori invalidi

        cmd = Twist()
        if all_more:
            cmd.linear.x = 0.5
            cmd.angular.z = 0.0
            self.get_logger().info("Path clear, moving forward")
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
            self.get_logger().info("Obstacle detected, turning")

        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = LidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()