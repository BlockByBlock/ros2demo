# Connect nanopi to comp using USB to UART converter

# ssh into nanopi
ssh root@192.168.1.21

# On Pi
cd ~/demo && python3 ./serialButton.py

# On COM
cd ~/ros2_ws && . install/local_setup.bash
cd ~/Downloads/RMF_demo && python3 ./button_pub.py
