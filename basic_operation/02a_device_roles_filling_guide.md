# 02A. 如何根据截图和 device_simple 判断设备角色

本章不是附加材料，而是在你还分不清主从臂和相机视角时必须先看的页面。它专门解决两个最常见的问题：

- 怎么分清 `leader` 和 `follower`
- 怎么分清 `top_camera`、`wrist_camera` 和 `side_camera`

这份教程建议和 [02. 设备识别与端口判断](/home/xuan/so101_education/basic_operation/02_arm_detection.md) 配合使用。  
`02_arm_detection.md` 负责讲概念，这一章负责告诉你“现在就该怎么做”。

## 1. 先明白你要看什么

现在你主要看两个地方：

- [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)
- `tools/devices/images/`

这里面最重要的是：

- 机械臂的 `tty` 和 `by-id`
- 相机的 `dev`、`by_path` 和 `image`

## 2. 先运行检测工具

```bash
python3 tools/detect_system.py
```

运行后，请同时打开这 3 个位置：

1. [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)
2. `tools/devices/images/`
3. 你准备改写的 LeRobot 命令模板

## 3. 怎么判断 leader 和 follower

### 动作法

先确保当前没有遥操作程序在运行。不要一边运行 `lerobot-teleoperate` 一边判断。

然后按下面步骤操作：

1. 找到两只机械臂
2. 轻轻手动带动其中一只
3. 观察它是否明显更适合作为“人手示教”的那只
4. 再看另一只是否是后续执行任务、接 `--robot.type=so101_follower` 的那只

课堂里固定采用下面这套定义：

- `leader`：人手直接带动、用于示教的主臂
- `follower`：后续执行动作、连接 `--robot.type=so101_follower` 的从臂

如果你们的设备安装方式有明显区别，比如：

- 一只更靠近学生
- 一只安装了任务端夹爪
- 一只用于演示，另一只用于执行

这些都可以作为辅助判断，但不是唯一标准。

### 判断完以后怎么抄

打开 `device_simple.json` 里的 `arms`，找到两条机械臂记录，例如：

- `5B41532613` | `tty=/dev/ttyACM0` | `by-id=/dev/serial/by-id/...`
- `5B42137834` | `tty=/dev/ttyACM1` | `by-id=/dev/serial/by-id/...`

如果你刚才确认第一只是真正的主臂，那么就在后续命令里把它当前的 `tty` 当作 `leader` 端口。  
另一只同理作为 `follower`。

## 4. 怎么判断 top_camera、wrist_camera、side_camera

### 截图法

打开 `tools/devices/images/` 下的图片。

课堂里固定采用下面这套定义：

- `top_camera`：俯视或高位全局视角，能看见操作台和机械臂整体
- `wrist_camera`：贴近末端执行器或手部附近，画面更近、更局部
- `side_camera`：侧面补充视角，只有第三路相机时才需要填

### 看到什么就填什么

如果某张截图里：

- 能看到桌面、机械臂整体和任务区域，那它通常是 `top_camera`
- 主要看到夹爪、手腕附近或近距离操作细节，那它通常是 `wrist_camera`
- 主要从侧面拍机械臂，那它通常是 `side_camera`

### 没有截图怎么办

如果 `device_simple.json` 里写着：

- `本次未生成截图`
- `OpenCV 无法打开相机`
- `本次未连接该相机`

那么先看同一行里的 `capture_detail` 或提示信息：

- 如果是“未连接”，先接回相机
- 如果是“OpenCV 无法打开”，先检查相机是否被别的程序占用
- 如果是“未生成截图”，先不要盲填角色，优先排除相机状态问题

## 5. 具体填写步骤

建议你严格按下面顺序来：

1. 先判断哪只是 `leader`，哪只是 `follower`
2. 再从 `device_simple.json` 里找到这两只机械臂当前的 `tty`
3. 打开截图，判断哪路是 `top_camera`，哪路是 `wrist_camera`
4. 再从 `device_simple.json` 里找到对应相机当前的 `dev`
5. 把这些当前端口写进命令

## 6. 重插设备后该怎么做

这是最重要的一条：

- `/dev/video10` 变成 `/dev/video12` 时，先重新运行检测
- `/dev/ttyACM0` 变成 `/dev/ttyACM1` 时，也先重新运行检测

你真正要做的是：

1. 重新运行 `python3 tools/detect_system.py`
2. 再看 `device_simple.json`
3. 先确认角色判断、截图和当前端口都对上
4. 再重写这次实际要执行的命令

## 7. 常见错误

- 只看 `/dev/video*` 名字，不看截图
- 只看 `/dev/ttyACM*` 名字，不结合主从臂实际位置判断
- 只看端口，不看截图，结果把 `top_camera` 和 `wrist_camera` 填反
- 相机截图都没看，就直接开始改 `teleoperate` 或 `record` 命令

## 8. 完成后你应该能做到什么

完成这一章后，你应该能独立完成：

1. 判断主臂和从臂
2. 判断 `top_camera` 和 `wrist_camera`
3. 重新运行检测获取当前端口
4. 再去改 LeRobot 命令里的当前端口

---
**配套章节：**
- [02. 设备映射与角色绑定](02_arm_detection.md)
- [04. 带相机的遥操作](04_teleoperation.md)
- [05. 数据采集与回放](05_dataset_recording.md)
