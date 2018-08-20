#!/usr/bin/env python3
import time
import rclpy
rclpy.init()
node = rclpy.create_node('list_all_topics_example')
while(1):
    print(node.get_topic_names_and_types(no_demangle=True))
    time.sleep(.5)
