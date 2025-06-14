import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster

# Subsiption on the topic odom 
class OdomToTF(Node):


    def __init__(self,name='odom_to_tf'):
        super().__init__(node_name=name)

        self.br = TransformBroadcaster(self) # Pubblica automaticamente su /tf e /tf_static
        self.subscription = self.create_subscription(Odometry,'/odom',self.odom_callback,100)

    def odom_callback(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg() 
        t.header.frame_id = 'odom' 
        t.child_frame_id = 'base_link'
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = OdomToTF()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()