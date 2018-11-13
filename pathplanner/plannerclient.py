#! /usr/bin/env python
"""
Planner Client
<ybingcheng@gmail.com>

There are 8 states in action client:
    - Waiting for goal ack
    - Pending
    - Active
    - Waiting for cancel ack
    - Recalling
    - Preempting
    - Waiting for result
    - Done
"""
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class PlannerClient(object):
    def __init__(self):
        self.client = actionlib.SimpleActionClient(
            'move_base', 
            MoveBaseAction
        )
        self.client.wait_for_server()

    def prepare_goal(self):
        """
        Prepare goal. 
        """
        ### Create goal object
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        #goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        ### Goal coordinates
        goal.target_pose.pose.position.x = 0.5
        goal.target_pose.pose.position.y = 0.5
        #goal.target_pose.pose.orientation.w = 1.0
        rospy.loginfo('Goal established at (x,y): %s, %s' % (
                goal.target_pose.pose.position.x,
                goal.target_pose.pose.position.y))
        ### Send goal and wait for result
        client.send_goal(goal)

    def wait_spin(self):
        wait = client.wait_for_result()
        if not wait:
            rospy.logerr('Action server not available!')
            rospy.signal_shutdown('Action server not available!')
        else:
            return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('pathclient')
        pc = PlannerClient()
        pc.wait_spin()

        if result:
            rospy.loginfo("Goal done")
    except rospy.ROSInterruptException:
        rospy.loginfo("Interrupt")
