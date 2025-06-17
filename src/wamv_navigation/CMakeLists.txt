cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)
project(wamv_navigation)

# Abilita debug simboli e compilazione moderna
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Dipendenze di build dichiarate in package.xml
find_package(ament_cmake REQUIRED)
find_package(nav2_common REQUIRED)

# Dipendenze ROS 2
find_package(ros_gz_bridge REQUIRED)
find_package(ros_gz_interfaces REQUIRED)
find_package(ros_gz_image REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(xacro REQUIRED)

# # Hooks
# ament_environment_hooks("hooks/ament_prefix_path.dsv.in")
# ament_environment_hooks("hooks/ament_prefix_path.sh")
# ament_environment_hooks("hooks/path.dsv.in")
# ament_environment_hooks("hooks/path.sh")

# Installa i file Python
install(
  DIRECTORY
    ${CMAKE_CURRENT_SOURCE_DIR}/
  DESTINATION lib/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.py"
)

# install(
#   DIRECTORY
#     ${CMAKE_CURRENT_SOURCE_DIR}/
#   DESTINATION share/${PROJECT_NAME}
#   FILES_MATCHING PATTERN "*.py"
# )

# CMake config files 
install(DIRECTORY 
  config
  launch
  maps
  params
  rviz
  description
  DESTINATION share/${PROJECT_NAME}
)

# Rende visibile il pacchetto ad ament
ament_package()