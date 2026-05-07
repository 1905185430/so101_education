# 第一次课：环境验证、设备映射与主从臂校准

本次课的目标是让学生在已预装好的 LeRobot 环境中，学会读取检测报告、绑定设备角色，并根据当前端口改写主从臂校准命令。

## 先修导学

- [00. 课程导览](/home/xuan/so101_education/primer/00_course_map.md)
- [01. SO-101 导学](/home/xuan/so101_education/primer/01_so101_intro.md)
- [02. LeRobot 导学](/home/xuan/so101_education/primer/02_lerobot_intro.md)

建议先理解 `leader`、`follower`、角色绑定和 CLI 工作流，再进入本次课的端口识别与校准操作。

## 课前准备

- 教师已完成 LeRobot 与依赖预装
- 学生座位上的主臂、从臂已经接入电脑
- 相机可以接入，但第一次课不要求完成相机实验

## 课内目标

- 会运行 `python3 tools/detect_system.py`
- 会看懂 `leader` 和 `follower` 的当前端口
- 会填写 `device_roles.json`
- 会把 `<LEADER_PORT>`、`<FOLLOWER_PORT>` 改写成自己的端口
- 完成主从臂校准

## 课内步骤

### 1. 验证环境

```bash
lerobot-find-port --help
lerobot-calibrate --help
python3 tools/detect_system.py --stage env
```

### 2. 识别设备并绑定角色

```bash
python3 tools/detect_system.py --write-roles-template
python3 tools/detect_system.py
lerobot-find-port
```

第一次运行 `python3 tools/detect_system.py` 后，请按这个顺序看：

1. 打开 [report.md](/home/xuan/so101_education/tools/devices/report.md)
2. 在“当前角色身份与端口”里看 `leader`、`follower` 当前对应的 `tty`
3. 在“填写 device_roles.json 的建议来源”里抄机械臂的 `by-id` 和 `serial`
4. 如果本组已经接了相机，也顺手看一下 `top_camera`、`wrist_camera` 的 `by_path` 和截图，后面第二次课会直接用到
5. 打开 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)，把 `leader` 和 `follower` 的 `port`、`serial` 填进去
6. 填完以后再运行一次 `python3 tools/detect_system.py`，确认报告中的角色不再是 `missing`

如果你第一次看到：

- `leader: missing`
- `follower: missing`

这是正常的，说明设备已经识别到了，但角色还没有绑定。这个时候先不要急着校准，先去看：

- [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)

如果你重新插拔了主从臂，`/dev/ttyACM*` 可能会变，但只要 `device_roles.json` 里写的是正确的 `by-id`，角色就应该还能恢复成原来的 `leader` / `follower`。

### 3. 参考命令

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=<LEADER_PORT>

lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT>
```

## 你需要修改的参数

- `<LEADER_PORT>`：改成检测报告中 `leader` 当前对应的 `tty`
- `<FOLLOWER_PORT>`：改成检测报告中 `follower` 当前对应的 `tty`

## 修改后应达到的效果

- 主臂和从臂分别完成零位校准
- 终端出现保存结果或校准完成提示
- 后续遥操作时主从臂没有明显零位偏差
- 即使断电重连后重新运行检测，`leader` 和 `follower` 仍然能恢复到正确角色

## 课后任务

- 复查一次 `device_roles.json`
- 用文字说明 `serial`、`by-id`、`ttyACM*` 三者的区别
- 如果课堂上没接相机，课后预习 `top_camera` 和 `wrist_camera` 的角色概念

## 提交要求

- `tools/devices/report.md`
- 填写后的 `tools/devices/device_roles.json`
- 两条改写后的校准命令
- 一张校准成功截图

## 评分点

- 能正确识别 `leader` 和 `follower`
- 能正确填写角色配置文件
- 能手动改写 `<LEADER_PORT>` 和 `<FOLLOWER_PORT>`
- 能完成校准并保留结果

## 细化参考

- [00. 如何从检测结果改写命令](/home/xuan/so101_education/basic_operation/00_command_template_guide.md)
- [01. 环境搭建与 CLI 验证](/home/xuan/so101_education/basic_operation/01_environment_setup.md)
- [02. 设备映射与角色绑定](/home/xuan/so101_education/basic_operation/02_arm_detection.md)
- [02A. 如何填写 device_roles.json](/home/xuan/so101_education/basic_operation/02a_device_roles_filling_guide.md)
- [03. 主从臂校准](/home/xuan/so101_education/basic_operation/03_calibration.md)
