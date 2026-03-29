<div align="center">

# 🤖 ROS2 Robot Simulation

### Differential-Drive Robot with IMU · GPS · Camera Sensors

[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue?style=for-the-badge&logo=ros)](https://docs.ros.org/en/humble/)
[![Gazebo Classic](https://img.shields.io/badge/Gazebo-Classic-orange?style=for-the-badge)](https://classic.gazebosim.org/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

A complete robot simulation built **from scratch** using ROS2 Humble and Gazebo Classic —  
featuring real-world sensors, live dashboards, and CSV data logging.

<br/>

[![Demo Video](https://img.shields.io/badge/▶%20Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=77MXowE__Yk)

</div>

---

## 📌 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#️-installation)
- [Running the Project](#-running-the-project)
- [Robot Controls](#️-robot-controls)
- [ROS2 Topics](#-ros2-topics)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 📖 About

This project simulates a 4-wheeled differential-drive robot in a custom Gazebo environment.  
It integrates **IMU**, **GPS**, and **Camera** sensors that stream live data, which can be monitored via a terminal dashboard and saved to timestamped CSV files — mimicking real embedded robotics workflows.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🏎️ Differential Drive | 4-wheel robot with full kinematic control via `teleop_twist_keyboard` |
| 📐 IMU Sensor | 50 Hz — roll, pitch, yaw + linear acceleration |
| 🛰️ GPS Sensor | 1 Hz — latitude, longitude, altitude |
| 📷 Front Camera | 30 Hz — 640×480 RGB image feed |
| 📊 Sensor Dashboard | Live terminal display of all sensor values in real time |
| 💾 CSV Logger | Saves all sensor data to timestamped `.csv` files |
| 🌍 Custom World | Ramps, walls, and obstacles for realistic sensor testing |
| 🎥 Webcam Support | Laptop camera streamed live via ROS2 `v4l2_camera` |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| [ROS2 Humble](https://docs.ros.org/en/humble/) | Robot middleware and topic communication |
| [Gazebo Classic](https://classic.gazebosim.org/) | Physics-based 3D simulation |
| [Python 3](https://www.python.org/) | Sensor nodes, dashboard, and data logger |
| [URDF / Xacro](http://wiki.ros.org/xacro) | Robot model definition and sensor plugins |
| [SDF](http://sdformat.org/) | Custom Gazebo world description |

---

## 📁 Project Structure

```
ros2-robot-simulation/
├── urdf/
│   └── my_robot.urdf.xacro     # Robot model + sensor plugins
├── worlds/
│   └── robot_world.world       # Custom Gazebo environment
├── launch/
│   └── gazebo.launch.py        # Full system launch file
├── scripts/
│   ├── sensor_monitor.py       # Live terminal sensor dashboard
│   └── sensor_logger.py        # CSV data logger
├── CMakeLists.txt
├── package.xml
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Ubuntu 22.04
- ROS2 Humble installed — [Installation Guide](https://docs.ros.org/en/humble/Installation.html)
- Gazebo Classic (`gazebo11`)

### 1. Install ROS2 Dependencies

```bash
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-plugins \
  ros-humble-xacro \
  ros-humble-robot-state-publisher \
  ros-humble-teleop-twist-keyboard \
  ros-humble-v4l2-camera \
  ros-humble-rqt-image-view \
  xterm
```

### 2. Clone and Build

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone repository
git clone https://github.com/luckybisht21/ros2-robot-simulation.git

# Build the package
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot
source install/setup.bash
```

---

## ▶️ Running the Project

Open **5 separate terminals** and run one command in each:

```bash
# Terminal 1 — Launch Gazebo Simulation
ros2 launch my_robot gazebo.launch.py
```

```bash
# Terminal 2 — CSV Data Logger
ros2 run my_robot sensor_logger
```

```bash
# Terminal 3 — Stream Laptop Webcam
ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:="/dev/video0"
```

```bash
# Terminal 4 — View Camera Feed
ros2 run rqt_image_view rqt_image_view
```

```bash
# Terminal 5 — Keyboard Control
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap /cmd_vel:=/robot/cmd_vel
```

> **Tip:** Source `install/setup.bash` in every new terminal before running ROS2 commands.

---

## 🕹️ Robot Controls

| Key | Action |
|---|---|
| `i` | Move Forward |
| `,` | Move Backward |
| `j` | Turn Left |
| `l` | Turn Right |
| `k` | Stop |
| `q` / `z` | Increase / Decrease Speed |

---

## 📡 ROS2 Topics

| Topic | Message Type | Rate |
|---|---|---|
| `/robot/imu/data` | `sensor_msgs/Imu` | 50 Hz |
| `/robot/gps/fix` | `sensor_msgs/NavSatFix` | 1 Hz |
| `/robot/front_camera/image_raw` | `sensor_msgs/Image` | 30 Hz |
| `/robot/odom` | `nav_msgs/Odometry` | 10 Hz |

---

## 🚀 Future Improvements

- [ ] Add LIDAR sensor (Velodyne / RPLidar)
- [ ] Implement SLAM mapping (SLAM Toolbox)
- [ ] Add obstacle avoidance behaviour
- [ ] Integrate RViz2 visualization
- [ ] Add autonomous navigation (Nav2 stack)
- [ ] Sensor fusion with Extended Kalman Filter (EKF)

---

## 👤 Author

<div align="center">

**Lucky Bisht**  
Robotics & AI/ML Enthusiast · ROS2 Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/lucky-bisht-b176b2291/)
[![YouTube](https://img.shields.io/badge/YouTube-Demo-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=77MXowE__Yk)
[![GitHub](https://img.shields.io/badge/GitHub-luckybisht21-black?style=for-the-badge&logo=github)](https://github.com/luckybisht21)

</div>

---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

</div>
