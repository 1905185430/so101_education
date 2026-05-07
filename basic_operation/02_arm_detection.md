# 02. 设备映射与角色绑定

本章的目标是区分“设备身份”和“当前端口号”，并把你的设备绑定到统一的教学角色名上。

如果你现在最关心的是“怎么分清哪只是主臂、哪只是从臂、哪一路是 top/wrist 相机”，请优先阅读：

- [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)

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
- `tools/devices/images/`

第一次运行后，建议依次看这 4 个位置：

1. `report.md` 的“当前角色身份与端口”
2. `report.md` 的“相机固定身份参考”
3. `report.md` 的“填写 device_roles.json 的建议来源”
4. `tools/devices/images/` 下每张截图对应的是哪一路相机

## 3. 参考命令

```bash
python3 tools/detect_system.py --write-roles-template
python3 tools/detect_system.py
lerobot-find-port
```

建议的实际操作顺序是：

1. 先运行 `python3 tools/detect_system.py --write-roles-template`
2. 再运行 `python3 tools/detect_system.py`
3. 打开 `report.md`，抄机械臂的 `by-id` 和相机的 `by_path`
4. 把这些固定身份填入 `device_roles.json`
5. 再运行一次 `python3 tools/detect_system.py`
6. 确认 `leader`、`follower`、`top_camera`、`wrist_camera` 已从 `missing` 变成 `connected`
7. 角色恢复成功后，优先复制检测工具给出的可直接执行命令；如果要做课堂解释，再去看教学版参考命令里的当前 `tty` / `dev`

如果你还不能明确判断主从臂和相机角色，不要在这一章里硬猜。  
先去按 [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md) 里的动作法和截图法做判断，再回来填写。

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
- 报告中的截图能帮助你确认哪一路画面是 `top`，哪一路画面是 `wrist`

## 6. 命令改写训练

如果报告中写着：

- `leader -> /dev/ttyACM1`
- `follower -> /dev/ttyACM0`

那么在后续命令中：

- `<LEADER_PORT>` 应改成 `/dev/ttyACM1`
- `<FOLLOWER_PORT>` 应改成 `/dev/ttyACM0`

相机也是同样的逻辑：

- `device_roles.json` 里优先填写 `top_camera.by_path` 和 `wrist_camera.by_path`
- 真正改 LeRobot 命令时，再填写 `top_camera`、`wrist_camera` 当前的 `/dev/video*`

## 7. 自检问题

- 为什么不能只记住 `/dev/ttyACM0` 是 leader？
- `serial` 和 `by_path` 分别更适合描述哪类设备？
- 如果断电重连后 `top_camera` 从 `/dev/video10` 变成 `/dev/video12`，你应该先改 `device_roles.json` 还是先改命令？

## 8. 本章提交要求

- 提交你填写后的 `device_roles.json`
- 提交一次更新后的 `report.md`

---
**上一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
**辅助教程：** [02A. 如何填写 device_roles.json](02a_device_roles_filling_guide.md)
**下一节：** [03. 主从臂校准](03_calibration.md)
