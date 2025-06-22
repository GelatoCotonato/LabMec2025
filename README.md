# Progetto per Esame di Laboratorio di Meccatronica
Progetto per esame di 'Laboratorio di Meccatronica', nell'Anno Accademico 2024/2025, realizzato da:
1. Luca Barbieri, matricola 252440
2. Lorenzo Graceffa, matricola 257254

La cartella _wamv_gazebo_ contiene i modelli del mondo, compresi gli ostacoli statici, e il modello URDF del robot. Sono inoltre presenti i seguenti launch files:
1. wamv_rviz.py 
2. wamv_gz_rviz.py 
3. wamv_keyboard_control.py 

La cartella _python_node_ contiene nodi Publisher/Subscriber a supporto dei launch files di altre cartelle.

La cartella _wamv_navigation_ integra SLAM Toolbox, Nav2 e Cartographer per la navigazione del robot, e include i seguenti launch files:
1. wamv_localization.py
2. wamv_navigation.py

Per avviare correttamente le simulazioni, è necessario aggiornare la proprietà Xacro _user_path_ nel file _wamv_gazebo/urdf/model.urdf.xacro_ con il percorso assoluto corretto.