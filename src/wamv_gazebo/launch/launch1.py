# PLOTTING THE WAMV IN RVIZ 

from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description(robot_name="wam-v"):

    gazebo_dir = get_package_share_directory("wamv_gazebo")
    navigation_dir = get_package_share_directory("wamv_navigation")

    model_path = os.path.join(gazebo_dir,"urdf","model.urdf.xacro")
    
    rviz_config_path = os.path.join(navigation_dir, 'rviz', 'config.rviz')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Urdf file not found at: {model_path}")
    

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
    
    model_path_arg = DeclareLaunchArgument(
        name='model',
        default_value=model_path,
        description='Absolute path to robot model file'
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', model_path])}],
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', model_path])}]
    )

    rviz_node = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + rviz_config_path]
    )
        
    ld = LaunchDescription([
        gui,
        model_path_arg,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher,
        rviz_node
    ])

    return ld


if __name__ == '__main__':

    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()

