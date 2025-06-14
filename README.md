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

Command to launch the world and the robot:
<pre>python3 ~/proj_ws/src/wamv_gazebo/launch/mylaunch.py</pre>

<pre>ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/home/luca002/proj_ws/src/wamv_navigation/config/slam_toolbox_params.yaml
</pre>


<pre>rviz2</pre>

<pre>ros2 run python_node python_publisher</pre>

Tf check:
<pre>ros2 run tf2_ros tf2_echo base_link lidar_link</pre>

Generation of /tf_static topic:
<pre>ros2 run tf2_tools view_frames</pre>

How to get the params of slam toolbox:
<pre>ros2 param list /slam_toolbox</pre>

To get the publication rate (Hz) of a topic :
<pre>ros2 topic hz /name_of_topic</pre>

STEPS for SIMULATION:
1. Launch Gazebo with World
2. Define Robot Parameters
3. Launch Gazebo with Boat   
4. Launch Bridges <pre>python3 ~/proj_ws/src/wamv_gazebo/launch/mylaunch.py</pre>
5. Launch Subscription Node to receive /odom in order to publish /tf 
5. Define SLAM Toolbox Config Parameters (yaml)
6. Launch SLAM Toolbox
7. Launch RViz
8. Launch Teleop
