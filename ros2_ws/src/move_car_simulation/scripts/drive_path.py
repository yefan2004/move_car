#!/usr/bin/env python3
"""Drive the simulation robot through the room so SLAM can close a loop."""

import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy


WAYPOINTS = [
    (0.7, 1.05),
    (1.5, 1.05),
    (1.5, -1.05),
    (0.75, -1.05),
    (0.75, 1.05),
    (3.25, 1.05),
    (3.25, -1.05),
    (2.45, -1.05),
    (2.45, 1.05),
    (0.7, 0.0),
]


class DrivePath(Node):
    def __init__(self):
        super().__init__('drive_path')
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Odometry, 'odom', self._odom, qos)
        self.pose = None
        self.index = 0
        self.done = False
        self.create_timer(0.1, self._tick)

    def _odom(self, msg):
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            math.atan2(siny, cosy),
        )

    def _tick(self):
        if self.pose is None or self.done:
            return
        if self.index >= len(WAYPOINTS):
            self.publisher.publish(Twist())
            self.done = True
            self.get_logger().info('path done')
            return

        x, y, yaw = self.pose
        target_x, target_y = WAYPOINTS[self.index]
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        if distance < 0.12:
            self.index += 1
          #  self.get_logger().info(f'reached waypoint {self.index}/{len(WAYPOINTS)}')
            return

        heading = math.atan2(dy, dx)
        error = math.atan2(math.sin(heading - yaw), math.cos(heading - yaw))
        command = Twist()
        if abs(error) > 0.45:
            command.angular.z = 0.7 if error > 0.0 else -0.7
        else:
            command.linear.x = 0.16
            command.angular.z = max(-0.8, min(0.8, 1.6 * error))
        self.publisher.publish(command)


def main():
    rclpy.init()
    node = DrivePath()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publisher.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
