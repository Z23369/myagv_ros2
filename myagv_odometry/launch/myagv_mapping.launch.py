import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    description_dir = get_package_share_directory('myagv_description')
    odometry_dir = get_package_share_directory('myagv_odometry')
    lidar_dir = get_package_share_directory('ydlidar_ros2_driver')
    slam_dir = get_package_share_directory('slam_toolbox')

    urdf_path = os.path.join(description_dir, 'urdf', 'myAGV.urdf')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    lidar_params = os.path.expanduser('~/ydlidar_ros2_ws/src/ydlidar_ros2_driver/params/X2.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='false'),
        Node(package='myagv_odometry', executable='myagv_odometry_node', output='screen'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}], output='screen'),
        Node(package='tf2_ros', executable='static_transform_publisher', name='base_to_imu',
             arguments=['0', '0', '0', '0', '3.14159', '3.14159', 'base_footprint', 'imu_link']),
        Node(package='robot_localization', executable='ekf_node', name='ekf_node',
             parameters=[os.path.join(odometry_dir, 'config', 'ekf.yaml')], output='screen'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(lidar_dir, 'launch', 'ydlidar_launch.py')),
            launch_arguments={'params_file': lidar_params}.items()),
        Node(package='slam_toolbox', executable='async_slam_toolbox_node', name='slam_toolbox',
             parameters=[os.path.join(slam_dir, 'config', 'mapper_params_online_async.yaml')],
             output='screen'),
        Node(package='rviz2', executable='rviz2',
             condition=IfCondition(LaunchConfiguration('rviz')), output='screen',
            arguments=['-d', '/home/er/myagv_mapping.rviz']),
    ])
