# 02. 设备映射与角色绑定

本章的目标是区分“设备身份”和“当前端口号”，并把你的设备绑定到统一的教学角色名上。

## 1. 为什么要做角色绑定

断电重连之后，系统里的 `/dev/ttyACM0`、`/dev/video0` 可能会变化。  
但是教学里我们更关心的是：

- 哪个是 `leader`
- 哪个是 `follower`
- 哪个是 `top_camera`
- 哪个是 `wrist_camera`
- `side_camera` 是否作为可选扩展存在

## 2. 先看系统检测结果

```bash
python3 tools/detect_system.py
```

这个命令会把结果写到：

- [report.md](/home/xuan/so101_education/tools/devices/report.md)
- [report.json](/home/xuan/so101_education/tools/devices/report.json)

## 3. 参考命令

```bash
python3 tools/detect_system.py --write-roles-template
python3 tools/detect_system.py
lerobot-find-port
```

## 4. 你需要修改的参数

本章主要不是改命令，而是改角色配置文件 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)。

参考填写方式：

```json
{
  "arms": {
    "leader": {
      "serial": "<LEADER_SERIAL>",
      "port": "<LEADER_BY_ID>"
    },
    "follower": {
      "serial": "<FOLLOWER_SERIAL>",
      "port": "<FOLLOWER_BY_ID>"
    }
  },
  "cameras": {
    "top_camera": {
      "serial": "<TOP_CAMERA_SERIAL>",
      "by_path": "<TOP_CAMERA_BY_PATH>"
    },
    "wrist_camera": {
      "serial": "<WRIST_CAMERA_SERIAL>",
      "by_path": "<WRIST_CAMERA_BY_PATH>"
    },
    "side_camera": {
      "serial": "<SIDE_CAMERA_SERIAL>",
      "by_path": "<SIDE_CAMERA_BY_PATH>"
    }
  }
}
```

## 5. 修改后应达到的效果

- 再次运行 `python3 tools/detect_system.py` 时，报告中能看到 `leader` 和 `follower`
- 如果相机已接好，报告中默认应能看到 `top_camera` 和 `wrist_camera`
- 即使重插设备，工具仍然能恢复这些角色

## 6. 命令改写训练

如果报告中写着：

- `leader -> /dev/ttyACM1`
- `follower -> /dev/ttyACM0`

那么在后续命令中：

- `<LEADER_PORT>` 应改成 `/dev/ttyACM1`
- `<FOLLOWER_PORT>` 应改成 `/dev/ttyACM0`

## 7. 自检问题

- 为什么不能只记住 `/dev/ttyACM0` 是 leader？
- `serial` 和 `by_path` 分别更适合描述哪类设备？

## 8. 本章提交要求

- 提交你填写后的 `device_roles.json`
- 提交一次更新后的 `report.md`

---
**上一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
**下一节：** [03. 主从臂校准](03_calibration.md)
