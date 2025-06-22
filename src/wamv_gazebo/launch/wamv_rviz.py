# Displaying the urdf model on rviz and moving, through a graphical interface, the joints of the boat, which are:
# 1. 'left_chassis_engine_joint';
# 2. 'left_engine_propeller_joint';
# 3. 'right_chassis_engine_joint';
# 4. 'right_engine_propeller_joint'.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node

def generate_launch_description():

    # Defining directory
    pkg_gazebo = get_package_share_directory('wamv_gazebo')

    # Defining urdf model and rviz config file
    urdf_model_path = os.path.join(pkg_gazebo,'urdf','model.urdf.xacro')
    rviz_config_path = os.path.join(pkg_gazebo,'rviz', 'wamv_rviz.rviz')

    if not os.path.exists(urdf_model_path):
        raise FileNotFoundError(f'Urdf file not found at: {urdf_model_path}')
    if not os.path.exists(rviz_config_path):
        raise FileNotFoundError(f'Rviz config file not found at: {rviz_config_path}')
    
    gui = DeclareLaunchArgument(
        name='gui',
        default_value='True',
        description='Flag to enable joint_state_publisher_gui'
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_model_path])}],
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_model_path])}]
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
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher,
        rviz_node
    ])

    return ld
