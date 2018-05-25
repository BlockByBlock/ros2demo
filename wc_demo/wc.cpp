#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

// Pub
class TwistPub : public rclcpp::Node
{
public:
    TwistPub(): Node("twist_publisher")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel");
        auto timer_callback =
            [this]() -> void {
                auto msg = geometry_msgs::msg::Twist();
                //msg.linear.x = 1;
                msg.angular.z = 0.5;
                RCLCPP_INFO(this->get_logger(), "Moving: '%f'", msg.angular.z);
                this->publisher_->publish(msg);
            };
        timer_ = this->create_wall_timer(1000ms, timer_callback);
    }

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
};

// Sub
class ChatterSub : public rclcpp::Node
{
public:
    ChatterSub(): Node("chatter_sub")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "chatter",
            [this](std_msgs::msg::String::UniquePtr msg) {
            RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
            
        });
    }

private:
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::executors::SingleThreadedExecutor exec;
    auto twist_pub = std::make_shared<TwistPub>();
    auto chatter_sub = std::make_shared<ChatterSub>();
    exec.add_node(twist_pub);
    exec.add_node(chatter_sub);
    exec.spin();
    rclcpp::shutdown();
    return 0;
}