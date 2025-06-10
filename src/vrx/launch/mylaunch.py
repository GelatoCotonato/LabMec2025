
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription, LaunchService
from bridge import Bridge, BridgeDirection

def lidar_scan(world_name, model_name, link_name, sensor_name):
    gz_sensor_prefix="/lidar"
    ros_sensor_prefix="/lidar_ros"
    return Bridge(
        gz_topic=f'{gz_sensor_prefix}/scan',
        ros_topic=f'{ros_sensor_prefix}/scan',
        gz_type='gz.msgs.LaserScan',
        ros_type='sensor_msgs/msg/LaserScan',
        direction=BridgeDirection.GZ_TO_ROS)


def lidar_points(world_name, model_name, link_name, sensor_name):

    gz_sensor_prefix="/lidar"
    ros_sensor_prefix="/lidar_ros"

    return Bridge(
        gz_topic=f'{gz_sensor_prefix}/scan/points',
        ros_topic=f'{ros_sensor_prefix}/scan/points',
        gz_type='gz.msgs.PointCloudPacked',
        ros_type='sensor_msgs/msg/PointCloud2',
        direction=BridgeDirection.GZ_TO_ROS)

def generate_launch_description(world_name, ign_flag=True):
    # Get the full path to the world file
    world_path = os.path.join(
        get_package_share_directory("vrx"),
        "worlds",
        f"{world_name}.sdf"
    )

    # Verify the world file exists
    if not os.path.exists(world_path):
        raise FileNotFoundError(f"World file not found at: {world_path}")

    # Build the Gazebo command arguments
    gz_args = ["gz", "sim"]
    gz_args = []
    if ign_flag:
        gz_args.extend(["-v", "0", "-r"])  # Using verbosity level 4 for Ignition Gazebo

    gz_args.extend([world_path])

    gz_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'),
                '/gz_sim.launch.py']),
            launch_arguments={'gz_args': ' '.join(gz_args)}.items())

    # Create the ExecuteProcess action
    # subprocess.run(gz_args,check=True)

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='dynamic_bridge',
        arguments=['/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                   '/lidar/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked'
                   ],
        output='screen'
    )

    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0', '0', '0', '0', '0', '0',  
            'lidar_link',                   
            'wamv/lidar_link/gpu_lidar' 
        ],
        output='screen'
    )

    return LaunchDescription([gz_sim, bridge_node, static_tf])

if __name__ == '__main__':

    world_name = "sydney"
    ld = generate_launch_description(world_name)
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()