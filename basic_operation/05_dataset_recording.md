# 05. 数据采集与回放

本章的目标是根据当前设备映射，手动改写数据采集命令和回放命令。

## 1. 先查看模板

```bash
python3 tools/detect_system.py --show-template record
python3 tools/detect_system.py --show-template replay
```

## 2. 参考命令：采集

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

## 3. 你需要修改的参数

- `<FOLLOWER_PORT>`
- `<LEADER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<WRIST_CAMERA_DEV>`
- `<DATASET_REPO_ID>`
- `<TASK_DESCRIPTION>`

## 4. 修改后应达到的效果

- 完成多条示教轨迹采集
- 生成本地数据集目录
- 后续可以用于 replay 和 ACT 训练

## 5. 参考命令：回放

```bash
lerobot-replay \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --episode=<EPISODE_INDEX>
```

## 6. 回放时需要修改的参数

- `<FOLLOWER_PORT>`
- `<DATASET_REPO_ID>`
- `<EPISODE_INDEX>`

## 7. 命令改写训练

- 如果要把数据集名改成 `${USER}/so101_stack_blocks`，你应改哪个占位符？
- 如果要回放第 2 条轨迹，`<EPISODE_INDEX>` 应该改成几？

## 8. 自检问题

- 为什么 replay 不需要填写 leader 端口？
- 为什么 record 阶段既要写机械臂端口，也要写 camera 节点？

## 可选扩展

如果本组额外有 `side_camera`，可以在默认 `top + wrist` 成功采集后，再把 `side` 加入采集命令作为第三路视角。

## 9. 本章提交要求

- 提交你改写后的采集命令
- 提交你改写后的回放命令
- 提交一次回放成功的截图

---
**上一节：** [04. 带相机的遥操作](04_teleoperation.md)
**下一节：** [06. ACT 训练](06_act_training.md)
