#include <inttypes.h>
#include <memory>
#include "say_hello/srv/say_hello.hpp"
#include "rclcpp/rclcpp.hpp"

using SayHello = say_hello::srv::SayHello;
rclcpp::Node::SharedPtr g_node = nullptr;

void reply_hello(
  const std::shared_ptr<rmw_request_id_t> request_header,
  const std::shared_ptr<SayHello::Request> request,
  const std::shared_ptr<SayHello::Response> response)
{
  (void)request_header;
  RCLCPP_INFO(
    g_node->get_logger(),
    "I receive: %s", request->hello.c_str())
  response->bye= "Bye World!";
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  g_node = rclcpp::Node::make_shared("hello");
  auto server = g_node->create_service<SayHello>("hellobye", reply_hello);
  rclcpp::spin(g_node);
  rclcpp::shutdown();
  g_node = nullptr;
  return 0;
}
