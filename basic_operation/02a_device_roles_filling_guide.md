# 02A. 如何填写 device_roles.json

本章专门解决两个最常见的问题：

- 怎么分清 `leader` 和 `follower`
- 怎么分清 `top_camera`、`wrist_camera` 和 `side_camera`

这份教程建议和 [02. 设备映射与角色绑定](/home/xuan/so101_education/basic_operation/02_arm_detection.md) 配合使用。  
`02_arm_detection.md` 负责讲概念，这一章负责告诉你“现在就该怎么做”。

现在 `detect_system` 已经支持输出“可直接执行命令”。  
这份教程的作用就是：先帮你把角色绑定正确，让这些直出命令真的能生成。

## 1. 先明白你要填什么

你要填写的是 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)：

```json
{
  "arms": {
    "leader": {
      "serial": "",
      "port": ""
    },
    "follower": {
      "serial": "",
      "port": ""
    }
  },
  "cameras": {
    "top_camera": {
      "serial": "",
      "by_path": ""
    },
    "wrist_camera": {
      "serial": "",
      "by_path": ""
    },
    "side_camera": {
      "serial": "",
      "by_path": ""
    }
  }
}
```

这里填的不是“这一次的临时端口”，而是“固定身份”：

- 机械臂填 `serial` 和 `port(by-id)`
- 相机填 `serial` 和 `by_path`

真正执行 LeRobot 命令时，你后面要填的是本次的：

- `/dev/ttyACM*`
- `/dev/video*`

## 2. 先运行检测工具

```bash
python3 tools/detect_system.py --write-roles-template
python3 tools/detect_system.py
```

运行后，请同时打开这 3 个位置：

1. [report.md](/home/xuan/so101_education/tools/devices/report.md)
2. `tools/devices/images/`
3. [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)

如果报告里写着 `leader: missing`、`follower: missing`、`top_camera: missing`，这是正常现象。  
它表示“设备已经识别到，但角色还没有绑定”。

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

打开 `report.md` 的“当前识别到的设备 -> 机械臂”部分，找到两条机械臂记录，例如：

- `5B41532613` | `tty=/dev/ttyACM0` | `by-id=/dev/serial/by-id/...`
- `5B42137834` | `tty=/dev/ttyACM1` | `by-id=/dev/serial/by-id/...`

如果你刚才确认第一只是真正的主臂，那么就把它对应那一行的：

- `serial`
- `by-id`

填进 `leader`。

另一只同理填进 `follower`。

## 4. 怎么判断 top_camera、wrist_camera、side_camera

### 截图法

打开 `tools/devices/images/` 下的图片，或直接看 `report.md` 的“相机截图预览”。

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

如果 `report.md` 里写着：

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
2. 再从报告里抄这两只机械臂的 `serial` 和 `by-id`
3. 打开截图，判断哪路是 `top_camera`，哪路是 `wrist_camera`
4. 再从报告里抄对应相机的 `serial` 和 `by_path`
5. 把这些内容填进 `device_roles.json`
6. 重新运行 `python3 tools/detect_system.py`
7. 确认报告里的角色从 `missing` 变成 `connected`

## 6. 完整填写示例

下面只是示例，你必须替换成自己机器上的真实值：

```json
{
  "arms": {
    "leader": {
      "serial": "5B41532613",
      "port": "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00"
    },
    "follower": {
      "serial": "5B42137834",
      "port": "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00"
    }
  },
  "cameras": {
    "top_camera": {
      "serial": "icSpring_icspring_camera_20240307110322",
      "by_path": "/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1:1.0-video-index0"
    },
    "wrist_camera": {
      "serial": "Sonix_Technology_Co.__Ltd._USB2.0_HD_UVC_WebCam",
      "by_path": "/dev/v4l/by-path/pci-0000:00:14.0-usb-0:7:1.0-video-index0"
    },
    "side_camera": {
      "serial": "",
      "by_path": ""
    }
  }
}
```

如果你们没有第三路相机，`side_camera` 可以先留空。

## 7. 填完以后怎么验证

再次运行：

```bash
python3 tools/detect_system.py
```

你应重点检查：

- `leader` 是否从 `missing` 变成 `connected`
- `follower` 是否从 `missing` 变成 `connected`
- `top_camera` 是否从 `missing` 变成 `connected`
- `wrist_camera` 是否从 `missing` 变成 `connected`

如果这里还没有变成 `connected`，说明：

- 你填错了 `serial`
- 你填错了 `by-id` 或 `by_path`
- 设备这次根本没有连上
- 你修改完 `device_roles.json` 后还没有重新运行检测

## 8. 重插设备后该怎么做

这是最重要的一条：

- `/dev/video10` 变成 `/dev/video12`，通常不需要改 `device_roles.json`
- `/dev/ttyACM0` 变成 `/dev/ttyACM1`，通常也不需要改 `device_roles.json`

因为 `device_roles.json` 里保存的是固定身份，不是临时端口。

你真正要做的是：

1. 重新运行 `python3 tools/detect_system.py`
2. 让工具根据固定身份恢复角色
3. 优先复制这次检测生成的“可直接执行命令”
4. 如果你还想做课堂讲解，再去看教学版参考命令

## 9. 常见错误

- 看到 `missing` 就直接去猜填 `device_roles.json`
- 把命令里的 `/dev/video*` 当成固定身份写进 `device_roles.json`
- 只看端口，不看截图，结果把 `top_camera` 和 `wrist_camera` 填反
- 修改完 `device_roles.json` 后没有重新运行检测
- 相机截图都没看，就直接开始改 `teleoperate` 或 `record` 命令

## 10. 完成后你应该能做到什么

完成这一章后，你应该能独立完成：

1. 判断主臂和从臂
2. 判断 `top_camera` 和 `wrist_camera`
3. 填写 `device_roles.json`
4. 重新运行检测确认角色恢复
5. 再去改 LeRobot 命令里的当前端口

---
**配套章节：**
- [02. 设备映射与角色绑定](02_arm_detection.md)
- [04. 带相机的遥操作](04_teleoperation.md)
- [05. 数据采集与回放](05_dataset_recording.md)
