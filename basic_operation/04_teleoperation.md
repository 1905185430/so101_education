# 04. 带相机的遥操作

本章的目标是根据主从臂和相机的当前端口，手动改写遥操作命令。

## 1. 先查看本章模板

```bash
python3 tools/detect_system.py --show-template teleoperate
```

## 2. 参考命令

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "<SIDE_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --display_data=true
```

## 3. 你需要修改的参数

- `<FOLLOWER_PORT>`
- `<LEADER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`

这些值都来自检测工具输出，而不是自己猜。

## 4. 修改后应达到的效果

- 主臂移动时，从臂能同步跟随
- 能看到 top 和 side 相机画面
- 终端没有串口或相机设备找不到的报错

## 5. 命令改写训练

如果报告里显示：

- `follower -> /dev/ttyACM0`
- `leader -> /dev/ttyACM1`
- `top_camera -> /dev/video10`
- `side_camera -> /dev/video4`

那么你应该把模板中的 4 个占位符全部替换，而不是只改机械臂端口。

## 6. 常见问题

- 只改了机械臂端口，没改 camera 节点
- 把 `top_camera` 和 `side_camera` 写反
- 重插相机后沿用旧的 `/dev/video*`

## 7. 自检问题

- 如果 side camera 是 `/dev/video4`，应改 JSON 中的哪一项？
- 为什么本章的 camera 参数要写在同一条命令里？

## 8. 本章提交要求

- 提交你改写后的遥操作命令
- 标出你替换的 4 个占位符
- 提交一次遥操作运行截图

---
**上一节：** [03. 主从臂校准](03_calibration.md)
**下一节：** [05. 数据采集与回放](05_dataset_recording.md)
