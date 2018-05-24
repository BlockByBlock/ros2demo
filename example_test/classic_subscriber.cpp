/* Classic ROS nodes, not recommended */
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

rclcpp::Node::SharedPtr g_node = nullptr;

void topic_callback(const std_msgs::msg::String::SharedPtr msg)
{
  RCLCPP_INFO(g_node->get_logger(), "I heard: '%s'", msg->data.c_str())
}

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv); // init node
    g_node = rclcpp::Node::make_shared("listener"); // create node
    auto subscription = g_node->create_subscription<std_msgs::msg::String>
        ("chatter", topic_callback);
    // spin: Blocking call, do work indefinitely as it comes in 
    rclcpp::spin(g_node); 
    rclcpp::shutdown();
    g_node = nullptr;
    return 0;
}
