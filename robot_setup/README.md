# myAGV Pi 2023 - ROS 2 Mapping Setup

## Platform
Raspberry Pi 4, Ubuntu 20.04 ARM64, ROS 2 Galactic, myAGV firmware 1.3.

## Components
- myagv_odometry: chassis control, /odom and /imu, using /dev/ttyAMA2.
- myagv_description: official robot URDF.
- robot_localization: EKF providing odom to base_footprint TF.
- YDLIDAR X2: /scan on /dev/ttyAMA0, using the separate Z23369/ydlidar_ros2_driver repository, branch myagv-galactic-x2.
- slam_toolbox: publishes /map.
- RViz 2: displays the live map.

## Setup
Build myagv_description and myagv_odometry with ROS 2 Galactic. Separately build the YDLIDAR workspace in ~/ydlidar_ros2_ws. Install robot_localization, slam_toolbox, rviz2, and nav2_map_server. Copy start_myagv_mapping.sh, myagv_mapping.rviz, and myagv_demo_teleop.py from this folder into ~/; copy start_ylidar.py to ~/swarm_ws/src/swarm_project/scripts/. Make the startup script executable.

## Run
Run ~/start_myagv_mapping.sh to enable LiDAR GPIO 20 and start odometry, EKF, LiDAR, SLAM, and RViz on display :0. In another ROS 2 Galactic terminal, run python3 ~/myagv_demo_teleop.py for keyboard control. Do not start another chassis or LiDAR driver simultaneously.

## Important paths and limitations
The current scripts assume user er and the existing workspace layout. The mapping launch uses ~/ydlidar_ros2_ws/src/ydlidar_ros2_driver/params/X2.yaml. RViz uses /home/er/myagv_mapping.rviz. The LiDAR height of 0.02 m and IMU static transform require physical verification before accurate mapping or navigation. The saved room map (~/myagv_first_map.pgm and .yaml) is kept outside this repository.
