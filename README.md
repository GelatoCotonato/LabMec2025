# LabMec2025
Progetto per esame di laboratorio di meccatronica 2025

Questo repositorio contiene i file relativi al progetto di laboritorio di meccatronica del 2025

link per aggiungere sensore: https://gazebosim.org/docs/harmonic/sensors/

esempio utile per prendere i modelli: https://github.com/osrf/vrx.git

Comandi utili:

Generation of /tf_static topic: <pre>ros2 run tf2_tools view_frames</pre>
Visualizing frame:<pre>evince frame_name.pdf</pre>
How to get the params of slam toolbox: <pre>ros2 param list /slam_toolbox</pre>
To get the publication rate (Hz) of a topic: <pre>ros2 topic hz /name_of_topic</pre>

Command to save the map:
<pre>ros2 run nav2_map_server map_saver_cli -f /home/user/my_map --ros-args -r /map:=/map_abs_path</pre>

Command to launch Obstaicle Avoidance Algorith:
1. Lanciare launch8 in wamv_navigation
2. <pre>ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom</pre>
3. <pre>ros2 launch wamv_navigation bringup_launch.py use_sim_time:=true</pre>
4. <pre>ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz</pre>

<pre>ros2 run nav2_costmap_2d nav2_costmap_2d_markers voxel_grid:=/local_costmap/voxel_grid visualization_marker:=/my_marker</pre>

