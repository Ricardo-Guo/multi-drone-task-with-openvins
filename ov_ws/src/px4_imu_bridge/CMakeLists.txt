cmake_minimum_required(VERSION 3.8)
project(px4_imu_bridge)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# 只包含这一个文件，避免 main 函数冲突
add_executable(px4_imu_bridge_node src/px4_imu_bridge_node.cpp)

ament_target_dependencies(px4_imu_bridge_node
  rclcpp
  px4_msgs
  sensor_msgs
)

install(TARGETS
  px4_imu_bridge_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
