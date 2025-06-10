from setuptools import find_packages
from setuptools import setup

setup(
    name='wamv_gazebo',
    version='0.0.0',
    packages=find_packages(
        include=('wamv_gazebo', 'wamv_gazebo.*')),
)
