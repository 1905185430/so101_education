# 04. 带相机的遥操作

本章的目标是根据主从臂和相机的当前端口完成遥操作，并在执行前看懂 `top/wrist` 视角和当前端口的对应关系。

## 1. 先查看本章模板

```bash
python3 tools/detect_system.py --show-template teleoperate
```

在改命令之前，先重新运行一次：

```bash
python3 tools/detect_system.py
```

然后确认这 4 个值：

- `leader` 当前 `tty`
- `follower` 当前 `tty`
- `top_camera` 当前 `dev`
- `wrist_camera` 当前 `dev`

同时打开 `tools/devices/images/` 下的截图，确认俯视画面对应 `top_camera`，手眼近景对应 `wrist_camera`。如果截图方向不对，先修正 `device_roles.json`，不要直接硬改命令。

执行前先确认：

- `top_camera` 真的是俯视全局画面
- `wrist_camera` 真的是近手视角
- 当前 `tty` / `dev` 是这次重新检测到的结果，不是上一次记住的值

确认完以后，再执行报告里的“可直接执行命令”。下面保留教学版参考命令。

## 2. 参考命令

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "wrist": {"type": "opencv", "index_or_path": "<WRIST_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true
```

## 3. 你需要修改的参数

- `<FOLLOWER_PORT>`
- `<LEADER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<WRIST_CAMERA_DEV>`

这些值都来自检测工具输出，而不是自己猜。

## 4. 修改后应达到的效果

- 主臂移动时，从臂能同步跟随
- 能看到 top 和 wrist 相机画面
- 终端没有串口或相机设备找不到的报错

## 5. 命令改写训练

如果报告里显示：

- `follower -> /dev/ttyACM0`
- `leader -> /dev/ttyACM1`
- `top_camera -> /dev/video10`
- `wrist_camera -> /dev/video4`

那么你应该把模板中的 4 个占位符全部替换，而不是只改机械臂端口。

如果你发现截图中 `top_camera` 实际上是手腕视角，而 `wrist_camera` 实际上是俯视视角，说明角色填反了。这个时候应先回到 `device_roles.json` 调整绑定，再重新运行检测，而不是直接在命令里把两个名字硬记反。

## 6. 常见问题

- 只改了机械臂端口，没改 camera 节点
- 把 `top_camera` 和 `wrist_camera` 写反
- 重插相机后沿用旧的 `/dev/video*`

## 7. 自检问题

- 如果 wrist camera 是 `/dev/video4`，应改 JSON 中的哪一项？
- 为什么本章的 camera 参数要写在同一条命令里？

## 可选扩展

如果现场额外接入 `side_camera`，可以在默认 `top + wrist` 跑通后，把它作为第三路视角加入 `robot.cameras`，用于进阶多视角实验。

## 8. 本章提交要求

- 提交你实际执行过的遥操作命令
- 如果你使用的是教学版模板，再标出你替换的 4 个占位符
- 提交一次遥操作运行截图

---
**上一节：** [03. 主从臂校准](03_calibration.md)
**下一节：** [05. 数据采集与回放](05_dataset_recording.md)
