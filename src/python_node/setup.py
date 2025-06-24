from setuptools import find_packages, setup

package_name = 'python_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Luca Barbieri',
    maintainer_email='emailprogramming02@gmail.com',
    description='Defining Python Nodes for control and teleoperation',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gui_teleop = python_node.GuiTeleop:main',
            'keyboard_teleop = python_node.KeyboardTeleop:main',
            'wamv_controller = python_node.WamvController:main',
            'coast_follower = python_node.CoastFollower:main'
        ],
    },
)
