import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.event_handlers import OnProcessExit


def generate_launch_description():

    package_name = 'my_bot'
    
    robot_controllers = os.path.join(
        get_package_share_directory(package_name), 'config', 'robot_controllers.yaml'
    )
    

    #include the launch file rsp.launch.py
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )), launch_arguments = {'use_sim_time': 'true'}.items()

    )

    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_node = Node(
        package = 'controller_manager',
        executable = 'ros2_control_node',
        parameters = [{'robot_description':robot_description},robot_controllers],
        output = 'both'
    )

    robot_pub_sub = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'both',
        parameters = [robot_description],

    )

    joint_state_broadcaster_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments= ['joint_state_broadcaster'],
    )

    robot_controller_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['diffbot_base_controller',
                      '--param-file',
                      robot_controllers,
                      '--controller-ros-args',
                      '-r /diffbot_base_controller/cmd_vel:=/cmd_vel',],
    )

    delay_joint_state_broadcaster_after_robot_controller_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=robot_controller_spawner,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )
 
    ld = LaunchDescription()
 
    ld.add_action(rsp)
    ld.add_action(controller_node)
    ld.add_action(robot_pub_sub)
    ld.add_action(delay_joint_state_broadcaster_after_robot_controller_spawner)
    ld.add_action(robot_controller_spawner)
   
    return ld