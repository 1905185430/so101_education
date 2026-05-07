# 03. 主从臂校准

本章的目标是根据当前硬件映射，手动改写校准命令并完成主从臂校准。

## 1. 先查看本章模板

```bash
python3 tools/detect_system.py --show-template calibrate
```

## 2. 参考命令

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT>

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT>
```

## 3. 你需要修改的参数

- `<LEADER_PORT>`：改成检测工具中 `leader` 当前对应的 `tty`
- `<FOLLOWER_PORT>`：改成检测工具中 `follower` 当前对应的 `tty`

## 4. 修改后应达到的效果

- 主臂和从臂都完成校准
- 终端中出现校准成功或保存结果的提示
- 后续遥操作时主从臂不会出现明显零位偏差

## 5. 操作建议

- 校准前先确认主从臂周围没有障碍物
- 校准时严格按照终端提示摆放机械臂姿态
- 如果中途重连设备，要重新运行检测工具，再改写命令

## 6. 命令改写训练

如果检测结果显示：

- `leader -> /dev/ttyACM1`
- `follower -> /dev/ttyACM0`

那么你需要把参考命令中的两个占位符替换成这两个端口，而不是照抄模板。

## 7. 自检问题

- 如果 leader 当前对应 `/dev/ttyACM0`，你需要修改哪一行？
- 为什么校准命令里没有 camera 参数？

## 8. 本章提交要求

- 提交你改写后的两条校准命令
- 说明你替换了哪些参数
- 提交一次校准成功的终端截图

---
**上一节：** [02. 设备映射与角色绑定](02_arm_detection.md)
**下一节：** [04. 带相机的遥操作](04_teleoperation.md)
