import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('my_robot')
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_file   = os.path.join(pkg, 'worlds', 'robot_world.world')
    urdf_file    = os.path.join(pkg, 'urdf', 'my_robot.urdf.xacro')
    robot_desc   = Command(['xacro ', urdf_file])

    # ── Gazebo ──────────────────────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': world_file, 'verbose': 'false'}.items()
    )

    # ── Robot State Publisher ────────────────────────────────────────────────
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}]
    )

    # ── Spawn Robot ──────────────────────────────────────────────────────────
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot',
                   '-x', '0', '-y', '0', '-z', '0.15'],
        output='screen'
    )

    # ── Sensor Monitor Node ──────────────────────────────────────────────────
    sensor_monitor = Node(
        package='my_robot',
        executable='sensor_monitor',
        name='sensor_monitor',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # ── Teleop Keyboard ──────────────────────────────────────────────────────
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop',
        remappings=[('/cmd_vel', '/robot/cmd_vel')],
        prefix='xterm -e',
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        gazebo,
        robot_state_pub,
        spawn_robot,
        sensor_monitor,
        teleop,
    ])
