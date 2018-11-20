#! /usr/bin/env python
"""
Planner Client
<ybingcheng@gmail.com>

todo:
- repeat cycle
- add marker on rviz

wpmark.pose.position.x
wpmark.pose.position.y
"""
import rospy
import actionlib
import yaml
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped
# from visualization_msgs.msg import Marker


class PlannerClient(object):
    def __init__(self):
        self.path = list()
        self.initpose = list()
        self.client = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)
        self.initpub = rospy.Publisher(
            'initialpose', PoseWithCovarianceStamped, queue_size=10)
        # self.wpmark = rospy.Publisher(
        #         'frame', Marker, queue_size=10)

    def start(self):
        print('Connect to Action Server ..')
        self.client.wait_for_server()

    def load_config_file(self, filename):
        try:
            f = open(filename, 'r')
            config = yaml.safe_load(f)
        except yaml.YAMLError as ex:
            print(ex)
            return False

        f.close()

        self.path = config['journey']['waypoints']
        self.initpose = config['journey']['initpose']

        print('Initialising position at {}').format(self.initpose)

        print ('Your itinerary in position(x, y) & orientation(z, w):')
        for step in range(len(self.path)):
            print ("Step {}: {}").format(step+1, self.path[step])

        return True

    def init_manager(self):
        """
        Init position based on config file.
        """
        startpose = PoseWithCovarianceStamped()
        startpose.header.frame_id = 'map'
        startpose.pose.pose.position.x = self.initpose[0][0]
        startpose.pose.pose.position.y = self.initpose[0][1]
        startpose.pose.pose.position.z = 0
        startpose.pose.pose.orientation.z = self.initpose[0][2]
        startpose.pose.pose.orientation.w = self.initpose[0][3]

        rospy.sleep(1)
        self.initpub.publish(startpose)

        rospy.loginfo('Init @ (x,y,z,w): %s, %s, %s, %s' % (
                    startpose.pose.pose.position.x,
                    startpose.pose.pose.position.y,
                    startpose.pose.pose.orientation.z,
                    startpose.pose.pose.orientation.w))

    def goal_manager(self):
        """
        Prepare goal. Send Goal.
        """
        for step in range(len(self.path)):
            # Create goal object
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = 'map'
            # goal.target_pose.header.frame_id = 'base_link'
            goal.target_pose.header.stamp = rospy.Time.now()
            # Goal coordinates
            goal.target_pose.pose.position.x = self.path[step][0]
            goal.target_pose.pose.position.y = self.path[step][1]
            goal.target_pose.pose.orientation.z = self.path[step][2]
            goal.target_pose.pose.orientation.w = self.path[step][3]
            rospy.loginfo('Set goal (x,y,z,w): %s, %s, %s, %s' % (
                    goal.target_pose.pose.position.x,
                    goal.target_pose.pose.position.y,
                    goal.target_pose.pose.orientation.z,
                    goal.target_pose.pose.orientation.w))

            # Send goal and wait for result
            self.client.send_goal(goal)
            self.client.wait_for_result()
            if not self.client.wait_for_result():
                rospy.logerr('Action server not available!')
                rospy.signal_shutdown('Action server not available!')
            else:
                print('STATUS: step{} completed!').format(step+1)
                rospy.loginfo('HURRAY goal completed!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage:   plannerclient.py CONFIG.yaml')
        print('example: plannerclient.py config/journey.yaml')
        sys.exit(1)

    try:
        rospy.init_node('pathclient')
        pc = PlannerClient()

        if not pc.load_config_file(sys.argv[1]):
            print("INVALID journey configuration file!")
            sys.exit(1)

        pc.init_manager()
        pc.start()
        pc.goal_manager()

    except rospy.ROSInterruptException:
        rospy.loginfo("Interrupt")
