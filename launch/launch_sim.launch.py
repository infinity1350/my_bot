import os

from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'my_bot'


    #include the launch file rsp.launch.py
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )), launch_arguments = {'use_sim_time': 'true'}.items()

    )

    #include the gazebo launch file

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                ))
                
    )

    #include the spwan robot launch file
    spawn_robot = Node(package = 'ros_gz_sim', executable = 'create', 
                        arguments = ['-topic', 'robot_description',
                                      '-entity', 'robot'],
                        output = 'screen'
    )

    ld = LaunchDescription()
    ld.add_action(rsp)
    ld.add_action(gazebo)
    ld.add_action(spawn_robot)
    return ld