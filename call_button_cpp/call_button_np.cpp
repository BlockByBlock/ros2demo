#include <chrono>
#include <wiringPi.h>
#include <iostream.h>

// ROS
#include "rclcpp/rclcpp.hpp"
#include "rmf_msgs/msg/CallButtonState.hpp"

using namespace std::chrono_literals;

class CallButton : public HelpButton, public rclcpp::Node
{
public:
    CallButton(): HelpButton(), Node("talker"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter");
        auto timer_callback =
            [this]() -> void {
                auto msg = rmf_msgs::msg::CallButtonState();
                // Button
                btn_state = digitalRead(btn_pin);   // Return integer
                msg.pressed = (btn_state > 0)? true : false;
                if(msg.pressed == true)
                {
                    digitalWrite(led_pin, HIGH);
                }
                else
                {
                    digitalWrite(led_pin, LOW);
                }
                std::cout << "Reading from button: " << msg.pressed << std::endl;     
                RCLCPP_INFO(this->get_logger(), "ROS2 Pub: '%s'", msg.pressed)
                this->publisher_->publish(msg);
            };
        timer_ = this->create_wall_timer(1000ms, timer_callback);
    }
    // Reset call button function
    // Ping function

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

class HelpButton
{
public:
    HelpButton(): led_pin(7), btn_pin(12), btn_state(0)
    {
        wiringPiSetupPhys();
        pinMode(led_pin, OUTPUT);
        pinMode(btn_pin, INPUT);
    }
private:
    int led_pin;
    int btn_pin;
    int btn_state;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CallButton>());
    rclcpp::shutdown();
    return 0;
}