import math, rclpy, PyKDL
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from python_node.RLS import RLS
from threading import Lock
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped

class CoastFollower(Node):
    def __init__(self):
        super().__init__('lidar_node')
        
        self.first_skip = True
        self.lock = Lock()
        self.sub_odom = self.create_subscription(Odometry,'/odometry/filtered',self.odom_callback,10)
        self.sub_lidar = self.create_subscription(LaserScan,'/scan',self.scan_callback,10)
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.timer = self.create_timer(10.0, self.update_goal)

        self.rls = RLS(mu=1.0, sigma=10000.0)

        self.d = 60.0
        self.k = 10.0

        self.rob_posx = 0.0
        self.rob_posy = 0.0
        self.rob_yaw = 0.0
        self.m = 0
        self.b = 50

    def odom_callback(self, msg):
        with self.lock:
            self.rob_posx = msg.pose.pose.position.x
            self.rob_posy = msg.pose.pose.position.y
            self.rob_yaw = self.quaternion_to_yaw(msg.pose.pose.orientation)

    def quaternion_to_yaw(self, q):
        rot = PyKDL.Rotation.Quaternion(q.x, q.y, q.z, q.w)
        return rot.GetRPY()[2]  
    
    def scan_callback(self, msg):
        with self.lock:
            # Process LIDAR data
            angle_min = msg.angle_min
            angle_increment = msg.angle_increment
            
            coast_points = []

            for i, distance in enumerate(msg.ranges):
                if math.isinf(distance):
                    continue
                
                # Polar to Cartesian (robot frame)
                angle = angle_min + i * angle_increment
                x_obs = distance * math.cos(angle)
                y_obs = distance * math.sin(angle)
                
                x_world = self.rob_posx + x_obs * math.cos(self.rob_yaw) - y_obs * math.sin(-self.rob_yaw)
                y_world = self.rob_posy + x_obs * math.sin(-self.rob_yaw) + y_obs * math.cos(self.rob_yaw)
                
                if y_world > 35:
                    coast_points.append([x_world, y_world])
                
            if len(coast_points) > 0:
                min_point = min(coast_points, key=lambda p: p[1])
                
                self.rls.update(min_point[0], min_point[1])
                self.m, self.b = self.rls.get_params()


                # self.get_logger().info(f"Stima RLS: y = {self.m:.3f} * x + {self.b:.3f}")

    def update_goal(self):

        if self.first_skip:
            self.first_skip = False
            return
        
        with self.lock:


            b_p = self.b - self.d * math.sqrt(1+self.m**2)


            x_way = self.rob_posx + self.k/math.sqrt(1+self.m**2)
            y_way = self.m*x_way + b_p
            # self.get_logger().info(f"Invio goal: self.rob_posx={self.rob_posx:.2f}")
            # self.get_logger().info(f"Invio goal: m={self.m:.2f}, b={self.b:.2f}")
            # self.get_logger().info(f"Invio goal: m={self.m:.2f}, b_p={b_p:.2f}")
            self.get_logger().info(f"Invio goal: x_way={x_way:.2f}, y_way={y_way:.2f}")

            self.send_goal(x_way, y_way)

    def send_goal(self, x, y):
        goal_msg = NavigateToPose.Goal()
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.get_clock().now().to_msg()

        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = 0.0

        goal_yaw = 0
        yaw_rad = math.radians(goal_yaw)
        qz = math.sin(yaw_rad / 2.0)
        qw = math.cos(yaw_rad / 2.0)

        goal_pose.pose.orientation.z = qz
        goal_pose.pose.orientation.w = qw

        goal_msg.pose = goal_pose


        self.nav_to_pose_client.wait_for_server()
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal rifiutato dal server.')
            self._current_goal_handle = None
            return

        self.get_logger().info('Goal accettato dal server.')
        self._current_goal_handle = goal_handle

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == 4:
            self.get_logger().info('Goal cancellato.')
        elif status == 3:
            self.get_logger().info('Goal raggiunto con successo.')
        else:
            self.get_logger().warn(f'Goal terminato con stato {status}.')
        self._current_goal_handle = None


def main(args=None):
    rclpy.init(args=args)
    node = CoastFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()