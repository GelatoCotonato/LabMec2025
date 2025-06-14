
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import launch.actions
import launch_ros.actions
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription, LaunchService
from bridge import Bridge, BridgeDirection
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
import subprocess

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
            # LIDAR topics (Gazebo -> ROS)
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',

            # (Gazebo -> ROS)
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',

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
        # remappings=[('/wamv/lidar_link/gpu_lidar/scan', '/wamv/base_link/scan'),
        #             ('/wamv/lidar_link/gpu_lidar/scan/points', '/wamv/base_link/scan/points')
        #             ],
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

    # static_tf = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='lidar_static_tf',
    #     arguments=[
    #         '0', '0', '1.5',   # translation: x y z
    #         '0', '0', '0',     # rotation: roll pitch yaw
    #         'base_link', 'lidar_link'
    #     ]
    # )

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
    command = "ros2 run python_node python_publisher"

    # Open a new terminal and run the command
    subprocess.Popen([
        "gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"
    ])

    ld = LaunchDescription([gz_sim, bridge_node])

    return ld


if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()

