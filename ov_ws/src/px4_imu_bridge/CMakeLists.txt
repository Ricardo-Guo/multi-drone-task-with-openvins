cmake_minimum_required(VERSION 3.8)
project(px4_imu_bridge)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 寻找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# 声明可执行文件
add_executable(imu_bridge_node src/px4_imu_bridge_node.cpp)

# 链接依赖
ament_target_dependencies(imu_bridge_node
  rclcpp
  px4_msgs
  sensor_msgs
)

# 安装可执行文件到 lib 目录，这样 ros2 run 才能找到
install(TARGETS
  imu_bridge_node
  DESTINATION lib/${PROJECT_NAME}
)

# 导出包
ament_package()
