#!/usr/bin/env python3
"""
sensor_monitor.py
Subscribes to IMU, GPS, Camera topics and prints live data to terminal.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix, Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
import time


def quat_to_euler(q):
    """Convert quaternion to roll/pitch/yaw (degrees)."""
    # Roll
    sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    # Pitch
    sinp = 2 * (q.w * q.y - q.z * q.x)
    sinp = max(-1.0, min(1.0, sinp))
    pitch = math.asin(sinp)
    # Yaw
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


class SensorMonitor(Node):
    def __init__(self):
        super().__init__('sensor_monitor')

        # Latest data store
        self.imu_data   = None
        self.gps_data   = None
        self.odom_data  = None
        self.img_count  = 0
        self.cmd_vel    = None

        # Subscribers
        self.create_subscription(Imu,        '/robot/imu/data',   self.imu_cb,  10)
        self.create_subscription(NavSatFix,  '/robot/gps/fix',    self.gps_cb,  10)
        self.create_subscription(Odometry,   '/robot/odom',       self.odom_cb, 10)
        self.create_subscription(Image,      '/robot/front_camera/image_raw', self.img_cb, 10)
        self.create_subscription(Twist,      '/robot/cmd_vel',    self.cmd_cb,  10)

        # Print timer (2 Hz)
        self.create_timer(0.5, self.print_dashboard)
        self.get_logger().info('🤖 Sensor Monitor started — printing every 0.5s')

    # ── Callbacks ────────────────────────────────────────────────────────────
    def imu_cb(self, msg):   self.imu_data  = msg
    def gps_cb(self, msg):   self.gps_data  = msg
    def odom_cb(self, msg):  self.odom_data = msg
    def cmd_cb(self, msg):   self.cmd_vel   = msg
    def img_cb(self, msg):   self.img_count += 1

    # ── Dashboard ────────────────────────────────────────────────────────────
    def print_dashboard(self):
        now = time.strftime('%H:%M:%S')
        lines = [
            '=' * 60,
            f'  🤖 ROBOT SENSOR DASHBOARD   [{now}]',
            '=' * 60,
        ]

        # IMU
        if self.imu_data:
            d = self.imu_data
            roll, pitch, yaw = quat_to_euler(d.orientation)
            ax = d.linear_acceleration.x
            ay = d.linear_acceleration.y
            az = d.linear_acceleration.z
            gx = d.angular_velocity.x
            gy = d.angular_velocity.y
            gz = d.angular_velocity.z
            lines += [
                '📐 IMU',
                f'   Orientation  → Roll:{roll:7.2f}°  Pitch:{pitch:7.2f}°  Yaw:{yaw:7.2f}°',
                f'   Lin.Accel   → X:{ax:6.3f}  Y:{ay:6.3f}  Z:{az:6.3f}  m/s²',
                f'   Ang.Vel     → X:{gx:6.3f}  Y:{gy:6.3f}  Z:{gz:6.3f}  rad/s',
            ]
        else:
            lines.append('📐 IMU          → waiting for data…')

        lines.append('')

        # GPS
        if self.gps_data:
            g = self.gps_data
            status_str = {0:'FIX', 1:'SBAS_FIX', 2:'GBAS_FIX', -1:'NO_FIX'}.get(g.status.status, '?')
            lines += [
                '🛰️  GPS',
                f'   Latitude    → {g.latitude:.8f} °',
                f'   Longitude   → {g.longitude:.8f} °',
                f'   Altitude    → {g.altitude:.3f} m',
                f'   Status      → {status_str}',
            ]
        else:
            lines.append('🛰️  GPS          → waiting for data…')

        lines.append('')

        # Odometry
        if self.odom_data:
            o = self.odom_data
            px = o.pose.pose.position.x
            py = o.pose.pose.position.y
            pz = o.pose.pose.position.z
            vx = o.twist.twist.linear.x
            wz = o.twist.twist.angular.z
            _, _, yaw = quat_to_euler(o.pose.pose.orientation)
            lines += [
                '📍 ODOMETRY',
                f'   Position    → X:{px:7.3f} m  Y:{py:7.3f} m  Z:{pz:7.3f} m',
                f'   Heading     → {yaw:.2f}°',
                f'   Velocity    → Linear:{vx:.3f} m/s  Angular:{wz:.3f} rad/s',
            ]
        else:
            lines.append('📍 Odometry     → waiting for data…')

        lines.append('')

        # Camera
        lines.append(f'📷 CAMERA        → Frames received: {self.img_count}')

        lines.append('')

        # CMD_VEL
        if self.cmd_vel:
            lines += [
                '🕹️  CMD_VEL (current command)',
                f'   Linear X    → {self.cmd_vel.linear.x:.3f} m/s',
                f'   Angular Z   → {self.cmd_vel.angular.z:.3f} rad/s',
            ]
        else:
            lines.append('🕹️  CMD_VEL      → no command sent yet')

        lines.append('=' * 60)

        print('\033[H\033[J', end='')   # clear terminal
        print('\n'.join(lines))


def main(args=None):
    rclpy.init(args=args)
    node = SensorMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
