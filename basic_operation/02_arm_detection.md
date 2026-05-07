# 02. 设备识别与端口判断

本章的目标只做两件事：区分主从臂与相机角色，以及区分“识别字段”和“当前端口号”。

如果你现在最关心的是“怎么分清哪只是主臂、哪只是从臂、哪一路是 top/wrist 相机”，请优先阅读：

- [02A. 如何根据截图和 device_simple 判断设备角色](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)

## 1. 为什么要先做设备识别

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

- [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)
- `tools/devices/images/`

第一次运行后，建议依次看这 4 个位置：

1. `device_simple.json` 的 `arms`
2. `device_simple.json` 的 `cameras`
3. 每一路相机的 `by-path` / `by-id`
4. `tools/devices/images/` 下每张截图对应的是哪一路相机

## 3. 建议的实际操作顺序

```bash
python3 tools/detect_system.py
lerobot-find-port
```

1. 运行 `python3 tools/detect_system.py`
2. 打开 `device_simple.json`
3. 记录两只机械臂的 `tty` 和 `by-id`
4. 打开截图，判断哪一路是 `top_camera`、哪一路是 `wrist_camera`
5. 再回到 `device_simple.json`，记录相机的当前 `dev`
6. 最后把这些当前端口写入 LeRobot 命令

如果你还不能明确判断主从臂和相机角色，不要在这一章里硬猜。  
先去按 [02A. 如何根据截图和 device_simple 判断设备角色](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md) 里的动作法和截图法做判断，再回来写命令。

## 4. 修改后应达到的效果

- `device_simple.json` 能列出当前机械臂和相机
- 相机截图能帮助你确认哪一路画面是 `top`，哪一路画面是 `wrist`
- 你能根据当前 `tty` / `dev` 手动改写 LeRobot 命令

## 5. 这一章你必须看懂的两件事

- 哪只是 `leader`、哪只是 `follower`
- `by-id / by_path` 用来帮你识别设备，而当前 `/dev/ttyACM*`、`/dev/video*` 只用于这一次执行

## 6. 命令改写训练

如果报告中写着：

- `leader -> /dev/ttyACM1`
- `follower -> /dev/ttyACM0`

那么在后续命令中：

- `<LEADER_PORT>` 应改成 `/dev/ttyACM1`
- `<FOLLOWER_PORT>` 应改成 `/dev/ttyACM0`

相机也是同样的逻辑：

- 先用截图确认哪一路是 `top_camera`、哪一路是 `wrist_camera`
- 真正改 LeRobot 命令时，再填写它们当前的 `/dev/video*`

## 7. 自检问题

- 为什么不能只记住 `/dev/ttyACM0` 是 leader？
- `serial` 和 `by_path` 分别更适合描述哪类设备？
- 如果断电重连后 `top_camera` 从 `/dev/video10` 变成 `/dev/video12`，你应该先重新检测还是直接照抄旧命令？

## 8. 本章提交要求

- 提交一次更新后的 `device_simple.json`
- 提交你记录下来的相机截图判断结果

---
**上一节：** [01. 环境搭建与 CLI 验证](01_environment_setup.md)
**辅助教程：** [02A. 如何根据截图和 device_simple 判断设备角色](02a_device_roles_filling_guide.md)
**下一节：** [03. 主从臂校准](03_calibration.md)
