# SO-101 实验设备检测报告

- 生成时间: `2026-05-07T17:02:24.341645`
- 检测阶段: `all`

## 当前角色身份与端口

- `leader`: missing | 当前tty: `未识别`
- `follower`: missing | 当前tty: `未识别`
- `top_camera`: missing | 当前dev: `未识别`
- `side_camera`: missing | 当前dev: `未识别`
- `wrist_camera`: missing | 当前dev: `未识别`

## 三次课使用提示

- 第一次课重点关注 `leader`、`follower` 和当前 `tty`，用于角色绑定与校准命令改写。
- 第二次课在第一次课基础上新增关注 `top_camera`、`side_camera` 和当前 `video` 节点，用于遥操作、录制与回放。
- 第三次课重点沿用第二次课的数据集命名与相机映射，并结合训练输出目录与 checkpoint 路径完成训练启动和 rollout。

## 当前识别到的设备

### 机械臂

- `5B41532613` | status=`connected` | tty=`/dev/ttyACM0` | by-id=`/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00`
- `5B42137834` | status=`connected` | tty=`/dev/ttyACM1` | by-id=`/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00`

### 相机

- `Sonix_Technology_Co.__Ltd._USB2.0_HD_UVC_WebCam` | status=`disconnected` | dev=`/dev/video0` | by-path=`/dev/v4l/by-path/pci-0000:00:14.0-usb-0:7:1.0-video-index0`
- `Orbbec_R__Orbbec_Gemini_335_CP15641000AW` | status=`disconnected` | dev=`/dev/video10` | by-path=`/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.4:1.4-video-index0`
- `Orbbec_R__Orbbec_Gemini_335_CP1L44P0007K` | status=`disconnected` | dev=`/dev/video14` | by-path=`/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1:1.4-video-index0`
- `icSpring_icspring_camera_20240307110322` | status=`disconnected` | dev=`/dev/video2` | by-path=`/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1:1.0-video-index0`

## 检查结果

### env

- `WARN` python: 当前 Python 版本: 3.13.13
  提示: LeRobot 常见教学环境建议使用 Python 3.10-3.12。
- `PASS` ffmpeg: ffmpeg: 已找到
  提示: 如果后续实验会用到 ffmpeg，请先在 LeRobot 环境中完成安装。
- `WARN` v4l2-ctl: v4l2-ctl: 未找到
  提示: 如果后续实验会用到 v4l2-ctl，请先在 LeRobot 环境中完成安装。
- `WARN` nvidia-smi: nvidia-smi: 未找到
  提示: 如果后续实验会用到 nvidia-smi，请先在 LeRobot 环境中完成安装。
- `WARN` lerobot-find-port: lerobot-find-port: 未找到
  提示: 如果后续实验会用到 lerobot-find-port，请先在 LeRobot 环境中完成安装。
- `WARN` lerobot-calibrate: lerobot-calibrate: 未找到
  提示: 如果后续实验会用到 lerobot-calibrate，请先在 LeRobot 环境中完成安装。
- `WARN` lerobot-record: lerobot-record: 未找到
  提示: 如果后续实验会用到 lerobot-record，请先在 LeRobot 环境中完成安装。
- `WARN` lerobot-train: lerobot-train: 未找到
  提示: 如果后续实验会用到 lerobot-train，请先在 LeRobot 环境中完成安装。
- `WARN` lerobot-rollout: lerobot-rollout: 未找到
  提示: 如果后续实验会用到 lerobot-rollout，请先在 LeRobot 环境中完成安装。
- `WARN` opencv-python: cv2 未安装
  提示: 如需保存相机截图，请在教学环境中安装 opencv-python。
- `WARN` dialout: 当前用户组: xuan adm cdrom sudo dip plugdev users lpadmin lxd
  提示: 若串口权限不足，请执行 sudo usermod -a -G dialout $USER 后重新登录。

### robot

- `PASS` arms_detected: 已连接机械臂数量: 2
  提示: 请检查主从臂供电、USB 连接和串口权限。

### camera

- `WARN` cameras_detected: 已连接相机数量: 0
  提示: 如果后续实验需要相机，请检查 USB 连接和供电。
- `WARN` camera_color_stream: 支持彩色流的已连接相机数量: 0
  提示: 如果采集或遥操作需要画面显示，请优先选择支持彩色流的相机。

### train

- `WARN` gpu: 未检测到 nvidia-smi。
  提示: 如果课程要求本地 ACT 训练，请确认机器已安装 NVIDIA 驱动和 CUDA 环境。
- `PASS` disk: 当前工作目录剩余空间约 738.3 GB。
  提示: 建议为数据采集和训练预留至少 20 GB 可用空间。

## 参考命令模板

### calibrate - 校准参考命令

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT>

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT>
```

本机应参考的占位符取值：
- `<LEADER_PORT>` -> `<请根据检测结果填写>`
- `<FOLLOWER_PORT>` -> `<请根据检测结果填写>`

你需要修改的参数：
- `<LEADER_PORT>`
- `<FOLLOWER_PORT>`

修改后应达到的效果：主臂和从臂分别完成零位校准，终端出现校准完成或保存结果提示。

自检问题：
- 如果 leader 当前对应 /dev/ttyACM1，你应该改哪一段？
- 为什么 leader 和 follower 不能共用同一个端口？

### teleoperate - 遥操作参考命令

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "<SIDE_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true
```

本机应参考的占位符取值：
- `<LEADER_PORT>` -> `<请根据检测结果填写>`
- `<FOLLOWER_PORT>` -> `<请根据检测结果填写>`
- `<TOP_CAMERA_DEV>` -> `<请根据检测结果填写>`
- `<SIDE_CAMERA_DEV>` -> `<请根据检测结果填写>`

你需要修改的参数：
- `<LEADER_PORT>`
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`

修改后应达到的效果：移动主臂时，从臂同步运动，终端或弹窗可以看到 top 和 side 画面。

自检问题：
- 如果 side camera 实际是 /dev/video4，你应该改 JSON 里的哪一项？
- 为什么本章要同时填写 leader、follower 和 camera 参数？

### record - 数据采集参考命令

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "<SIDE_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --dataset.single_task='<TASK_DESCRIPTION>' \
  --dataset.num_episodes=5 \
  --dataset.episode_time_s=20 \
  --dataset.push_to_hub=false
```

本机应参考的占位符取值：
- `<LEADER_PORT>` -> `<请根据检测结果填写>`
- `<FOLLOWER_PORT>` -> `<请根据检测结果填写>`
- `<TOP_CAMERA_DEV>` -> `<请根据检测结果填写>`
- `<SIDE_CAMERA_DEV>` -> `<请根据检测结果填写>`
- `<DATASET_REPO_ID>` -> `<请自行命名，例如 ${USER}/so101_pick_place>`
- `<TASK_DESCRIPTION>` -> `<请填写任务描述，例如 pick cube and place into tray>`

你需要修改的参数：
- `<LEADER_PORT>`
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`
- `<DATASET_REPO_ID>`
- `<TASK_DESCRIPTION>`

修改后应达到的效果：完成多条 episode 采集，本地生成数据集目录，可用于 replay 和 ACT 训练。

自检问题：
- 如果你的数据集名想换成 so101_stack_blocks，应修改哪个占位符？
- 为什么录制命令里也必须保留 camera 参数？

### replay - 回放参考命令

```bash
lerobot-replay \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --episode=<EPISODE_INDEX>
```

本机应参考的占位符取值：
- `<FOLLOWER_PORT>` -> `<请根据检测结果填写>`
- `<DATASET_REPO_ID>` -> `<请自行命名，例如 ${USER}/so101_pick_place>`
- `<EPISODE_INDEX>` -> `0`

你需要修改的参数：
- `<FOLLOWER_PORT>`
- `<DATASET_REPO_ID>`
- `<EPISODE_INDEX>`

修改后应达到的效果：从臂按已采集轨迹复现动作，学生能验证录制数据是否可用。

自检问题：
- 如果要回放第 2 条 episode，应修改哪个占位符？
- 为什么 replay 时不需要填写 leader 端口？

### rollout - 策略部署参考命令

```bash
lerobot-rollout \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "<SIDE_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --policy.path=<CHECKPOINT_PATH>
```

本机应参考的占位符取值：
- `<FOLLOWER_PORT>` -> `<请根据检测结果填写>`
- `<TOP_CAMERA_DEV>` -> `<请根据检测结果填写>`
- `<SIDE_CAMERA_DEV>` -> `<请根据检测结果填写>`
- `<CHECKPOINT_PATH>` -> `<请填写训练输出中的 checkpoint 路径>`

你需要修改的参数：
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`
- `<CHECKPOINT_PATH>`

修改后应达到的效果：已训练策略加载成功，follower 在相机反馈下执行任务。

自检问题：
- 为什么 rollout 阶段还要再次检查 camera 端口？
- 如果 checkpoint 目录换了，你应替换哪个占位符？
