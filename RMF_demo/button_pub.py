import serial
import time

# ROS library
import rclpy
from std_msgs.msg import String

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)

def main(args=None):
    # ROS init
    rclpy.init(args=args)
    node = rclpy.create_node('button_node')
    publisher = node.create_publisher(String, 'button')
    msg = String()    

    while rclpy.ok():
        rcv = port.readline()
        print("Read: " + repr(rcv)[2:-3])
        msg.data = repr(rcv)[2:-3]
        node.get_logger().info("%s" % msg.data)
        publisher.publish(msg)
        time.sleep(0.1)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()