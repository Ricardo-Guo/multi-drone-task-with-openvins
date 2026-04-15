import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry, TrajectorySetpoint, OffboardControlMode
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

class SwarmFollower(Node):
    def __init__(self):
        super().__init__('swarm_follower_node')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # 1. 订阅 Leader (px4_0)
        self.leader_sub = self.create_subscription(
            VehicleOdometry,
            '/px4_0/fmu/out/vehicle_odometry', # 统一使用 odometry 保证字段一致
            self.leader_cb,
            qos_profile)

        # 2. 发布给 Follower (px4_1)
        self.follower_sp_pub = self.create_publisher(
            TrajectorySetpoint,
            '/px4_1/fmu/in/trajectory_setpoint',
            qos_profile)
        
        self.follower_mode_pub = self.create_publisher(
            OffboardControlMode,
            '/px4_1/fmu/in/offboard_control_mode',
            qos_profile)

        # 初始状态
        self.leader_pos = [0.0, 0.0, 0.0]
        # 修改：提升到 20Hz (0.05s) 模仿 MAVSDK 的高频心跳
        self.timer = self.create_timer(0.05, self.cmd_loop)  

    def leader_cb(self, msg):
        # 记录 Leader 坐标
        self.leader_pos = [float(msg.position[0]), float(msg.position[1]), float(msg.position[2])]

    def cmd_loop(self):
        # --- 发布 Offboard 控制模式心跳 ---
        off_msg = OffboardControlMode()
        off_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        off_msg.position = True
        off_msg.velocity = False
        off_msg.acceleration = False
        off_msg.attitude = False
        off_msg.body_rate = False
        self.follower_mode_pub.publish(off_msg)

        # --- 计算并发布目标点 ---
        sp = TrajectorySetpoint()
        
        # 坐标偏置逻辑
        # initial_offset_x: yml中两机的起始差值 (282 - 280 = 2.0)
        # follow_dist: 你希望它跟在 Leader 后面几米
        initial_offset_x = 2.0
        follow_dist = 2.0  
        
        # 计算 X, Y
        target_x = float(self.leader_pos[0] - initial_offset_x - follow_dist)
        target_y = float(self.leader_pos[1])
        
        # 计算 Z (高度修正)
        # 如果 Leader 在地面 (Z=0)，给 Follower 一个起飞高度 -1.5m (NED系负数代表向上)
        target_z = float(self.leader_pos[2])
        if target_z > -1.0: 
            target_z = -1.5 # 强制起飞到 1.5 米高度
        
        sp.position = [target_x, target_y, target_z]
        sp.yaw = 0.0 # 保持正前方，不乱转
        sp.timestamp = off_msg.timestamp
        
        self.follower_sp_pub.publish(sp)
        
        # 调试信息
        # self.get_logger().info(f"Leader Z: {self.leader_pos[2]:.2f} | Target: [{target_x:.2f}, {target_y:.2f}, {target_z:.2f}]")

def main():
    rclpy.init()
    node = SwarmFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
