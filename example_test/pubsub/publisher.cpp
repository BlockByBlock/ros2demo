#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

/* 
New node pass through initiate constructor
Lambda function in constructor
*/

class NewPublisher : public rclcpp::Node
{
public:
    NewPublisher(): Node("talker"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter");
        auto timer_callback =
            [this]() -> void {
                auto msg = std_msgs::msg::String();
                msg.data = "Hello, world! " + std::to_string(this->count_++);
                RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str())
                this->publisher_->publish(msg);
            };
        timer_ = this->create_wall_timer(1000ms, timer_callback);
    }

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NewPublisher>());
    rclcpp::shutdown();
    return 0;
}