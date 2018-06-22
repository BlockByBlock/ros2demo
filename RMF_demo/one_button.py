#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

# ROS library
import rclpy
from std_msgs.msg import String
from rmf_msgs.msg import CallButtonState

# GPIO declaration
LED_PIN_0 = 7
LED_PIN_1 = 11
BTN_PIN_0 = 12
BTN_PIN_1 = 16
# BTN_PIN_2 = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN_0,GPIO.OUT)
GPIO.setup(LED_PIN_1,GPIO.OUT)
GPIO.setup(BTN_PIN_0,GPIO.IN)
GPIO.setup(BTN_PIN_1,GPIO.IN)
# GPIO.setup(BTN_PIN_2,GPIO.IN)

btn_state_0 = False
btn_state_1 = False
# btn_state_2 = False
bed_dict = {12:"bed_0_button", 16:"bed_1_button", 18:"bed_2_button"}

def main(args=None):
    # ROS init
    rclpy.init(args=args)
    node = rclpy.create_node('button_node')
    publisher = node.create_publisher(CallButtonState, 'call_button_state')
    msg_0 = CallButtonState()
    msg_1 = CallButtonState()

    try:

        while rclpy.ok():
            btn_state_0 = GPIO.input(BTN_PIN_0)
            btn_state_1 = GPIO.input(BTN_PIN_1)
            # btn_state_2 = GPIO.input(BTN_PIN_2)

            # Update & publish msg
            msg_0.id = bed_dict[BTN_PIN_0]
            msg_0.pressed = bool(btn_state_0)
            msg_1.id = bed_dict[BTN_PIN_1]
            msg_1.pressed = bool(btn_state_1)
            node.get_logger().info("%s,%s" % (msg_0.id,msg_0.pressed))
            node.get_logger().info("%s,%s" % (msg_1.id,msg_1.pressed))
            publisher.publish(msg_0)
            publisher.publish(msg_1)

            # Update LEDs
            if btn_state_0 == True:
                GPIO.output(LED_PIN_0,GPIO.HIGH)
            else:
                GPIO.output(LED_PIN_0,GPIO.LOW)
            if btn_state_1 == True:
                GPIO.output(LED_PIN_1,GPIO.HIGH)
            else:
                GPIO.output(LED_PIN_1,GPIO.LOW)

            time.sleep(0.2)
            
    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()
        GPIO.cleanup()
        print("Cleaned up!")

if __name__ == '__main__':
    main()
