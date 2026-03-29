#!/usr/bin/env python3
"""
sensor_logger.py
Saves IMU, GPS, Odometry and CMD_VEL data to CSV files with timestamps.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

import csv
import os
import math
from datetime import datetime


def quat_to_euler(q):
    sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (q.w * q.y - q.z * q.x)
    sinp = max(-1.0, min(1.0, sinp))
    pitch = math.asin(sinp)

    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


class SensorLogger(Node):
    def __init__(self):
        super().__init__('sensor_logger')

        # ── Output folder ────────────────────────────────────────────────────
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_dir = os.path.expanduser(f'~/sensor_logs/{timestamp}')
        os.makedirs(self.log_dir, exist_ok=True)

        # ── CSV files ────────────────────────────────────────────────────────
        self.imu_file   = self._open_csv('imu_data.csv',  [
            'time', 'roll_deg', 'pitch_deg', 'yaw_deg',
            'accel_x', 'accel_y', 'accel_z',
            'gyro_x',  'gyro_y',  'gyro_z',
            'quat_x',  'quat_y',  'quat_z', 'quat_w'
        ])

        self.gps_file   = self._open_csv('gps_data.csv',  [
            'time', 'latitude', 'longitude', 'altitude', 'status'
        ])

        self.odom_file  = self._open_csv('odom_data.csv', [
            'time', 'pos_x', 'pos_y', 'pos_z',
            'yaw_deg', 'vel_linear_x', 'vel_angular_z'
        ])

        self.cmd_file   = self._open_csv('cmd_vel_data.csv', [
            'time', 'linear_x', 'linear_y', 'linear_z',
            'angular_x', 'angular_y', 'angular_z'
        ])

        # ── Subscribers ──────────────────────────────────────────────────────
        self.create_subscription(Imu,       '/robot/imu/data',  self.imu_cb,  10)
        self.create_subscription(NavSatFix, '/robot/gps/fix',   self.gps_cb,  10)
        self.create_subscription(Odometry,  '/robot/odom',      self.odom_cb, 10)
        self.create_subscription(Twist,     '/robot/cmd_vel',   self.cmd_cb,  10)

        # Counters
        self.counts = {'imu': 0, 'gps': 0, 'odom': 0, 'cmd': 0}

        # Print status every 5 seconds
        self.create_timer(5.0, self.print_status)

        self.get_logger().info(f'📁 Logging to: {self.log_dir}')
        self.get_logger().info('✅ Sensor Logger started — saving IMU, GPS, Odometry, CMD_VEL')

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _open_csv(self, filename, headers):
        path = os.path.join(self.log_dir, filename)
        f = open(path, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(headers)
        self.get_logger().info(f'  Created: {path}')
        return {'file': f, 'writer': writer, 'path': path}

    def _now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # ── Callbacks ────────────────────────────────────────────────────────────
    def imu_cb(self, msg):
        roll, pitch, yaw = quat_to_euler(msg.orientation)
        self.imu_file['writer'].writerow([
            self._now(),
            round(roll,  4), round(pitch, 4), round(yaw,  4),
            round(msg.linear_acceleration.x, 6),
            round(msg.linear_acceleration.y, 6),
            round(msg.linear_acceleration.z, 6),
            round(msg.angular_velocity.x, 6),
            round(msg.angular_velocity.y, 6),
            round(msg.angular_velocity.z, 6),
            round(msg.orientation.x, 6),
            round(msg.orientation.y, 6),
            round(msg.orientation.z, 6),
            round(msg.orientation.w, 6),
        ])
        self.imu_file['file'].flush()
        self.counts['imu'] += 1

    def gps_cb(self, msg):
        status_str = {0:'FIX', 1:'SBAS_FIX', 2:'GBAS_FIX', -1:'NO_FIX'}.get(
            msg.status.status, 'UNKNOWN')
        self.gps_file['writer'].writerow([
            self._now(),
            round(msg.latitude,  8),
            round(msg.longitude, 8),
            round(msg.altitude,  3),
            status_str
        ])
        self.gps_file['file'].flush()
        self.counts['gps'] += 1

    def odom_cb(self, msg):
        _, _, yaw = quat_to_euler(msg.pose.pose.orientation)
        self.odom_file['writer'].writerow([
            self._now(),
            round(msg.pose.pose.position.x, 4),
            round(msg.pose.pose.position.y, 4),
            round(msg.pose.pose.position.z, 4),
            round(yaw, 4),
            round(msg.twist.twist.linear.x,  4),
            round(msg.twist.twist.angular.z, 4),
        ])
        self.odom_file['file'].flush()
        self.counts['odom'] += 1

    def cmd_cb(self, msg):
        self.cmd_file['writer'].writerow([
            self._now(),
            round(msg.linear.x,  4),
            round(msg.linear.y,  4),
            round(msg.linear.z,  4),
            round(msg.angular.x, 4),
            round(msg.angular.y, 4),
            round(msg.angular.z, 4),
        ])
        self.cmd_file['file'].flush()
        self.counts['cmd'] += 1

    def print_status(self):
        print('\n📊 SENSOR LOGGER STATUS')
        print(f'   📁 Saving to: {self.log_dir}')
        print(f'   📐 IMU rows logged    : {self.counts["imu"]}')
        print(f'   🛰️  GPS rows logged    : {self.counts["gps"]}')
        print(f'   📍 Odometry rows logged: {self.counts["odom"]}')
        print(f'   🕹️  CMD_VEL rows logged : {self.counts["cmd"]}')

    def destroy_node(self):
        # Close all files cleanly on shutdown
        for name, d in [('IMU', self.imu_file), ('GPS', self.gps_file),
                        ('Odom', self.odom_file), ('CMD', self.cmd_file)]:
            d['file'].close()
            self.get_logger().info(f'💾 Saved {name} → {d["path"]}')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SensorLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\n🛑 Logger stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()