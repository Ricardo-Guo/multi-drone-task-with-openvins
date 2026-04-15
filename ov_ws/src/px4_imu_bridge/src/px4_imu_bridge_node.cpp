#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/sensor_combined.hpp>
#include <sensor_msgs/msg/imu.hpp>

class Px4ImuBridge : public rclcpp::Node
{
public:
    Px4ImuBridge() : Node("px4_imu_bridge_node")
    {
        auto qos = rclcpp::QoS(rclcpp::KeepLast(10)).best_effort();
        subscription_ = this->create_subscription<px4_msgs::msg::SensorCombined>(
            "/fmu/out/sensor_combined", qos,
            std::bind(&Px4ImuBridge::imu_callback, this, std::placeholders::_1));
        publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("/imu/data_raw", 10);
        RCLCPP_INFO(this->get_logger(), "PX4 IMU Bridge Node has started.");
    }

private:
    void imu_callback(const px4_msgs::msg::SensorCombined::SharedPtr msg)
    {
        auto imu_msg = sensor_msgs::msg::Imu();
        imu_msg.header.stamp = this->get_clock()->now();
        imu_msg.header.frame_id = "imu_link";

        // 坐标系转换: FRD -> ENU
        imu_msg.linear_acceleration.x = msg->accelerometer_m_s2[0];
        imu_msg.linear_acceleration.y = -msg->accelerometer_m_s2[1];
        imu_msg.linear_acceleration.z = -msg->accelerometer_m_s2[2];

        imu_msg.angular_velocity.x = msg->gyro_rad[0];
        imu_msg.angular_velocity.y = -msg->gyro_rad[1];
        imu_msg.angular_velocity.z = -msg->gyro_rad[2];

        publisher_->publish(imu_msg);
    }
    rclcpp::Subscription<px4_msgs::msg::SensorCombined>::SharedPtr subscription_;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Px4ImuBridge>());
    rclcpp::shutdown();
    return 0;
}
