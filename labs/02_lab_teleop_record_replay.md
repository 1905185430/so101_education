# 第二次课：遥操作、数据采集与回放

本次课的目标是让学生在已经完成角色绑定和校准的基础上，改写相机与采集相关命令，完成遥操作、录制和回放验证。

## 课前准备

- 第一次课已完成 `leader` 和 `follower` 绑定
- 主从臂已完成校准
- `top_camera` 和 `side_camera` 已接入电脑

## 课内目标

- 会看懂检测报告中的 `top_camera` 和 `side_camera`
- 会改写 `<TOP_CAMERA_DEV>` 和 `<SIDE_CAMERA_DEV>`
- 能完成遥操作
- 能录制至少一组有效 episode
- 能完成 replay 验证

## 课内步骤

### 1. 检查当前角色与相机节点

```bash
python3 tools/detect_system.py
python3 tools/detect_system.py --show-template teleoperate
python3 tools/detect_system.py --show-template record
python3 tools/detect_system.py --show-template replay
```

### 2. 先完成遥操作

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "<SIDE_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true
```

### 3. 再完成数据采集

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

### 4. 最后用 replay 验证

```bash
lerobot-replay \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --episode=<EPISODE_INDEX>
```

## 你需要修改的参数

- `<FOLLOWER_PORT>`
- `<LEADER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`
- `<DATASET_REPO_ID>`
- `<TASK_DESCRIPTION>`
- `<EPISODE_INDEX>`

## 修改后应达到的效果

- 先看到稳定的主从遥操作画面
- 再完成至少 1 组可用数据录制
- 最后 replay 时从臂能复现已录制轨迹

## 课后任务

- 整理一份本组统一的数据集命名规范
- 补充录制 1 到 2 组更稳定的 episode
- 记录本组相机最稳定的 `video` 节点映射

## 提交要求

- 改写后的遥操作命令
- 改写后的采集命令
- 改写后的回放命令
- 至少 1 个成功 replay 的结果截图

## 评分点

- 能正确改写相机相关占位符
- 能完成遥操作且画面正常
- 能录制有效数据集
- 能用 replay 证明数据可用

## 细化参考

- [04. 带相机的遥操作](/home/xuan/so101_education/basic_operation/04_teleoperation.md)
- [05. 数据采集与回放](/home/xuan/so101_education/basic_operation/05_dataset_recording.md)
