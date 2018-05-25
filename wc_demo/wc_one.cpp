#include <chrono>
#include <iostream>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"

using std::placeholders::_1;

using namespace std::chrono_literals;

class ChatSpotter : public rclcpp::Node
{
public:
    ChatSpotter(): Node("chatspotter")
    {
        // pub
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel");
        
        // sub
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "chatter",std::bind(&ChatSpotter::topic_callback, this, _1));
    }

private:
    void topic_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
        auto move_msg = geometry_msgs::msg::Twist();
        move_msg.angular.z = 1;
        RCLCPP_INFO(this->get_logger(), "Moving: '%f'", move_msg.angular.z);
        if (msg->data == "Alert")
        {
            publisher_->publish(move_msg);
        } 
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    //rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ChatSpotter>());
    rclcpp::shutdown();
    return 0;
}