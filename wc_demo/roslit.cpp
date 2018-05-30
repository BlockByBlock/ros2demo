#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include "SerialStream.h"

using namespace LibSerial;

rclcpp::Node::SharedPtr g_node = nullptr;

void topic_callback(const std_msgs::msg::String::SharedPtr msg)
{
    RCLCPP_INFO(g_node->get_logger(), "I heard: '%s'", msg->data.c_str())
    if (msg->data == "Alert")
    {
        SerialStream aserial;
        aserial.Open("/dev/ttyACM0");
        aserial.SetBaudRate(SerialStreamBuf::BAUD_9600);
        aserial.SetCharSize(SerialStreamBuf::CHAR_SIZE_8);
        aserial.SetNumOfStopBits(1);
        aserial.SetParity(SerialStreamBuf::PARITY_NONE);
        aserial.SetFlowControl(SerialStreamBuf::FLOW_CONTROL_NONE);
        // Serial Check
        if ( ! aserial.IsOpen() ) 
        {
            std::cerr << "ERROR: could not open port." << std::endl ;
            exit(1) ;
        }  
        aserial << 'a';
    } 
}

int main(int argc, char * argv[])
{ 
    rclcpp::init(argc, argv); // init node
    g_node = rclcpp::Node::make_shared("led_sub"); // create node
    auto subscription = g_node->create_subscription<std_msgs::msg::String>
        ("chatter", topic_callback);
    // spin: Blocking call, do work indefinitely as it comes in 
    rclcpp::spin(g_node); 
    rclcpp::shutdown();
    g_node = nullptr;
    return 0;
}
