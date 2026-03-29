cmake_minimum_required(VERSION 3.8)
project(my_robot)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Install Python scripts as executables
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/sensor_monitor.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME sensor_monitor
)

install(PROGRAMS
  scripts/sensor_logger.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME sensor_logger
)

# Install directories
install(DIRECTORY
  urdf
  worlds
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()