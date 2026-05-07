# 07. 策略部署

本章的目标是根据 follower 端口、相机节点和 checkpoint 路径，优先使用检测工具给出的直接命令完成部署；如果要做教学解释，再对照教学版模板。

## 1. 先查看模板

```bash
python3 tools/detect_system.py --show-template rollout
```

如果报告里的 `rollout` 已经生成“可直接执行命令”，优先直接复制那一段。  
下面保留的是教学版参考命令。

## 2. 参考命令

```bash
lerobot-rollout \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "wrist": {"type": "opencv", "index_or_path": "<WRIST_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --policy.path=<CHECKPOINT_PATH>
```

## 3. 你需要修改的参数

- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<WRIST_CAMERA_DEV>`
- `<CHECKPOINT_PATH>`

## 4. 修改后应达到的效果

- 成功加载训练好的策略
- follower 在相机反馈下执行动作
- 部署时没有端口错误、相机错误或 checkpoint 路径错误

## 5. 命令改写训练

如果：

- `follower -> /dev/ttyACM0`
- `top_camera -> /dev/video10`
- `wrist_camera -> /dev/video4`
- checkpoint 在 `outputs/act_pick_place_run1/checkpoints/last`

那么你应把模板中的 4 个占位符都替换掉。

## 6. 自检问题

- 为什么部署前还要重新运行检测工具？
- 如果重新插拔相机后 `top_camera` 从 `/dev/video10` 变成 `/dev/video12`，哪一段必须重写？

## 可选扩展

如果本组还有 `side_camera`，可以在默认 `top + wrist` 部署成功后，把它加入 `robot.cameras` 作为第三路扩展视角。

## 7. 本章提交要求

- 提交你实际执行过的 rollout 命令
- 如果你使用的是教学版模板，再标出你替换的 4 个占位符
- 提交一次部署运行截图

---
**上一节：** [06. ACT 训练](06_act_training.md)
