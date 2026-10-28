#!/bin/bash
set -e
/usr/bin/python3 "$HOME/swarm_ws/src/swarm_project/scripts/start_ylidar.py"
exec env -i DISPLAY=:0 XAUTHORITY="$HOME/.Xauthority" HOME="$HOME" USER="$USER" TERM="${TERM:-xterm}" LANG=C.UTF-8 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin bash --noprofile --norc -c 'source /opt/ros/galactic/setup.bash && source "$HOME/ydlidar_ros2_ws/install/setup.bash" && source "$HOME/myagv_ros2_download/install/setup.bash" && exec ros2 launch myagv_odometry myagv_mapping.launch.py rviz:=true'
