# Mapping 

import os, subprocess, atexit, signal
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('wamv_gazebo')
    pkg_navigation = get_package_share_directory('wamv_navigation')
    pkg_slam = get_package_share_directory('slam_toolbox')
    pkg_nav2 = get_package_share_directory('nav2_bringup')

    urdf_model_path = os.path.join(pkg_gazebo, 'urdf', 'model.urdf.xacro')
    world_path = os.path.join(pkg_gazebo, 'worlds', 'sydney.sdf')
    rviz_config_path = os.path.join(pkg_navigation, 'rviz', 'wamv_localization.rviz')

    if not os.path.exists(urdf_model_path):
        raise FileNotFoundError(f"Urdf file not found at: {urdf_model_path}")
    
    if not os.path.exists(world_path):
        raise FileNotFoundError(f"World file not found at: {world_path}")
    
    if not os.path.exists(rviz_config_path):
        raise FileNotFoundError(f"Rviz config file not found at: {rviz_config_path}")
    
    sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time', 
        default_value='True', 
        description='Flag to enable use_sim_time'
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_model_path]),
            'publish_frequency': 20.0, 
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )

    # Gazebo Sim - Nuova sintassi per ROS 2 Jazzy
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', '-r', world_path],
        output='screen'
    )

    # Spawn del modello
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-topic', '/robot_description',
            '-name', 'wamv',
            '-x', '0', '-y', '0', '-z', '0.2',
            '--wait', '5'  
        ],
        output='screen'
    )

    # Bridge per TF e sensori
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
        
            # GZ -> ROS

            # Pose Syncro
            '/model/wamv/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/world/sydney/dynamic_pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/world/sydney/pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',

            # Clock
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                                           
            # LIDAR 
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',

            # IMU 
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',

            # Odom & TF 
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',

            # GPS
            '/fix@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',

            # Clock 
            '/world/sydney/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',

            # Angular velocity 
            '/model/wamv/joint/left_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/ang_vel@std_msgs/msg/Float64[gz.msgs.Double',

            # ROS -> GZ

            # Thruster angle  
            '/wamv/left/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
            '/wamv/right/thruster/joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',

            # Thrust
            '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
        
            # Deadband
            '/model/wamv/joint/left_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',
            '/model/wamv/joint/right_engine_propeller_joint/enable_deadband@std_msgs/msg/Bool]gz.msgs.Boolean',

            '/robot_description@std_msgs/msg/String]gz.msgs.StringMsg',

            '/odometry/filtered@nav_msgs/msg/Odometry]gz.msgs.OdometryWithCovariance'
        ],
        remappings=[('/fix', '/gps/fix')],
        output='screen'
    )

    # odom2tf = Node(
    #     package='python_node',
    #     executable='odom2tf', 
    #     name='odom2tf',
    #     parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    # )
    navsat_config = os.path.join(pkg_gazebo, 'config/navsat.yaml')

    navsat_node = Node(
        package='robot_localization',
        executable='navsat_transform_node',
        name='navsat_transform_node',
        output='screen',
        parameters=[navsat_config,
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg_gazebo, 'config/ekf.yaml'),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
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

    slam_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_slam, 'launch', 'online_async_launch.py')
            ),
            launch_arguments=[('use_sim_time', 'true')]
    )

    # slam_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_slam, 'launch', 'online_async_launch.py')
    #     ),
    #     launch_arguments=[
    #         ('use_sim_time', 'true'),
    #         ('slam_params_file', os.path.join(pkg_navigation, 'config', 'slam_toolbox_saved_map.yaml')),
    #         ('start_rviz', 'false')
    #     ]
    # )
    
    # slam_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_slam, 'launch', 'localization_launch.py')
    #     ),
    #     launch_arguments=[
    #         ('use_sim_time', 'true'),
    #         ('map_file', '~/my_map2.yaml')  # << il file .yaml della tua mappa
    #     ]
    # )

    # For Cartographer
    cartographer_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo, 'launch', 'cartographer.launch.py')
            ),
            launch_arguments=[('use_sim_time', 'true')]
    )

    # For Nav2 Costmap
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, 'launch', 'navigation_launch.py')
        ),
        launch_arguments=[('use_sim_time', 'true')]
    )

    nav2_costmap_markers_node = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d_markers',
        name='nav2_costmap_2d_markers',
        output='screen',
        parameters=[],
        remappings=[
            ('voxel_grid', '/local_costmap/voxel_grid'),
            ('visualization_marker', '/my_marker')
        ]
    )

    my_actions = [rviz_node, slam_launch, nav2_launch, nav2_costmap_markers_node]

    delayed_slam = TimerAction(
        period=10.0,  
        actions=my_actions
    )

    # keyboard_teleop_process = subprocess.Popen([
    #     "gnome-terminal",
    #     "--disable-factory",
    #     "--",
    #     "bash",
    #     "-c",
    #     "ros2 run python_node keyboard_teleop --ros-args -p use_sim_time:=true; exit"
    # ])

    # atexit.register(lambda: keyboard_teleop_process.send_signal(signal.SIGKILL))

    # static_map_odom = Node(
    #         package='tf2_ros',
    #         executable='static_transform_publisher',
    #         name='static_map_to_odom',
    #         arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
    #         output='screen'
    # )
    
    return LaunchDescription([
        sim_time_arg,
        bridge,
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        #navsat_node,
        robot_localization_node,
        wamv_controller,
        #slam_launch,
        #cartographer_launch
        #rviz_node
        #delayed_slam
        # ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
        # ros2 launch wamv_navigation bringup_launch.py use_sim_time:=True autostart:=False map:=/home/luca002/proj_ws/src/wamv_navigation/maps/my_map_d.yaml
        #  ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz

    ])

if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
