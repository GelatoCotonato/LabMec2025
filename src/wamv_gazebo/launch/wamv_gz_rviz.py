# Displaying the urdf model on rviz and spawning the robot model in Gazebo

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # Defining directory
    pkg_gazebo = get_package_share_directory('wamv_gazebo')

    # Defining urdf model, world model and lastly rviz config file
    urdf_model_path = os.path.join(pkg_gazebo, 'urdf','model.urdf.xacro')
    world_path = os.path.join(pkg_gazebo, 'worlds','sydney.sdf')
    rviz_config_path = os.path.join(pkg_gazebo, 'rviz','wamv_gz_rviz.rviz')

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
                     'use_sim_time': True}],
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[{'rate': 20.0,
                    'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_model_path]),
            'publish_frequency': 20.0, 
            'use_sim_time': True
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
            '-x', '0', '-y', '0', '-z', '0.2',
            '--wait', '10'  
        ],
        output='screen'
    )
    
    # Bridge to convert topics (GZ -> ROS & ROS -> GZ)
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
        ],
        remappings=[('/fix', '/gps/fix')],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + rviz_config_path],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )
    
    gui_teleop = Node(
        package='python_node',
        executable='gui_teleop', 
        name='gui_teleop',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    return LaunchDescription([
        sim_time_arg,
        gui,
        bridge,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        rviz_node,
        gui_teleop
    ])