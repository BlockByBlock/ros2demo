#! /usr/bin/env python

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initailize(sys.argv)
rospy.init_node('demo_manipulator', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("manipulator")
display_trajecttory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

pose_target = geometry_msgs.msg.Pose()
pose_target.orientation.w = 1.0
pose_target.position.x = 0.3
pose_target.position.y = 0
pose_target.position.z = 1.1
group.set_pose_target(pose_target)

plan1 = group.plan()

rospy.sleep(3)

moveit_commander.roscpp_shutdown()
