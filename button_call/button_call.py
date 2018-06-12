import rclpy
from rclpy.node import Node

#from std_msgs.msg import String
from rmf_msgs.msg import CallButtonState

class ButtonCall(Node):

    def __init__(self):
        super().__init__('button_node')
        self.publisher_ = self.create_publisher(CallButtonState, 'button')
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = CallButtonState()
        msg.id = 'Hello World!'
        msg.pressed = True
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s @ %s"' %(msg.id,msg.pressed))


def main(args=None):
    rclpy.init(args=args)

    button_call = ButtonCall()

    rclpy.spin(button_call)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    button_call.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()