from time import sleep

import rclpy

from std_msgs.msg import String

# We do not recommend this style as ROS 2 provides timers for this purpose,
# and it is recommended that all nodes call a variation of spin.
# This example is only included for completeness because it is similar to examples in ROS 1.
# For periodic publication please see the other examples using timers.


def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('minimal_publisher')

    publisher = node.create_publisher(String, 'topic')

    msg = String()

    i = 0
    while rclpy.ok():
        msg.data = 'Hello World: %d' % i
        i += 1
        node.get_logger().info('Publishing: "%s"' % msg.data)
        publisher.publish(msg)
        sleep(0.5)  # seconds

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()