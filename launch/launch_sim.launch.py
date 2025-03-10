import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArguments
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import IncludeLaunchDescription

from launch_ros.actions import Node

def generate_launch_descriptions():

    package_name = 'robot_testing'


    #include the launch file rsp.launch.py
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )]), launch_arguements = {'use_sim_time': 'true'}.items()

    )

    #include the gazebo launch file

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                )])
                
    )

    #include the spwan robot launch file
    spawn_robot = Node(package = 'ros_gz_sim', executable = 'create', 
                        arguements = ['-topic', 'robot_desciption',
                                      '-entity', 'robot'],
                        output = 'screen'
    )

    return IncludeLaunchDescription(
        [rsp, 
         gazebo,
         spawn_robot
         ])