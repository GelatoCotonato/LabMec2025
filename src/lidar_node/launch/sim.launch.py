import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    # Path to your world file
    world_path = os.path.join(os.getcwd(),'src/proj/src/vrx/vrx_gz/worlds/sydney.sdf')
    
    return LaunchDescription([
        # Launch Gazebo with your world
        ExecuteProcess(
            cmd=['gz', 'sim', '-v', '4', '-r', world_path],
            output='screen'
        ),
        
        # Launch ROS-Gazebo bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['--config', os.path.join(
                os.getcwd(), 
                'config/bridge.yaml'
            )],
            output='screen'
        )
    ])