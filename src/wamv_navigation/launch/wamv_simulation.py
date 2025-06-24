# Navigating with the WAM-V using a map of the environment.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('wamv_gazebo')
    pkg_navigation = get_package_share_directory('wamv_navigation')

    urdf_model_path = os.path.join(pkg_gazebo, 'urdf', 'model.urdf.xacro')
    world_path = os.path.join(pkg_gazebo, 'worlds', 'sydney.sdf')
    rviz_config_path = os.path.join(pkg_navigation, 'rviz', 'wamv_navigation.rviz')

    if not os.path.exists(urdf_model_path):
        raise FileNotFoundError(f'Urdf file not found at: {urdf_model_path}')
    if not os.path.exists(world_path):
        raise FileNotFoundError(f'World file not found at: {world_path}')
    if not os.path.exists(rviz_config_path):
        raise FileNotFoundError(f'Rviz config file not found at: {rviz_config_path}')
    
    sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time', 
        default_value='True', 
        description='Flag to enable use_sim_time'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_model_path]),
            'publish_frequency': 20.0, 
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '0', '-r', world_path],
        output='screen'
    )

    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-topic', '/robot_description',
            '-name', 'wamv',
            '-x', '0.0', '-y', '0.0', '-z', '0.2',
            '--wait', '5'  
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
        
            # GZ -> ROS
            '/model/wamv/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/world/sydney/dynamic_pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/world/sydney/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/fix@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',
            '/world/sydney/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/model/wamv/joint/left_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',

            # ROS -> GZ
            '/wamv/left/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
            '/wamv/right/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/wamv/joint/left_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',
            '/robot_description@std_msgs/msg/String]gz.msgs.StringMsg',
            '/odometry/filtered@nav_msgs/msg/Odometry]gz.msgs.OdometryWithCovariance'
        ],
        remappings=[('/fix', '/gps/fix')],
        output='screen'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg_gazebo, 'config/ekf.yaml'),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        output='screen'
    )

    wamv_controller = Node(
        package='python_node',
        executable='wamv_controller', 
        name='wamv_controller',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    rviz_node = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + rviz_config_path],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            nav2_bringup_dir + '/launch/bringup_launch.py'
        ]),
        launch_arguments={
            'use_sim_time': 'True',
            'map': pkg_navigation+'/maps/sydney_map.yaml',
            'params_file': pkg_navigation+'/params/wamv_nav2_params.yaml'  
        }.items()
    )
    
    rviz_node = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + rviz_config_path],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    coast_follower = Node(
        package='python_node',
        executable='coast_follower', 
        name='coast_follower',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    delayed_nav2_bringup = TimerAction(
        period=10.0,
        actions=[nav2_launch,
                 rviz_node,
                 coast_follower]
    )

    return LaunchDescription([
        sim_time_arg,
        bridge,
        robot_state_publisher,
        static_tf_node,
        gz_sim,
        spawn_entity,
        robot_localization_node,
        wamv_controller,
        delayed_nav2_bringup
    ])
