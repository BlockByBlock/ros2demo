#include <iostream>
#include <memory>

#include "rclcpp/rclcpp.hpp"

#include "std_msgs/msg/string.hpp"

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);   // init ros node
    auto node = rclcpp::Node::make_shared("talker");  // create node
    auto pub = node->create_publisher<std_msgs::msg::String>("chatter");    
    auto msg = std::make_shared<std_msgs::msg::String>();   // msg
    auto publish_count = 0;
    rclcpp::WallRate loop_rate(1);  // timer

    if(rclcpp::ok()) 
    {
        msg->data = "Hello world! " + std::to_string(publish_count++);   // load data
        RCLCPP_INFO(node->get_logger(), "Publishing: '%s'", msg->data.c_str())
        pub->publish(msg);  // publish message
        // spin_some: Do all the work that is immediately available to the executor
        rclcpp::spin_some(node);    
        loop_rate.sleep();  // rate
    }
    rclcpp::shutdown();
    return 0;
}