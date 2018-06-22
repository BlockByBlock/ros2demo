# raspi version
#ssh into raspi

ssh songshan@192.168.1.85

#On Raspi
cd ~/rmf/src && git clone https://github.com/songshan0321/RMF_demo.git

cd ~/rmf_ws && . install/setup.bash

export ROS_DOMAIN_ID=1

cd ~/rmf_ws && ament build --symlink-install --only-packages one_button

one_button



# nanopi and comp version, connect nanopi to comp using USB to UART converter

#ssh into nanopi

ssh root@192.168.1.21

#On nanoPi

cd ~/demo && python3 ./serialButton.py

#On COM

cd ~/ros2_ws && . install/local_setup.bash

cd ~/Downloads/RMF_demo && python3 ./button_pub.py
