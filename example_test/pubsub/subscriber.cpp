#include <iostream>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

/* 
New node pass through initiate constructor
Lambda function in constructor
*/

class NewSubscriber : public rclcpp::Node
{
public:
    NewSubscriber(): Node("listener")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "chatter",
            [this](std_msgs::msg::String::UniquePtr msg) {
            RCLCPP_INFO(this->get_logger(), "I heard: %s", msg->data.c_str())
        });
    }

private:
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NewSubscriber>());
    rclcpp::shutdown();
    return 0;
}
