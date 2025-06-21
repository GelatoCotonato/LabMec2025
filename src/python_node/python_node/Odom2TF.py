import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster

# Subsiption on the topic odom 
class Odom2TF(Node):


    def __init__(self,name='odom2tf'):
        super().__init__(name)
        
        self.br = TransformBroadcaster(self) # Pubblica automaticamente su /tf e /tf_static
        self.subscription = self.create_subscription(Odometry,'/odom',self.odom_callback,10)

    def odom_callback(self, msg):
        t = TransformStamped()
        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = Odom2TF()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()