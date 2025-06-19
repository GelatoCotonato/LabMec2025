# ADDING SLAM_TOOLBOX

import os, subprocess, atexit, signal
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('wamv_gazebo')
    pkg_navigation = get_package_share_directory('wamv_navigation')
    pkg_slam = get_package_share_directory('slam_toolbox')

    # Percorsi dei file
    urdf_model_path = os.path.join(pkg_gazebo, 'urdf', 'model.urdf.xacro')
    world_path = os.path.join(pkg_gazebo, 'worlds', 'sydney.sdf')
    rviz_config_path = os.path.join(pkg_navigation, 'rviz', 'config3.rviz')

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

    gui = DeclareLaunchArgument(
        name='gui',
        default_value='True',
        description='Flag to enable joint_state_publisher_gui'
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_model_path]),
                     'rate': 20.0,
                     'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=UnlessCondition(LaunchConfiguration('gui'))
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
        output='screen'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg_navigation, 'config/ekf.yaml'),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )
    
    slam_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_slam, 'launch', 'online_async_launch.py')
            ),
            launch_arguments=[('use_sim_time', 'true')]
    )

    wamv_controller = Node(
        package='python_node',
        executable='wamv_controller', 
        name='wamv_controller',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    keyboard_teleop_process = subprocess.Popen([
        "gnome-terminal",
        "--disable-factory",
        "--",
        "bash",
        "-c",
        "ros2 run python_node keyboard_teleop --ros-args -p use_sim_time:=true; exit"
    ])

    atexit.register(lambda: keyboard_teleop_process.send_signal(signal.SIGKILL))

    return LaunchDescription([
        sim_time_arg,
        gui,
        bridge,
        joint_state_publisher_node,
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        robot_localization_node,
        wamv_controller,
        slam_launch
    ])

if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()


