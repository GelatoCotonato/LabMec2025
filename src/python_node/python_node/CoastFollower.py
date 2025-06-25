# This node receive the LaserScan data from the Lidar and Odometry data from /odometry/filtered topic in order to 
# find the next waypoint to move to. The waypoint is then transmitted to Nav2.

import math, rclpy, PyKDL
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from python_node.RLS import RLS
from threading import Lock
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Quaternion

class CoastFollower(Node):
    def __init__(self):
        super().__init__('lidar_node')
        
        # Lock to prevent simultaneous access to critical data
        self.lock = Lock()

        # Defining Recursive Least Square Estimator
        self.rls = RLS(mu=1.0, sigma=10000.0)

        # Flag to allow to Recursive Least Square Estimator to have a good estimate of the coast
        self.first_skip = True

        # Starting values for the coast line: y = m x + b
        self.m = 0
        self.b = 50

        # Distance from the coast line
        self.d = 60.0 # [m]

        # Distance from the WAM-V
        self.k = 10.0 # [m]

        # Waypoint transmission timing
        way_time = 10.0; # [s]

        # WAM-V pose
        self.rob_posx = 0.0
        self.rob_posy = 0.0
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = 0.0
        q.w = 1.0
        self.rob_orientation = q
        self.rob_yaw = 0.0

        # Defining subscribers
        self.sub_odom = self.create_subscription(Odometry,'/odometry/filtered',self.odom_callback,10)
        self.sub_lidar = self.create_subscription(LaserScan,'/scan',self.scan_callback,10)

        # In order to transmit the waypoint to Nav2
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Setting timer for waypoint update
        self.timer = self.create_timer(way_time, self.update_goal)

    def odom_callback(self, msg):
        # Getting odometry data
        with self.lock:
            self.rob_posx = msg.pose.pose.position.x
            self.rob_posy = msg.pose.pose.position.y
            self.rob_orientation = msg.pose.pose.orientation
            self.rob_yaw = self.quaternion_to_yaw(msg.pose.pose.orientation)

    def quaternion_to_yaw(self, q):
        rot = PyKDL.Rotation.Quaternion(q.x, q.y, q.z, q.w)
        return rot.GetRPY()[2]  
    
    def scan_callback(self, msg):
        with self.lock:
            # Process Lidar data
            angle_min = msg.angle_min
            angle_increment = msg.angle_increment
            
            coast_points = []

            for i, distance in enumerate(msg.ranges):
                if math.isinf(distance):
                    continue
                
                # Getting obstacle data in the robot frame
                angle = angle_min + i * angle_increment
                x_obs = distance * math.cos(angle)
                y_obs = distance * math.sin(angle)
                
                # Getting obstacle data in the map frame
                x_world = self.rob_posx + x_obs * math.cos(self.rob_yaw) - y_obs * math.sin(-self.rob_yaw)
                y_world = self.rob_posy + x_obs * math.sin(-self.rob_yaw) + y_obs * math.cos(self.rob_yaw)
                
                # To prevent taking points too close to the coast
                if y_world > 35:
                    coast_points.append([x_world, y_world])
                
            if len(coast_points) > 0:
                # Getting the nearest point of the coast
                min_point = min(coast_points, key=lambda p: p[1])

                # Update of the estimate
                self.rls.update(min_point[0], min_point[1])
                self.m, self.b = self.rls.get_params()
                # # Printing data
                # self.get_logger().info(f"Stima RLS: y = {self.m:.3f} * x + {self.b:.3f}")

    def update_goal(self):
        
        if self.first_skip:
            self.first_skip = False
            return
        
        with self.lock:

            # Finding a parallel line to the coast line: y = m x + b_p
            b_p = self.b - self.d * math.sqrt(1+self.m**2) 

            # Finding the next waypoint
            x_way = self.rob_posx + self.k/math.sqrt(1+self.m**2)
            y_way = self.m*x_way + b_p
            # # Printing data
            #self.get_logger().info(f"Invio goal: x_way={x_way:.2f}, y_way={y_way:.2f}")

            # Sending waypoint
            self.send_goal(x_way, y_way)

    def send_goal(self, x, y):

        goal_yaw = 0
        yaw_rad = math.radians(goal_yaw)
        qz = math.sin(yaw_rad / 2.0)
        qw = math.cos(yaw_rad / 2.0)

        # Building the message
        goal_msg = NavigateToPose.Goal()
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.get_clock().now().to_msg()
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.z = qz
        goal_pose.pose.orientation.w = qw
        goal_msg.pose = goal_pose

        # Waypoint uploading
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