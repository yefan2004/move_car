cmake_minimum_required(VERSION 3.8)
project(move_car_navigation)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch config maps models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
