# Minimal python publisher for Call Button 

Learning points

* Depending on the method of invoking the executable (.py), there has to be modification to the directory

If you are trying to call ros2 run ... that won’t work since that command expects the executable to be in the path <install-prefix>/lib/<pkgname>. The script is likely being installed into <install-prefix>/bin and is therefore already on the PATH. You should be able to invoke the executable directly using just the name.

* ros2 run <pkg> <executable> <--- this requires a setup.cfg file to install in the /lib directory

e.g.
[develop]
script-dir=$base/lib/button_call
[install]
install-scripts=$base/lib/button_call

* run by python3 ./<executable> if compile without setup.cfg

# Connect nanopi to comp using USB to UART converter

# ssh into nanopi
ssh root@192.168.1.21

# On Pi
cd ~/demo && python3 ./serialButton.py

# On COM
cd ~/ros2_ws && . install/local_setup.bash
cd ~/Downloads/RMF_demo && python3 ./button_pub.py
