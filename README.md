# LabMec2025
Progetto per esame di laboratorio di meccatronica 2025

Questo repositorio contiene i file relativi al progetto di laboritorio di meccatronica del 2025

Link modello catamarano: https://github.com/Intelligent-Quads/iq_sim

comando primo terminale 
gz sim /home/gelatocotonato/prog_mec/src/world/simple_baylands.sdf

comando secondo terminale
gz service -s /world/simple_baylands/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 1000 --req 'sdf_filename: "/home/gelatocotonato/prog_mec/src/boat_description/boat/model.sdf"'

link per aggiungere sensore: https://gazebosim.org/docs/harmonic/sensors/

esempio utile per prendere i modelli: https://github.com/osrf/vrx.git


---Punti da seguire---

1) importare il modeloo della barca
2) importare il mondo
3) collegare il lidar
4) ricevere la cloud point 
5) profilo della costa(modello 3d)
6) ricavare distanza dalla costa
7) obstacle avoidance
8) correzione rotta


<pre>python3 ~/proj_ws/src/wamv_gazebo/launch/mylaunch.py</pre>

<pre>rviz2</pre>

<pre>ros2 run python_node python_publisher</pre>

<pre>ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=~/proj_ws/src/wamv_navigation/config/mapper_params_online_async.yaml \
  use_sim_time:=true</pre>

Tf:
<pre>ros2 run tf2_ros static_transform_publisher --x 0.77 --y 1,3 --z 0.035 --roll 0 --pitch 0 --yaw 0 --frame-id base_link --child-frame-id lidar_link</pre>

Tf check:
<pre>ros2 run tf2_ros tf2_echo base_link lidar_link</pre>


Generation of /tf_static topic:
<pre>ros2 run tf2_tools view_frames</pre>
