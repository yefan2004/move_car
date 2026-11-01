cmake_minimum_required(VERSION 3.8)
project(move_car_simulation)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
install(PROGRAMS scripts/drive_path.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
