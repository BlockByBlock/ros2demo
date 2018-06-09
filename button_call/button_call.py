# Note the python3 header declaration is missing. Add if require.

# Shan's required library
from time import sleep
import RPi.GPIO as GPIO
import serial

# ROS library
import rclpy
from std_msgs.msg import Float32

def main(args=None):
    # ROS init
    rclpy.init(args=args)
    node = rclpy.create_node('button_node')
    publisher = node.create_publisher(String, 'button')
    msg = Float32()     # To minimize in the future

    # Nanopi - declaration and configuration
    LED_PIN = 7
    BTN_PIN_1 = 12
    BTN_PIN_2 = 16
    BTN_PIN_3 = 18
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN,GPIO.OUT)
    GPIO.setup(BTN_PIN_1,GPIO.IN)
    GPIO.setup(BTN_PIN_2,GPIO.IN)
    GPIO.setup(BTN_PIN_3,GPIO.IN)

    bed_dict = {12:"B01", 16:"B02", 18:"B03"}
    logic_dict = {True:"S1", False:"S0"}

    counter = 0
    
    # Loop
    while rclpy.ok():
        # button
        btn_state_1 = GPIO.input(BTN_PIN_1)
	    btn_state_2 = GPIO.input(BTN_PIN_2)
	    btn_state_3 = GPIO.input(BTN_PIN_3)

        print(bed_dict[BTN_PIN_1] + logic_dict[btn_state_1] + "  " + bed_dict[BTN_PIN_2] + logic_dict[btn_state_2] + "  " + bed_dict[BTN_PIN_3] + logic_dict[btn_state_3])

        if btn_state_1 == True or btn_state_2 == True or btn_state_3 == True:
            GPIO.output(LED_PIN,True)
            if counter == 5:
                GPIO.output(LED_PIN,False)
            elif counter == 7:
                GPIO.output(LED_PIN,True)
            elif counter == 9:
                GPIO.output(LED_PIN,False)
            elif counter == 10:
                counter = 5
            counter += 1
        else:
            GPIO.output(LED_PIN,False)
            counter = 0

        sleep(0.5)  # Not sure if this is too much? 

        msg.data = float(counter)   # To put in correct variable
        node.get_logger().info('Publishing: "%d"' % msg.data)
        publisher.publish(msg)
        sleep(0.5)  # seconds

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()