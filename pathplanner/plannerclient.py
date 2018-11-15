#! /usr/bin/env python
"""
Planner Client
<ybingcheng@gmail.com>

todo:
- add waypoints
- add server cutoff
"""
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class PlannerClient(object):
    def __init__(self):
        self.client = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)
        self.client.wait_for_server()

    def go_goal(self, goal):
        """
        Prepare a coordinate, send to robot, and wait.
        """
        # Send goal and wait for result
        self.client.send_goal(goal)
        self.client.wait_for_result()
        if not self.client.wait_for_result():
            rospy.logerr('Action server not available!')
            rospy.signal_shutdown('Action server not available!')
        else:
            rospy.loginfo('HURRAY Goal completed!')

    def prepare_goal(self, coordx, coordy, oriz, oriw):
        """
        Prepare goal.
        """
        # Create goal object
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        # goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        # Goal coordinates
        goal.target_pose.pose.position.x = coordx
        goal.target_pose.pose.position.y = coordy
        goal.target_pose.pose.orientation.z = oriz
        goal.target_pose.pose.orientation.w = oriw
        rospy.loginfo('Set goal (x,y,z,w): %s, %s, %s, %s' % (
                goal.target_pose.pose.position.x,
                goal.target_pose.pose.position.y,
                goal.target_pose.pose.orientation.z,
                goal.target_pose.pose.orientation.w))
        return goal


if __name__ == '__main__':
    try:
        rospy.init_node('pathclient')
        pc = PlannerClient()

        goalone = pc.prepare_goal(3.65, 5.03, 0.60, 0.80)
        pc.go_goal(goalone)

    except rospy.ROSInterruptException:
        rospy.loginfo("Interrupt")
