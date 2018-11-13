#! /usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback

class PlannerServer(object):
    # todo: action server msg if any

    # init 
    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(
            'move_base', 
            move_base_msgs.msg.MoveBaseAction,
            execute_cb = self.execute_cb,
            auto_start = False
        )
        self._as.start()

    # callback
    def execute_cb(self, goal):
        r = rospy.Rate(1)
        success = True

        # todo: init action server msg

        # start executing the action
        for i in range(1, goal.order):
            # check if preempt has not been requested by client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            # append action server msg
            # publish feedback
            r.sleep()
        
    #if success:

if __name__ == '__main__'
    rospy.init_node('pathscripting')
    server = PathPlanning(rospy.get_name())
    rospy.spin()