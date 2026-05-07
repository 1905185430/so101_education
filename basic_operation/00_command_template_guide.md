# 00. 如何从检测结果改写命令

本章的目标是先学会“看懂检测结果，再改写命令”。

## 1. 先运行检测工具

```bash
python3 tools/detect_system.py
```

重点看两类信息：

- `角色身份`：`leader`、`follower`、`top_camera`、`side_camera`
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

## 3. 三种最常见的改写方式

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
- `side_camera -> /dev/video4`

那么你应把：

- `<TOP_CAMERA_DEV>` 改成 `/dev/video10`
- `<SIDE_CAMERA_DEV>` 改成 `/dev/video4`

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

## 5. 常用自检问题

- 这条命令里哪些占位符必须替换？
- 替换值来自检测工具的哪一行？
- 这个参数是硬件相关，还是实验命名相关？

## 6. 本章提交要求

- 提交一条你自己改写过的校准命令
- 写出你替换了哪几个占位符
- 说明每个替换值来自哪条检测结果

---
**下一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
