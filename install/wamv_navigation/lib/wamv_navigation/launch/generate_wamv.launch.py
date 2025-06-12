import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def launch(context, *args, **kwargs):
    wamv_locked = LaunchConfiguration('wamv_locked').perform(context)
    component_yaml = LaunchConfiguration('component_yaml').perform(context)
    thruster_yaml = LaunchConfiguration('thruster_yaml').perform(context)
    wamv_target = LaunchConfiguration('wamv_target').perform(context)

    if not component_yaml:
        component_yaml = os.path.join(get_package_share_directory('wamv_gazebo'),
                                      'config', 'wamv_config', 'example_component_config.yaml')
    if not thruster_yaml:
        thruster_yaml = os.path.join(get_package_share_directory('wamv_gazebo'),
                                     'config', 'wamv_config', 'example_thruster_config.yaml')

    components_dir = os.path.join(get_package_share_directory('wamv_gazebo'),
                                  'urdf', 'components')
    thrusters_dir = os.path.join(get_package_share_directory('wamv_description'),
                                 'urdf', 'thrusters')
    wamv_gazebo = os.path.join(get_package_share_directory('wamv_gazebo'),
                                 'urdf', 'wamv_gazebo.urdf.xacro')

    node = Node(package='wamv_gazebo',
                executable='generate_wamv.py',
                output='screen',
                parameters=[{'wamv_locked': wamv_locked},
                            {'component_yaml': component_yaml},
                            {'thruster_yaml': thruster_yaml},
                            {'wamv_target': wamv_target},
                            {'components_dir': components_dir},
                            {'thrusters_dir': thrusters_dir},
                            {'wamv_gazebo': wamv_gazebo}])

    return [node]

def generate_launch_description():
    return LaunchDescription([
        # Launch Arguments
        DeclareLaunchArgument(
            'wamv_locked',
            default_value='False',
            description='WAM-V locked'),
        DeclareLaunchArgument(
            'component_yaml',
            default_value='',
            description='Path to component yaml file.'),
        DeclareLaunchArgument(
            'thruster_yaml',
            default_value='',
            description='Path to thruster yaml file.'),
        DeclareLaunchArgument(
            'wamv_target',
            default_value='',
            description='WAM-V target output URDF file'),
        OpaqueFunction(function=launch),
    ])
