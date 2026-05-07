# 01. 环境搭建与 CLI 验证

本章的目标是搭好 LeRobot 环境，并确认你后续会用到的命令已经安装成功。

## 1. 硬件准备

- 为主臂、从臂接通电源
- 用 USB 将机械臂接入电脑
- 如果后续要做遥操作和采集，相机也一起接入

## 2. 系统依赖

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake ffmpeg v4l-utils git
```

## 3. 参考命令

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot

mkdir -p <WORKSPACE_DIR>
cd <WORKSPACE_DIR>

git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install -e ".[feetech]"
```

## 4. 你需要修改的参数

- `<WORKSPACE_DIR>`：改成你自己的工作目录

## 5. 修改后应达到的效果

- `lerobot-find-port --help` 可以正常显示帮助
- `lerobot-calibrate --help` 可以正常显示帮助
- `lerobot-record --help` 可以正常显示帮助
- `lerobot-train --help` 可以正常显示帮助

## 6. 建议验证命令

```bash
lerobot-find-port --help
lerobot-calibrate --help
lerobot-record --help
lerobot-train --help
lerobot-rollout --help
python3 tools/detect_system.py --stage env
```

## 7. 自检问题

- 为什么本章只需要改 `<WORKSPACE_DIR>`，不需要改机械臂端口？
- 如果 `lerobot-record --help` 找不到，说明是硬件问题还是环境问题？

## 8. 本章提交要求

- 提交环境安装后的帮助命令截图
- 提交一次 `python3 tools/detect_system.py --stage env` 的输出

---
**上一节：** [00. 如何从检测结果改写命令](00_command_template_guide.md)
**下一节：** [02. 设备映射与角色绑定](02_arm_detection.md)
