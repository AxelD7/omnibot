import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    package_name = "omnibot_launch"

    # Calls for robot state pubisher launch file.
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name), "launch", "rsp.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    world = LaunchConfiguration("world")

    # Declare the world gazebo will load in to.
    world_arg = DeclareLaunchArgument(
        "world", default_value="empty.sdf", description="world to load"
    )
    # Gazebo <-> ROS Bridge
    bridge_params = os.path.join(
        get_package_share_directory(package_name), "config", "gz_bridge.yaml"
    )
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "--ros-args",
            "-p",
            f"config_file:={bridge_params}",
        ],
    )
    # Actually launches gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("ros_gz_sim"),
                    "launch",
                    "gz_sim.launch.py",
                )
            ]
        ),
        # -r starts sim in running mode -v4 is level 4 verbosity for logging.
        launch_arguments={
            "gz_args": ["-r -v4", world],
            "on_exit_shutdown": "true",
        }.items(),
    )

    # Spawns the robot into gazebo from the /robot_description topic.
    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "omnibot", "-z", "0.1"],
        output="screen",
    )

    # Wheel controller manager spawner. It is on a timer to delay its start up by 5 seconds.
    spawn_wheel_controller = TimerAction(
        period=5.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["joint_state_broadcaster", "omni_wheel_drive_controller"],
                parameters=[{"use_sim_time": True}],
                output="screen",
            )
        ],
    )

    # Loads RVIZ based off of the config saved in the description.
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            os.path.join(
                get_package_share_directory("omnibot_description"),
                "rviz",
                "omnibot_rviz_config.rviz",
            ),
        ],
    )

    # Finally returns the entire launch description of all the nodes!
    return LaunchDescription(
        [
            rsp,
            world_arg,
            ros_gz_bridge,
            gazebo,
            spawn_entity,
            rviz_node,
            spawn_wheel_controller,
        ]
    )
