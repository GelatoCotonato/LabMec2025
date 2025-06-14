import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import ThisLaunchFileDir
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():

    world_name="sydney"
    ign_flag = True
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

    # static_tf = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments=[
    #         '0', '0', '0', '0', '0', '0',  
    #         'lidar_link',                   
    #         'wamv/lidar_link/gpu_lidar' 
    #     ],
    #     output='screen'
    # )

    # UPLOAD WAMV PARAMS
    wamv_param_dir = LaunchConfiguration(
        'wamv_param_dir',
        default=os.path.join(
            get_package_share_directory('wamv_navigation'),
            'param','wamv_config.yaml'))


    # # UPLOAD WAMV PARAMS
    # tb3_param_dir = LaunchConfiguration(
    #     'tb3_param_dir',
    #     default=os.path.join(
    #         get_package_share_directory('turtlebot3_bringup'),
    #         'param',
    #         TURTLEBOT3_MODEL + '.yaml'))

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([ gz_sim, bridge_node,
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='Use simulation (Gazebo) clock if true'),

        DeclareLaunchArgument(
            'wamv_param_dir',
            default_value=wamv_param_dir,
            description='Full path to wam-v parameter file to load')


        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         [ThisLaunchFileDir(), '/turtlebot3_state_publisher.launch.py']),
        #     launch_arguments={'use_sim_time': use_sim_time,
        #                       'namespace': namespace}.items(),
        # ),

        # Node(
        #     package='turtlebot3_node',
        #     executable='turtlebot3_ros',
        #     parameters=[
        #         tb3_param_dir,
        #         {'namespace': namespace}],
        #     arguments=['-i', usb_port],
        #     output='screen'),
    ])
