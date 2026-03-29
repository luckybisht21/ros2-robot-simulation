<div align="center">

# 🤖 ROS2 Robot Simulation
### Differential-Drive Robot with IMU · GPS · Camera Sensors

[![ROS2](https://img.shields.io/badge/ROS2-Humble-blue?logo=ros)](https://docs.ros.org/en/humble/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange)](https://gazebosim.org/)
[![Python](https://img.shields.io/badge/Python-3.10-green?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## 📺 Demo Video
[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)
> 🎬 Click to watch full demo on YouTube

---

## 📌 About This Project

This project is a complete robot simulation built from scratch using
ROS2 Humble and Gazebo Classic. The robot integrates multiple real-world
sensors and demonstrates live data acquisition, visualization, and CSV
logging.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🏎️ Differential Drive | 4-wheel robot with full kinematic control |
| 📐 IMU Sensor | 50 Hz — roll, pitch, yaw + acceleration |
| 🛰️ GPS Sensor | 1 Hz — latitude, longitude, altitude |
| 📷 Front Camera | 30 Hz — 640x480 RGB feed |
| 📊 Sensor Dashboard | Live terminal display of all sensor values |
| 💾 CSV Logger | Saves all sensor data to timestamped CSV files |
| 🌍 Custom World | Ramps, walls, obstacles for sensor testing |
| 🎥 Webcam Support | Laptop camera streamed via ROS2 |

---

## 🛠️ Tech Stack

- **ROS2 Humble** — Robot Operating System
- **Gazebo Classic** — Physics simulation
- **Python 3** — Sensor nodes and data logging
- **URDF / Xacro** — Robot modeling
- **SDF** — World modeling

---

## 📁 Project Structure

\`\`\`
ros2-robot-simulation/
├── urdf/
│   └── my_robot.urdf.xacro      # Robot model + sensor plugins
├── worlds/
│   └── robot_world.world         # Custom Gazebo world
├── launch/
│   └── gazebo.launch.py          # Full system launch
├── scripts/
│   ├── sensor_monitor.py         # Live terminal dashboard
│   └── sensor_logger.py          # CSV data logger
├── docs/images/                  # Screenshots
├── package.xml
├── CMakeLists.txt
└── README.md
\`\`\`

---

## ⚙️ Installation

### 1. Install Dependencies
\`\`\`bash
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-plugins \
  ros-humble-xacro \
  ros-humble-robot-state-publisher \
  ros-humble-teleop-twist-keyboard \
  ros-humble-v4l2-camera \
  ros-humble-rqt-image-view \
  xterm
\`\`\`

### 2. Clone and Build
\`\`\`bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/luckybisht21/ros2-robot-simulation.git
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot
source install/setup.bash
\`\`\`

---

## ▶️ Run the Project

\`\`\`bash
# Terminal 1 — Gazebo Simulation
ros2 launch my_robot gazebo.launch.py

# Terminal 2 — CSV Data Logger
ros2 run my_robot sensor_logger

# Terminal 3 — Laptop Webcam
ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:="/dev/video0"

# Terminal 4 — Camera Viewer
ros2 run rqt_image_view rqt_image_view

# Terminal 5 — Keyboard Control
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap /cmd_vel:=/robot/cmd_vel
\`\`\`

---

## 🕹️ Robot Controls

| Key | Action |
|-----|--------|
| i | Move Forward |
| , | Move Backward |
| j | Turn Left |
| l | Turn Right |
| k | Stop |
| q / z | Speed Up / Down |

---

## 📊 ROS2 Topics

| Topic | Message Type | Rate |
|-------|-------------|------|
| /robot/imu/data | sensor_msgs/Imu | 50 Hz |
| /robot/gps/fix | sensor_msgs/NavSatFix | 1 Hz |
| /robot/front_camera/image_raw | sensor_msgs/Image | 30 Hz |
| /robot/odom | nav_msgs/Odometry | 10 Hz |

---

## 🚀 Future Improvements

- [ ] Add LIDAR sensor
- [ ] Implement SLAM mapping
- [ ] Add obstacle avoidance
- [ ] Integrate RViz2 visualization
- [ ] Add autonomous navigation (Nav2)

---

## 👤 Author

**Lucky Bisht**
> Robotics and AI/ML Enthusiast | ROS2 Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/luckybisht21)

---

<div align="center">
⭐ Star this repo if you found it helpful!
</div>
