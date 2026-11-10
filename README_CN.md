# roboparty_start

本仓库包含 RoboParty 机器人平台在运行期间所需的启动部署脚本与系统层面的配置文件。

## 包含组件

- **`start_robot.sh`**: 系统一键启动脚本，负责在后台利用 `screen` 守护运行所有的核心节点（如手柄控制进程、AI 推理进程等）。支持 `--robot` / `--policy` 参数，并自动探测 Humble / Jazzy。
- **`start_camera.sh`**: 相机一键启动脚本，在 `realsense_session` / `camera_session` 中启动 RealSense 与 `depth_node`。
- **`ros_environment.sh`**: `start_robot.sh` / `start_camera.sh` 使用的 ROS 2 环境自动探测脚本。
- **`rt_fastdds_profile.xml`**: 针对 Fast DDS 定制的专门应对实时要求（Real-time QoS）的配置文件。
- **`linux-router/`**: 包含配置机器人主板作为网络热点/路由等基建网络相关的脚本和工具。

## 安装

在机器人系统上执行：
```bash
sudo apt install roboparty-start
```
对应的脚本及网络配置将自动部署到安装前缀（默认 `/opt/roboparty/`）相关的目录系统中。

git clone https://github.com/Roboparty/roboparty_start

git submodule update --init --recursive

git submodule update --remote --recursive

source /opt/ros/humble/setup.bash

colcon build --symlink-install

