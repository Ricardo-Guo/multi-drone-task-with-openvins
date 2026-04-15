# PX4-ROS2-Gazebo-YOLOv8 项目完整介绍

## 项目根目录

### 根目录文件

#### Python脚本

**KeyPressModule.py**
- 功能：键盘输入处理模块
- 特点：使用termios和tty库实现非阻塞键盘捕获
- 线程安全：使用线程和锁机制
- 支持按键：WASD方向键、r（武装）、l（降落）、i（打印飞行模式）、Ctrl+C（退出）

**keyboard-mavsdk-test.py**
- 功能：无人机键盘控制器
- 控制内容：
  - 飞行控制：WASD控制滚转/俯仰/偏航/油门
  - 降落控制：L键降落
  - 武装控制：R键武装无人机
  - 云台控制：JKMN键控制云台俯仰和偏航角度
- 集成：与KeyPressModule模块配合使用

**uav_camera_det.py**
- 功能：实时目标检测与可视化
- 技术栈：ROS 2 + OpenCV + YOLOv8
- 功能细节：
  - 订阅相机话题接收视频流
  - 使用YOLOv8m.pt模型进行实时检测
  - 检测类别：人（class 0）、汽车（class 2）
  - 显示可调整大小的检测窗口
- 实现：基于CvBridge进行ROS图像消息与OpenCV图像转换

**move_car.py**
- 功能：在仿真环境中驱动汽车模型做圆周运动
- 参数配置：
  - 汽车模型：hatchback_blue_1
  - 圆心坐标：(280.0, -140.0)
  - 半径：15米
  - 速度：5 m/s
  - 更新频率：10 Hz
- 实现方式：通过gz service调用set_pose服务更新汽车位姿

**setup_gimbal.py**
- 功能：修改PX4 x500_depth无人机模型SDF文件，添加2轴云台
- 修改内容：
  - 移除固定的CameraJoint
  - 添加gimbal_link中间链接
  - 添加gimbal_yaw_joint（偏航关节，Z轴旋转）
  - 添加gimbal_pitch_joint（俯仰关节，Y轴旋转）
  - 添加JointPositionController插件
- 控制接口：
  - `/gimbal/cmd_pitch` - 俯仰控制话题
  - `/gimbal/cmd_yaw` - 偏航控制话题
- 初始参数：俯仰角45度向下，俯仰范围-90°~30°，偏航范围-90°~90°

#### 配置文件

**px4_ros2_gazebo.yml**
- 功能：tmuxinator配置文件，定义Docker容器内6个面板的启动配置
- 面板布局：
  1. Micro XRCE-DDS Agent通信桥梁
  2. PX4 SITL核心仿真
  3. 图像桥接（Gazebo到ROS 2）
  4. YOLO检测服务
  5. 交互终端（move_car）
  6. 键盘控制终端
- 布局方式：tiled（平铺布局）

**Dockerfile**
- 基础镜像：ros:humble-desktop-full
- 安装内容：
  - PX4 Autopilot源码与编译
  - Micro XRCE-DDS Agent
  - ROS 2工作空间（ws_sensor_combined、ws_offload_control）
  - Python依赖（MAVSDK、OpenCV、YOLOv8等）
  - Gazebo Garden
- 模型复制：
  - models/ → ~/.gz/models/
  - models_docker/ → Gazebo Fuel模型目录
- 镜像名称：monemati/px4_ros2_gazebo_yolov8_image

#### 其他文件

**.gitignore** - Git忽略配置
**Procedure.odt** - 过程文档（OpenDocument格式）
**yolov8m.pt** - YOLOv8中等模型权重文件

### models文件夹 - Gazebo模型库

#### casual_female - 休闲女性人偶模型

**model.config**
- 模型名称：Casual Female
- 版本：1.0
- SDF版本：1.5
- 作者：Rohit Salem
- 描述：使用MakeHuman创建的站立人偶

**model.sdf**
- 模型名称：casual_female
- 静态模型：true
- 碰撞体：0.76 x 0.33 x 1.77米的盒子
- 视觉网格：meshes/casual_female.dae

**meshes/casual_female.dae**
- COLLADA格式的3D人偶网格模型

**materials/textures/**
- casual_female.png - 主要纹理
- brown_eye.png - 眼睛纹理
- female_casualsuit01_diffuse.png - 服装1漫反射贴图
- female_casualsuit01_normal.png - 服装1法线贴图
- female_casualsuit02_diffuse.png - 服装2漫反射贴图
- female_casualsuit02_normal.png - 服装2法线贴图
- shoes05_diffuse.png - 鞋子纹理
- tongue01_diffuse.png - 舌头纹理
- young_lightskinned_female_diffuse.png - 皮肤纹理
- eyebrow002.png - 眉毛纹理
- eyelashes01.png - 睫毛纹理
- ponytail01_diffuse.png - 马尾纹理

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### hatchback - 两厢车模型

**model.config**
- 模型名称：Hatchback
- 版本：1.0
- SDF版本：1.6
- 作者：Nate Koenig
- 描述：两厢车模型

**model.sdf**
- 模型名称：hatchback
- 静态模型：true
- 碰撞体和视觉：使用meshes/hatchback.obj网格
- 旋转：绕Z轴旋转1.57079632679弧度（90度）
- 缩放：0.0254比例因子

**meshes/hatchback.mtl**
- 材质库文件

**meshes/hatchback.obj**
- OBJ格式的3D网格模型

**materials/textures/**
- hatchback.png - 车身纹理
- wheels3.png - 轮胎纹理

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### hatchback_blue - 蓝色两厢车模型

**model.config**
- 模型名称：Hatchback blue
- 版本：1.0
- SDF版本：1.6
- 作者：Nate Koenig
- 依赖：model://hatchback
- 描述：蓝色两厢车

**model.sdf**
- 模型名称：hatchback_blue
- 静态模型：true
- 碰撞体和视觉：使用meshes/hatchback.obj网格
- 旋转：绕Z轴旋转1.57079632679弧度（90度）
- 缩放：0.0254比例因子

**meshes/hatchback.mtl**
- 材质库文件

**meshes/hatchback.obj**
- OBJ格式的3D网格模型

**materials/textures/**
- hatchback.png - 车身纹理

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### pickup - 皮卡模型

**model.config**
- 模型名称：Pickup
- 版本：1.0
- SDF版本：1.6
- 作者：Nate Koenig
- 描述：皮卡卡车

**model.sdf**
- 模型名称：pickup
- 静态模型：true
- 碰撞体和视觉：使用meshes/pickup.dae网格
- 旋转：绕Z轴旋转-1.57079632679弧度（-90度）

**meshes/pickup.dae**
- COLLADA格式的3D网格模型

**materials/textures/**
- pickup_diffuse.jpg - 车身漫反射贴图
- wheels2.jpg - 轮胎贴图

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

**metadata.pbtxt**
- 元数据文件

#### sonoma_raceway - 索诺玛赛车场模型

**model.config**
- 模型名称：Sonoma Raceway
- 版本：1.0
- SDF版本：1.6
- 作者：Ian Chen, Cole Biesemeyer
- 描述：索诺玛赛车场模型

**model.sdf**
- 模型名称：sonoma_raceway
- 静态模型：true
- 位置：(0, 0, -4.8)
- 碰撞体和视觉：使用meshes/Raceway.obj网格
- 缩放：0.0254比例因子
- 网格URI：https://fuel.ignitionrobotics.org/1.0/openrobotics/models/sonoma raceway/2/files/meshes/Raceway.obj

**meshes/Raceway.mtl**
- 材质库文件

**meshes/Raceway.obj**
- OBJ格式的3D赛车场网格模型

**materials/textures/**
- Asphalt.png - 沥青路面
- Bridge.png - 桥梁
- Checker.png - 方格旗
- Concrete.png - 混凝土
- Fence.png - 栅栏
- Fence_Opacity.png - 栅栏透明度
- Grass.png - 草地
- Railing.png - 栏杆
- Roof.png - 屋顶
- RumbleStrip&Barrier.png - 凸起路标与障碍物
- RumbleStrip.png - 凸起路标
- Stands.png - 观众看台
- TireStack.png - 轮胎堆
- Track.png - 赛道
- Trim.png - 装饰条
- Wall.png - 墙壁
- Window.png - 窗户

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

### models_docker文件夹 - Docker专用模型库

此文件夹包含针对Docker环境优化的模型版本。

#### hatchback (2/) - Docker版本两厢车

**model.config**
- 模型名称：Hatchback
- 版本：1.0
- SDF版本：1.6
- 作者：Nate Koenig
- 描述：两厢车模型

**model.sdf**
- 模型名称：hatchback
- 静态模型：true
- 碰撞体和视觉：使用meshes/hatchback.obj网格
- 旋转：绕Z轴旋转1.57079632679弧度（90度）
- 缩放：0.0254比例因子

**meshes/hatchback.mtl**
- 材质库文件

**meshes/hatchback.obj**
- OBJ格式的3D网格模型

**materials/textures/**
- hatchback.png - 车身纹理
- wheels3.png - 轮胎纹理

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### prius hybrid (2/) - 丰田普锐斯混合动力车

**model.config**
- 模型名称：Prius Hybrid
- 版本：1.0
- SDF版本：1.6
- 作者：Ian Chen
- 描述：丰田普锐斯混合动力车

**model.sdf**
- 模型名称：prius_hybrid
- 位置：(0, 0, 0.03)
- 车身链接（chassis）：
  - 质量：1326.0 kg
  - 质心位置：(0, -0.266, 0.48)
  - 惯性矩阵：ixx=2581.13, iyy=591.31, izz=2681.95
- 视觉组件：
  - chassis_visual - 车身外观
  - interior_visual - 内饰
  - windows_visual - 车窗
  - 所有使用Hybrid.obj网格
- 碰撞体：
  - chassis - 主车身
  - front_bumper - 前保险杠
  - hood - 引擎盖
  - windshield - 挡风玻璃
  - top_front - 顶部前部
  - top_rear - 顶部后部
- 网格URI：https://fuel.ignitionrobotics.org/1.0/openrobotics/models/prius hybrid/2/files/meshes/Hybrid.obj
- 缩放：0.01比例因子

**meshes/Hybrid.mtl**
- 材质库文件

**meshes/Hybrid.obj**
- OBJ格式的3D网格模型

**materials/textures/**
- Hybrid.png - 混合动力车纹理
- Hybrid_Interior.png - 内饰纹理
- Wheels3.png - 轮胎纹理

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### prius hybrid with sensors (4/) - 带传感器的普锐斯

**model.config**
- 模型名称：Prius Hybrid with sensors
- 版本：1.0
- SDF版本：1.6
- 作者：Ian Chen
- 依赖：model://prius_hybrid
- 描述：带传感器的丰田普锐斯混合动力车

**model.sdf**
- 模型名称：prius_hybrid_sensors
- 包含：prius_hybrid模型
- 传感器链接（sensors）：
  - 通过固定关节连接到prius_hybrid::chassis
- 传感器配置：
  - back_camera_sensor - 后置摄像头
    - 更新率：30 Hz
    - 分辨率：800x800
    - 格式：R8G8B8
    - 视场角：1.39626弧度（80度）
    - 范围：0.02-300米
    - 噪声：高斯噪声，均值0，标准差0.007
    - 位置：(0, 1.45, 1.4)
  - back_left_far_sonar_sensor - 后左远距离超声波传感器
    - 类型：ray（光线传感器）
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 位置：(0.7, 2.4, 0.5)
  - back_left_middle_sonar_sensor - 后左中距离超声波传感器
    - 类型：ray
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 可视化：true
    - 位置：(0.24, 2.4, 0.5)
  - back_right_far_sonar_sensor - 后右远距离超声波传感器
    - 类型：ray
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 位置：(-0.7, 2.4, 0.5)
  - back_right_middle_sonar_sensor - 后右中距离超声波传感器
    - 类型：ray
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 可视化：true
    - 位置：(-0.24, 2.4, 0.5)
  - front_left_sonar_sensor - 前左超声波传感器
    - 类型：ray
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 位置：(0.7, -2.4, 0.5)
  - front_right_sonar_sensor - 前右超声波传感器
    - 类型：ray
    - 更新率：5 Hz
    - 范围：0.2-5米
    - 分辨率：0.1
    - 位置：(-0.7, -2.4, 0.5)

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

#### sonoma raceway (2/) - Docker版本赛车场

**model.config**
- 模型名称：Sonoma Raceway
- 版本：1.0
- SDF版本：1.6
- 作者：Ian Chen, Cole Biesemeyer
- 描述：索诺玛赛车场模型

**model.sdf**
- 模型名称：sonoma_raceway
- 静态模型：true
- 位置：(0, 0, -4.8)
- 碰撞体和视觉：使用meshes/Raceway.obj网格
- 缩放：0.0254比例因子
- 网格URI：https://fuel.ignitionrobotics.org/1.0/openrobotics/models/sonoma raceway/2/files/meshes/Raceway.obj

**meshes/Raceway.mtl**
- 材质库文件

**meshes/Raceway.obj**
- OBJ格式的3D赛车场网格模型

**materials/textures/**
- Asphalt.png - 沥青路面
- Bridge.png - 桥梁
- Checker.png - 方格旗
- Concrete.png - 混凝土
- Fence.png - 栅栏
- Fence_Opacity.png - 栅栏透明度
- Grass.png - 草地
- Railing.png - 栏杆
- Roof.png - 屋顶
- RumbleStrip&Barrier.png - 凸起路标与障碍物
- RumbleStrip.png - 凸起路标
- Stands.png - 观众看台
- TireStack.png - 轮胎堆
- Track.png - 赛道
- Trim.png - 装饰条
- Wall.png - 墙壁
- Window.png - 窗户

**thumbnails/**
- 1.png, 2.png, 3.png, 4.png, 5.png - 模型缩略图

### worlds文件夹 - Gazebo世界文件

**default.sdf**
- 世界名称：default
- 物理参数：
  - 求解器：ODE
  - 最大步长：0.004秒
  - 实时因子：1.0
  - 实时更新率：250 Hz
- 插件系统：
  - gz-sim-physics-system - 物理引擎
  - gz-sim-user-commands-system - 用户命令
  - gz-sim-scene-broadcaster-system - 场景广播
  - gz-sim-contact-system - 接触检测
  - gz-sim-imu-system - 惯性测量单元
  - gz-sim-air-pressure-system - 气压计
  - gz-sim-magnetometer-system - 磁力计
  - gz-sim-apply-link-wrench-system - 应用力
  - gz-sim-navsat-system - 导航卫星
  - gz-sim-sensors-system - 传感器系统（渲染引擎：ogre2）
- 环境参数：
  - 重力：0 0 -9.8 m/s²
  - 地磁场：6e-06 2.3e-05 -4.2e-05
  - 大气模型：adiabatic（绝热）
- 场景设置：
  - 网格：可见
  - 环境光：0.4 0.4 0.4 1
  - 背景：0.7 0.7 0.7 1
  - 阴影：开启
- 地面平面：100x100米白色平面
- 太阳光源：
  - 类型：directional（方向光）
  - 位置：(0, 0, 500)
  - 方向：(0.001, 0.625, -0.78)
  - 强度：1
  - 漫反射：0.904 0.904 0.904 1
  - 镜面反射：0.271 0.271 0.271 1
  - 衰减范围：2000米
- 测试目标：红色立方体（1.5x1.5x1.5米）位于(285, -145, 0.5)
- 坐标系统：
  - 表面模型：EARTH_WGS84
  - 世界帧方向：ENU
  - 纬度：47.397971057728974度
  - 经度：8.546163739800146度
  - 海拔：0米

**default_docker.sdf**
- 与default.sdf内容相同
- 用于Docker容器内的仿真环境

### __pycache__文件夹 - Python缓存

**KeyPressModule.cpython-310.pyc**
- Python字节码缓存文件
- 对应KeyPressModule.py模块
- Python版本：3.10

## 项目核心功能

### 1. 无人机飞行控制
- **MAVSDK集成**：通过MAVSDK协议实现无人机控制
- **手动控制模式**：支持滚转/俯仰/偏航/油门四自由度控制
- **飞行状态监控**：实时显示飞行模式信息
- **安全控制**：武装/降落控制

### 2. 2轴云台相机系统
- **硬件修改**：通过setup_gimbal.py修改x500_depth无人机模型
- **关节配置**：
  - 偏航关节（gimbal_yaw_joint）：Z轴旋转，-90°~90°
  - 俯仰关节（gimbal_pitch_joint）：Y轴旋转，-90°~30°
- **控制接口**：Gazebo transport话题
  - `/gimbal/cmd_pitch` - 俯仰控制
  - `/gimbal/cmd_yaw` - 偏航控制
- **初始设置**：俯仰角45度向下

### 3. YOLOv8实时目标检测
- **模型**：YOLOv8m.pt（中等模型）
- **检测类别**：人（class 0）、汽车（class 2）
- **性能**：实时视频流处理
- **可视化**：可调整大小的检测窗口

### 4. 移动目标模拟
- **汽车模型**：hatchback_blue_1
- **运动轨迹**：圆周运动
- **参数配置**：
  - 圆心：(280.0, -140.0)
  - 半径：15米
  - 速度：5 m/s
  - 周期：约18.8秒/圈

### 5. Docker容器化部署
- **镜像构建**：基于ROS 2 Humble Desktop Full
- **完整环境**：包含PX4、ROS 2、Gazebo、Python依赖
- **GPU加速**：支持NVIDIA GPU passthrough
- **X11转发**：支持图形界面显示
- **多面板管理**：tmuxinator统一管理6个终端面板
