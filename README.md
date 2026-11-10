# roboparty_start

This repository contains runtime configurations and scripts for the RoboParty robots.

## Features

- **`start_robot.sh`**: The main entry point script intended for launching the system nodes (e.g. inference, joystick) within background `screen` sessions. Accepts `--robot` / `--policy` and auto-detects Humble / Jazzy.
- **`start_camera.sh`**: Launches RealSense and `depth_node` inside the `realsense_session` / `camera_session` screens.
- **`ros_environment.sh`**: ROS 2 environment auto-detection helper used by `start_robot.sh` / `start_camera.sh`.
- **`rt_fastdds_profile.xml`**: Real-time QoS profile configuration for Fast DDS.
- **`linux-router/`**: Tools and configurations for network infrastructure and routing on the robot.

## Installation

```bash
sudo apt install roboparty-start
```
Scripts and configs will be placed into the appropriate directories under the configured install prefix (default `/opt/roboparty/`).
