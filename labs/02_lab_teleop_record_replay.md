# 第二次课：遥操作、数据采集与回放

本次课的目标是让学生在已经完成角色绑定和校准的基础上，改写相机与采集相关命令，完成遥操作、录制和回放验证。

## 先修导学

- [03. 具身智能数据采集导学](/home/xuan/so101_education/primer/03_embodied_data_intro.md)

建议先理解 `observation`、`action`、`episode`、`replay` 的含义，再进入本次课的数据采集与回放实验。

## 课前准备

- 第一次课已完成 `leader` 和 `follower` 绑定
- 主从臂已完成校准
- `top_camera` 和 `wrist_camera` 已接入电脑

## 课内目标

- 会看懂检测报告中的 `top_camera` 和 `wrist_camera`
- 会改写 `<TOP_CAMERA_DEV>` 和 `<WRIST_CAMERA_DEV>`
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

在真正改命令前，请先确认这 4 个值：

- `leader` 当前 `tty`
- `follower` 当前 `tty`
- `top_camera` 当前 `dev`
- `wrist_camera` 当前 `dev`

建议操作顺序：

1. 打开 [report.md](/home/xuan/so101_education/tools/devices/report.md)
2. 在“相机固定身份参考”里确认 `top_camera` 和 `wrist_camera` 的 `by_path`
3. 打开 `tools/devices/images/` 下的截图，确认哪一路俯视画面是 `top`，哪一路近距离手眼画面是 `wrist`
4. 如果截图方向和角色名对不上，先改 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)，再重新运行检测
5. 只有当 `report.md` 里的角色、截图和当前 `dev` 都对上之后，再去改命令

如果这一步里你看到：

- `top_camera: missing`
- `wrist_camera: missing`

先不要直接改相机命令。说明设备还没绑定到角色，请先看：

- [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)

### 2. 先完成遥操作

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "wrist": {"type": "opencv", "index_or_path": "<WRIST_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true
```

### 3. 再完成数据采集

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "wrist": {"type": "opencv", "index_or_path": "<WRIST_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
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
- `<WRIST_CAMERA_DEV>`
- `<DATASET_REPO_ID>`
- `<TASK_DESCRIPTION>`
- `<EPISODE_INDEX>`

## 修改后应达到的效果

- 先看到稳定的主从遥操作画面
- 再完成至少 1 组可用数据录制
- 最后 replay 时从臂能复现已录制轨迹
- 如果 `top` 和 `wrist` 画面方向不对，说明角色可能填反了，应先修正 `device_roles.json`

## 扩展任务：如果本组额外接入 side camera

如果你的教学现场额外提供了第三路 `side_camera`，可以在默认 `top + wrist` 成功后，再把 `side` 加入 `robot.cameras` 配置中，作为进阶多视角采集练习。这个扩展不会替代主流程，只是在主流程之上增加第三路视角。

## 课后任务

- 整理一份本组统一的数据集命名规范
- 补充录制 1 到 2 组更稳定的 episode
- 记录本组相机最稳定的 `video` 节点映射
- 如果本组有第三路相机，再额外记录 `side_camera` 的稳定映射

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

- [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)
- [04. 带相机的遥操作](/home/xuan/so101_education/basic_operation/04_teleoperation.md)
- [05. 数据采集与回放](/home/xuan/so101_education/basic_operation/05_dataset_recording.md)
