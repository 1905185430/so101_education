# SO-101 LeRobot 教学实验书

这套仓库面向课堂教学，目标不是替学生直接生成可执行命令，而是帮助学生根据自己机器上的硬件映射，正确改写 LeRobot 命令。

## 学习流程

每次做实验都按同一条流程走：

1. 运行检测工具识别当前硬件
2. 查看 `leader`、`follower`、`top_camera`、`side_camera` 的当前端口
3. 打开本章的参考命令模板
4. 手动替换占位符
5. 执行命令并记录结果

## 核心工具

```bash
python3 tools/detect_system.py
python3 tools/detect_system.py --show-template calibrate
python3 tools/detect_system.py --show-template teleoperate
python3 tools/detect_system.py --show-template record
python3 tools/detect_system.py --show-template replay
python3 tools/detect_system.py --show-template rollout
```

检测工具会输出：

- 当前识别到的设备
- 角色身份与当前端口的映射
- `tools/devices/report.md`
- 带占位符的参考命令模板
- 学生需要自己替换的位置

如果第一次使用本仓库，可以先生成角色配置模板：

```bash
python3 tools/detect_system.py --write-roles-template
```

然后由教师或助教根据真实设备填写 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)。

## 统一角色名

全文统一使用下面这组名字：

- `leader`
- `follower`
- `top_camera`
- `side_camera`
- `wrist_camera`

## 统一占位符

学生改写命令时，优先关注这些占位符：

- `<LEADER_PORT>`
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`
- `<DATASET_REPO_ID>`
- `<OUTPUT_DIR>`
- `<CHECKPOINT_PATH>`

## 实验目录

1. [00. 如何从检测结果改写命令](basic_operation/00_command_template_guide.md)
2. [01. 环境搭建与 CLI 验证](basic_operation/01_environment_setup.md)
3. [02. 设备映射与角色绑定](basic_operation/02_arm_detection.md)
4. [03. 主从臂校准](basic_operation/03_calibration.md)
5. [04. 带相机的遥操作](basic_operation/04_teleoperation.md)
6. [05. 数据采集与回放](basic_operation/05_dataset_recording.md)
7. [06. ACT 训练](basic_operation/06_act_training.md)
8. [07. 策略部署](basic_operation/07_policy_deployment.md)

## 课堂要求

- 学生提交自己修改后的命令，而不是原始模板
- 学生说明自己改了哪些参数、为什么这样改
- 每章完成后保留终端截图或 `report.md` 作为实验记录

## 推荐参考

- [LeRobot Installation](https://huggingface.co/docs/lerobot/en/installation)
- [LeRobot SO-101](https://huggingface.co/docs/lerobot/en/so101)
- [LeRobot Real Robot Data Collection](https://huggingface.co/docs/lerobot/en/il_robots)
- [LeRobot Inference / Rollout](https://huggingface.co/docs/lerobot/en/inference)
