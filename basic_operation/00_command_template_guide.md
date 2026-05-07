# 00. 如何从检测结果改写命令

本章的目标是先学会“看懂检测结果，再改写命令”。

## 1. 先运行检测工具

```bash
python3 tools/detect_system.py
```

重点看两类信息：

- `角色身份`：`leader`、`follower`、`top_camera`、`wrist_camera`
- `当前端口`：例如 `/dev/ttyACM0`、`/dev/video4`

## 2. 先看模板，再替换占位符

例如检测工具可能给出这样的参考命令：

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT>

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT>
```

学生不能直接执行这段命令，因为其中还有占位符。

## 3. 先绑定固定身份，再改当前端口

这一步最容易混淆。建议永远按下面的顺序：

1. 打开 [report.md](/home/xuan/so101_education/tools/devices/report.md)
2. 找到 `top_camera` 的固定身份 `by_path`
3. 把这个 `by_path` 填进 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)
4. 重新运行一次 `python3 tools/detect_system.py`
5. 再回到 `report.md`，查看 `top_camera` 当前对应的 `dev`
6. 最后把 `<TOP_CAMERA_DEV>` 填进 LeRobot 参考命令

也就是说：

- `device_roles.json` 填的是固定身份
- LeRobot 命令里填的是本次实际端口

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

假设你在 `report.md` 里看到：

- `top_camera` 的固定身份 `by_path` 是 `/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1:1.4-video-index0`
- `top_camera` 当前 `dev` 是 `/dev/video10`
- `wrist_camera` 当前 `dev` 是 `/dev/video4`

那么你应该这样做：

1. 先把 `top_camera.by_path` 填进 `device_roles.json`
2. 再运行一次 `python3 tools/detect_system.py`
3. 确认 `top_camera` 在报告中已经是 `connected`
4. 最后在命令里把 `<TOP_CAMERA_DEV>` 改成 `/dev/video10`
5. 把 `<WRIST_CAMERA_DEV>` 改成 `/dev/video4`

## 6. 常用自检问题

- 这条命令里哪些占位符必须替换？
- 替换值来自检测工具的哪一行？
- 这个参数是硬件相关，还是实验命名相关？

## 7. 本章提交要求

- 提交一条你自己改写过的校准命令
- 写出你替换了哪几个占位符
- 说明每个替换值来自哪条检测结果

---
**下一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
