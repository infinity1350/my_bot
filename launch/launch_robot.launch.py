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

    controller_manager = Node(
        package = 'controller_manager',
        executable = 'spawner.py,',
        parameter = [os.join(get_package_share_directory(package_name),'config','controllers.yaml')],
        output = 'screen'
    )

    diff_drive_spawner = Node(
        package = 'controller_manager'
        executable = spwaner.py,
        arguements  = ['diff_drive_controller', '--controller-manager', 'controller_manager'],
        output = 'screen'
    )

    joint_state_broadcaster = Node()

    serial_node = Node(
        package = 'my_bot'
        executable = 'serial_bridge',
        parameters = [{'port' : '/dev/ttyUSB0', 'baud_rate' : 115200}],
        output = 'screen'
    )
 
    ld = LaunchDescription()
 
    ld.add_action(rsp)
    ld.add_action(controller_manager)
    ld.add_action(diff_drive_spawner)
    ld.add_action(serial_node)
  
    return ld