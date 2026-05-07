# 00. 如何根据 device_simple 改写命令

本章的目标是学会“看懂 `device_simple.json` 和相机截图，再手动把当前端口写进命令”。

## 1. 先运行检测工具

```bash
python3 tools/detect_system.py
```

重点看两类信息：

- 机械臂当前端口：例如 `/dev/ttyACM0`
- 相机当前端口：例如 `/dev/video4`

## 2. 先看命令模板，再手动填端口

例如命令模板可能是：

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT>

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT>
```

## 3. 先识别设备，再写当前端口

建议永远按下面的顺序：

1. 打开 [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)
2. 找到机械臂的 `tty` 和 `by-id`
3. 打开 `tools/devices/images/`，确认哪一路是 `top_camera`、哪一路是 `wrist_camera`
4. 再回到 `device_simple.json`，查看这两路相机当前对应的 `dev`
5. 最后把这些当前端口写进 LeRobot 命令

也就是说：

- `by-id` / `by-path` 帮助你认设备
- LeRobot 命令里真正执行时用的是本次实际端口

## 4. 三种最常见的改写方式

### 例 1：替换主从臂串口

如果检测结果显示：

- `leader -> /dev/ttyACM1`
- `follower -> /dev/ttyACM0`

那么你应把：

- `<LEADER_PORT>` 改成 `/dev/ttyACM1`
- `<FOLLOWER_PORT>` 改成 `/dev/ttyACM0`

### 例 2：替换相机视频节点

如果检测结果显示：

- `top_camera -> /dev/video10`
- `wrist_camera -> /dev/video4`

那么你应把：

- `<TOP_CAMERA_DEV>` 改成 `/dev/video10`
- `<WRIST_CAMERA_DEV>` 改成 `/dev/video4`

### 例 3：替换数据集和输出目录

如果本次任务是积木抓取，训练输出希望保存到 `outputs/act_pick_block_run1`，那么你应把：

- `<DATASET_REPO_ID>` 改成 `${USER}/so101_pick_block`
- `<OUTPUT_DIR>` 改成 `outputs/act_pick_block_run1`

## 4. 判断哪些参数能改，哪些不要改

通常分两类：

- 固定参数：课程统一规定，不需要改
- 可变参数：跟端口、数据集名、输出目录、任务名有关，必须自己改

例如下面这条里：

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --output_dir=<OUTPUT_DIR>
```

其中：

- `--policy.type=act` 是固定参数
- `<DATASET_REPO_ID>` 和 `<OUTPUT_DIR>` 是可变参数

## 5. 一个完整例子：从 report 到命令

假设你在 `device_simple.json` 里看到：

- `top_camera` 的固定身份 `by_path` 是 `/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1:1.4-video-index0`
- `top_camera` 当前 `dev` 是 `/dev/video10`
- `wrist_camera` 当前 `dev` 是 `/dev/video4`

那么你应该这样做：

1. 先确认截图里哪一路是 `top_camera`
2. 再确认截图里哪一路是 `wrist_camera`
3. 最后在命令里把 `<TOP_CAMERA_DEV>` 改成 `/dev/video10`
4. 把 `<WRIST_CAMERA_DEV>` 改成 `/dev/video4`

## 6. 常用自检问题

- 这条命令里哪些占位符必须替换？
- 替换值来自检测工具的哪一行？
- 这个参数是硬件相关，还是实验命名相关？

## 7. 本章提交要求

- 提交一条你实际使用的命令
- 写出你替换了哪几个占位符
- 说明这些值来自 `device_simple.json` 的哪一项

---
**下一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
