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

# For physical button
import RPi.GPIO as GPIO
import time
import serial

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
        # config
        #self.led_pin = 7
        self.btn_pin_one = 12
        self.GPIO.setmode(GPIO.BOARD)
        #self.setup(self.led_pin, GPIO.OUT)
        self.setup(self.btn_pin_one, GPIO.IN)

    def send_ping(self):
        self.last_send_time = time.time()
        self.pub.publish(self.state_msg)

    def reset_cb(self, request, response):
        print("reset")
        self.state_msg.pressed = False
        self.send_ping()
        return response

    def setup_button(self):
        self.port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)
        if self.port.is_open:
            print('Port is connected')
        else:
            print('ERROR: Check serial port')

    def main(self):
        self.setup_button()
        print("Press to activate call button. Ctrl-C to exit.")
        self.send_ping()
        try:
            while True:
                rclpy.spin_once(self, timeout_sec=0.1)
                # read status of pin and assign to self.state_msg.pressed
                self.state_msg.pressed = GPIO.input(self.btn_pin_one)
                print("Button State:  " + self.state_msg.pressed)
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
