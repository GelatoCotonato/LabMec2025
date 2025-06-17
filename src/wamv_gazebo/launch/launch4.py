
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import ExecuteProcess, IncludeLaunchDescription
import launch.actions
import launch_ros.actions
from launch.actions import TimerAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
import subprocess
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from ros_gz_sim.actions import GzServer

def generate_launch_description(world_name="sydney", robot_name="wam-v", ign_flag=True):

    # PATHS
    my_dir = get_package_share_directory("wamv_gazebo")

    world_path = os.path.join(my_dir,"worlds",f"{world_name}.sdf")
    robot_path = os.path.join(my_dir,"models",f"{robot_name}","model.sdf")

    my_dir2 = get_package_share_directory("wamv_navigation")

    default_model_path = os.path.join(my_dir,"urdf","model.xacro")

    rviz_config_path = os.path.join(my_dir2, 'rviz', 'config.rviz')

    # Verify the world file exists
    if not os.path.exists(world_path):
        raise FileNotFoundError(f"World file not found at: {world_path}")

    if not os.path.exists(robot_path):
        raise FileNotFoundError(f"Robot file not found at: {robot_path}")

    if not os.path.exists(default_model_path):
        raise FileNotFoundError(f"Urdf file not found at: {default_model_path}")
    

    gz_args = ["-v", "0", "-r", world_path]

    gz_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('ros_gz_sim'),'launch'),
                '/gz_sim.launch.py']),
            launch_arguments={'gz_args': ' '.join(gz_args)}.items())
    
    # BRIDGES

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='dynamic_bridge',
        arguments=[
            # LIDAR topics (Gazebo -> ROS)
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',

            # IMU (Gazebo -> ROS)
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',

            # Odom & TF (Gazebo -> ROS)
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/model/wamv/odometry_with_covariance@nav_msgs/msg/Odometry[gz.msgs.OdometryWithCovariance',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',

            # GPS (Gazebo -> ROS)
            '/fix@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',

            # Clock (Gazebo -> ROS)
            '/world/sydney/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',

            # Angular velocity readings (Gazebo -> ROS)
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


    # # Localization Setup (AMCL) useful in a pre-built map 
    # amcl_node = Node(
    #     package='nav2_amcl',
    #     executable='amcl',
    #     name='amcl',
    #     parameters=[{
    #         'use_sim_time': True,
    #         'odom_frame_id': 'odom',
    #         'base_frame_id': 'base_link',
    #         'global_frame_id': 'map'
    #     }]
    # )

    # Dynamic TF: odom -> base_link
    odom_tf = Node(
        package='python_node',
        executable='odom_to_tf',  # assuming this is how your Python node is set
        name='odom_to_tf'
    )

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_lidar',
        arguments=['0.77', '0.0', '1.336', '0', '0', '0', 'base_link', 'lidar_link'],
        output='screen'
    )
    
    wamv_param_dir = LaunchConfiguration(
        'wamv_param_dir',
        default=os.path.join(
            get_package_share_directory('wamv_navigation'),
            'param','wamv_config.yaml'))
    
    wamv_param = DeclareLaunchArgument(
            'wamv_param_dir',
            default_value=wamv_param_dir,
            description='Full path to wam-v parameter file to load')
    

    slam_config = os.path.join(
    get_package_share_directory('wamv_navigation'),
    'config',
    'slam_toolbox_params.yaml'
    )

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[slam_config],
        output='screen'
    )
    
#     slam_toolbox_node = Node(
#     package='slam_toolbox',
#     executable='sync_slam_toolbox_node',
#     name='slam_toolbox',
#     parameters=[{
#         'use_sim_time': True,
#         'slam_mode': 'mapping'
#     }],
#     output='screen'
# )
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', default_model_path])}],
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d' + rviz_config_path]
    )
    
    gz_server = GzServer(
        world_sdf_file=world_path,
        container_name='ros_gz_container',
        create_own_container='True',
        use_composition='True',
    )


    command = "ros2 run python_node python_publisher"

    # Open a new terminal and run the command
    subprocess.Popen([
        "gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"
    ])

    spawn_robot = TimerAction(
        period=5.0, 
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'ros_gz_sim', 'create',
                    '-file', robot_path,
                    '-x', '0', '-y', '0', '-z', '-0.2',
                    '-name', 'wamv'
                ],
                output='screen'
            )
        ]
    )

    
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(my_dir2,'config','ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    gui = DeclareLaunchArgument(
        name='gui',
        default_value='True',
        description='Flag to enable joint_state_publisher_gui'
    )
    
    model_path = DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Absolute path to robot model file'
    )
        
    ld = LaunchDescription([
        gui,
        model_path,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
        DeclareLaunchArgument(name="use_sim_time",default_value="True", description="Flag to enable use_sim_time"),
        gz_sim,
        bridge_node,
        spawn_robot,
        # DeclareLaunchArgument(
        #     name='model',
        #     default_value=default_model_path,
        #     description='Absolute path to robot urdf file'
        # ),
        # DeclareLaunchArgument(
        #     name='gui',
        #     default_value='true',
        #     description='Flag to enable joint_state_publisher_gui'
        # ),

        # Node(
        #     package='joint_state_publisher',
        #     executable='joint_state_publisher',
        #     name='joint_state_publisher',
        #     parameters=[{'source_list': ['joint_states']}],
        #     condition=UnlessCondition(LaunchConfiguration('gui'))
        # ),

        # Node(
        #     package='joint_state_publisher_gui',
        #     executable='joint_state_publisher_gui',
        #     name='joint_state_publisher_gui',
        #     condition=IfCondition(LaunchConfiguration('gui'))
        # ),

        # Node(
        #     package='robot_state_publisher',
        #     executable='robot_state_publisher',
        #     name='robot_state_publisher',
        #     parameters=[{
        #         'robot_description': open(default_model_path).read()
        #     }]
        # ),
        
        # robot_localization_node
        ])

    return ld


if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()

