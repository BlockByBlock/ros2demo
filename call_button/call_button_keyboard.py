#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rmf_msgs.msg import CallButtonState
from std_srvs.srv import Empty
import select
import sys
import termios
import time
import tty

class CallButtonKeyboard(Node):
    def __init__(self):
        super().__init__('call_button_keyboard')
        self.id = self.get_name()
        self.ping_interval_sec = 1.0  # todo: make it a ROS parameter
        self.pub = self.create_publisher(CallButtonState, 'call_button_state')
        self.reset_srv = self.create_service(Empty, '~/reset', self.reset_cb)
        self.term_settings = termios.tcgetattr(sys.stdin)
        self.state_msg = CallButtonState(id=self.id)
        tty.setcbreak(sys.stdin.fileno())
        self.last_send_time = time.time()

    def send_ping(self):
        self.last_send_time = time.time()
        self.pub.publish(self.state_msg)

    def reset_cb(self, request, response):
        print("reset")
        self.state_msg.pressed = False
        self.send_ping()
        return response

    def main(self):
        print("[spacebar] activates the call button. 'r' to resets it. Ctrl-C to exit.")
        self.send_ping()
        try:
            while True:
                rclpy.spin_once(self, timeout_sec=0.1)
                i, o, e = select.select([sys.stdin], [], [], 0.1)
                if i:
                    key = sys.stdin.read(1)
                    if key == 'r':
                        print("call button reset!")
                        self.state_msg.pressed = False
                    else:
                        print("call button activated!")
                        self.state_msg.pressed = True
                    self.send_ping()
                t = time.time()
                if t > self.last_send_time + self.ping_interval_sec:
                    self.send_ping()
        except KeyboardInterrupt:
            pass  # Ctrl-C was pressed. Time to exit the loop.
        except Exception as e:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.term_settings)
            print(e)
            raise
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.term_settings)

def main(args=None):
    rclpy.init(args=args)
    node = CallButtonKeyboard()
    node.main()

if __name__ == '__main__':
    main()
