#!/usr/bin/env python3
import serial
import sys
import termios
import time
import tty

# ROS lib
import rclpy
from rclpy.node import Node
from rmf_msgs.msg import CallButtonState
from std_srvs.srv import Empty

class PButton:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', baudrate = 9200, timeout = 1)
            print ("CONNECTED!")
        except SerialException:
            import os
            print ("ERROR: Check serial port")
            os.exit(0)

    def close_serial(self):
        self.ser.close()

class CallButtonPub(Node):
    def __init__(self):
        super().__init__('call_button_pub')
        self.id = self.get_name()
        self.ping_interval_sec = 1.0
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
        print("Press to activate call button. Ctrl-C to exit.")
    

def main(args=None):
    rclpy.init(args=args)
    button = PButton()
    node = CallButtonPub()
    node.main()
    button.close_serial()

if __name__ == '__main__':
    main()