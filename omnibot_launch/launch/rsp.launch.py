import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro

# Starts robot_state_publisher with this robot's description.
def generate_launch_description():

    # Read this value when the launch file runs, so it can be set from the command line.
    use_sim_time = LaunchConfiguration("use_sim_time")

    # Find the installed description package path.
    pkg_path = os.path.join(get_package_share_directory("omnibot_description"))
    xacro_file = os.path.join(pkg_path, "urdf", "robots", "omnibot.urdf.xacro")

    # Expand the Xacro macros into the URDF XML string ROS nodes expect.
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # These values become parameters on robot_state_publisher.
    params = {
        "robot_description": robot_description_config,
        "use_sim_time": use_sim_time,
    }

    # Publishes the robot's TF transforms from its description and joint states.
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],
    )

    return LaunchDescription(
        [
            # Allows for our simulated system to have its own timers instead of what the physical bot hardware would provide. 
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use sim time if true",
            ),
            node_robot_state_publisher,
        ]
    )
