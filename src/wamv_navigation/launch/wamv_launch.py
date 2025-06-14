from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    slam_config = os.path.join(
        get_package_share_directory('wamv_navigation'),
        'config',
        'mapper_params.yaml'
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        ]),
        launch_arguments={
            'slam': 'True',
            'use_sim_time': 'True',
            'params_file': os.path.join(
                get_package_share_directory('wamv_navigation'),
                'params',
                'nav2_params.yaml'
            )
        }.items()
    )

    return LaunchDescription([
        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[slam_config],
            output='screen'
        ),
        # Nav2 bringup
        nav2_launch
    ])