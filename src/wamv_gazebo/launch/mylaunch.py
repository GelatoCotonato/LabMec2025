
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import launch.actions
import launch_ros.actions
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

def thrust_joint_pos(model_name, side):
    # ROS naming policy indicates that first character of a name must be an alpha
    # character. In the case below, the gz topic has the joint index 0 as the
    # first char so the following topics fail to be created on the ROS end
    # left_joint_topic = '/model/' + model_name + '/joint/left_chasis_engine_joint/0/cmd_pos'
    # right_joint_topic = '/model/' + model_name + '/joint/right_chasis_engine_joint/0/cmd_pos'
    # For now, use erb to generate unique topic names in model.sdf.erb
    return Bridge(
        gz_topic=f'{model_name}/thrusters/{side}/pos',
        ros_topic=f'thrusters/{side}/pos',
        gz_type='gz.msgs.Double',
        ros_type='std_msgs/msg/Float64',
        direction=BridgeDirection.ROS_TO_GZ)

def thrust(model_name, side):
    return Bridge(
        gz_topic=f'{model_name}/thrusters/{side}/thrust',
        ros_topic=f'thrusters/{side}/thrust',
        gz_type='gz.msgs.Double',
        ros_type='std_msgs/msg/Float64',
        direction=BridgeDirection.ROS_TO_GZ)

def generate_launch_description(world_name="sydney", ign_flag=True):
    # Get the full path to the world file
    world_path = os.path.join(
        get_package_share_directory("wamv_gazebo"),
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

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='dynamic_bridge',
        arguments=[
            # LIDAR topics
            '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/lidar/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',

            # Angular velocity readings
            '/model/wamv/joint/left_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',

            # Thruster angle control (ROS -> Gazebo)
            '/wamv/left/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
            '/wamv/right/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',

            # Thrust commands (ROS -> Gazebo)
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
        
            # Deadband control (ROS -> Gazebo)
            '/model/wamv/joint/left_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',
        
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

    ld = LaunchDescription([gz_sim, bridge_node, static_tf])

    # Teleop
    # parameters_file = os.path.join(
    #     get_package_share_directory('wamv_gazebo'),
    #     'config', 'wamv.yaml'
    # )
    # ld = LaunchDescription([gz_sim, bridge_node, static_tf,
    #    launch.actions.DeclareLaunchArgument('cmd_vel', default_value='cmd_vel'),
    #    launch.actions.DeclareLaunchArgument('teleop_config', default_value=parameters_file),
    # ])

    # ld.add_action(launch_ros.actions.Node(package='joy', executable='joy_node'))

    # ld.add_action(launch_ros.actions.Node(
    # package='teleop_twist_joy', executable='teleop_node',
    # parameters=[launch.substitutions.LaunchConfiguration('teleop_config')]))
    
    return ld


if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()

