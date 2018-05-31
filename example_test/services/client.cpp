#include <chrono>
#include <cinttypes>
#include <memory>
#include "say_hello/srv/say_hello.hpp"
#include "rclcpp/rclcpp.hpp"

using SayHello = say_hello::srv::SayHello;

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("bye");
  auto client = node->create_client<SayHello>("hellobye");
  while (!client->wait_for_service(std::chrono::seconds(1))) {
    if (!rclcpp::ok()) {
      RCLCPP_ERROR(node->get_logger(), "client interrupted while waiting for service to appear.")
      return 1;
    }
    RCLCPP_INFO(node->get_logger(), "waiting for service to appear...")
  }
  auto request = std::make_shared<SayHello::Request>();
  request->hello = "Hello World!";
  auto result_future = client->async_send_request(request);
  if (rclcpp::spin_until_future_complete(node, result_future) !=
    rclcpp::executor::FutureReturnCode::SUCCESS)
  {
    RCLCPP_ERROR(node->get_logger(), "service call failed :(")
    return 1;
  }
  auto result = result_future.get();
  RCLCPP_INFO(node->get_logger(), "Send %s , Receive %s",
    request->hello.c_str(), result->bye.c_str())
  rclcpp::shutdown();
  return 0;
}