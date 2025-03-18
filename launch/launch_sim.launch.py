import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'my_bot'
    print(os.path.join(get_package_share_directory(package_name)))


    #include the launch file rsp.launch.py
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )), launch_arguments = {'use_sim_time': 'true'}.items()

    )

    #declare the world path
    default_world = os.path.join(get_package_share_directory(package_name), 'worlds', 'empty.world')
    
    #declare the world argument
    world_arg = DeclareLaunchArgument('world', default_value=default_world, description='Loading World file')
    world = LaunchConfiguration('world')

    #include the gazebo launch file
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                )), launch_arguments = {'gz_args': ['-r -v 4 ', world], 'on_exit_shutdown':'true'}.items()
                
    )

    #include the spwan robot launch file
    spawn_robot = Node(package = 'ros_gz_sim', executable = 'create', 
                        arguments = ['-topic', 'robot_description',
                                      '-name', 'my_bot',
                                      'z', '-5.0'],
                        output = 'screen'
    )

    ld = LaunchDescription()
    ld.add_action(world_arg)
    ld.add_action(rsp)
    ld.add_action(gazebo)
    ld.add_action(spawn_robot)
    return ld