# SO-101 LeRobot 三次课实验书

这套仓库面向课堂教学，当前学生主入口已经重组为 3 次课、3 个实验。当前推荐路径是：先运行 `detect_system` 扫描当前硬件，再根据 `device_simple.json` 和相机截图手动填写 LeRobot 命令。

现在仓库采用“两层结构”：

- `primer/`：概念导学，先理解 SO-101、LeRobot、数据采集和 ACT
- `labs/`：三次课实验主线，带着导学知识进入具体操作

## 当前版本

- 当前教学主线：`三次课版`
- 历史稳定版本标签：`v1-eight-chapters`
- 历史版本含义：保留原始 `8` 章节拆分结构，便于教师回溯和细化备课

## 三次课主入口

1. [第一次课：环境验证、设备映射与主从臂校准](labs/01_lab_env_mapping_calibration.md)
2. [第二次课：遥操作、数据采集与回放](labs/02_lab_teleop_record_replay.md)
3. [第三次课：ACT 训练启动与策略部署](labs/03_lab_act_train_deploy.md)

## 导学主入口

建议学生先按下面顺序阅读导学，再进入三次课实验：

1. [00. 课程导览](primer/00_course_map.md)
2. [01. SO-101 导学](primer/01_so101_intro.md)
3. [02. LeRobot 导学](primer/02_lerobot_intro.md)
4. [03. 具身智能数据采集导学](primer/03_embodied_data_intro.md)
5. [04. ACT 导学](primer/04_act_intro.md)

## 课程节奏

### 第一次课

- 课前环境已经预装完成
- 课堂只验证 CLI、识别硬件、绑定角色、完成校准
- 课堂成果是“能看懂报告并写对主从臂命令”

### 第二次课

- 重点改写相机相关占位符
- 课堂完成遥操作、录制数据、回放验证
- 课堂成果是“能采到一份可回放的数据”

### 第三次课

- 课堂启动 ACT 训练并理解输出目录和日志
- 训练收敛允许课后继续
- 课堂或课后使用 checkpoint 完成 rollout

## 核心工具

```bash
python3 tools/detect_system.py
python3 tools/detect_system.py --skip-capture
python3 tools/detect_system.py --format json
```

检测工具会输出：

- 当前识别到的设备
- 机械臂当前 `tty` 与 `by-id`
- 相机当前 `dev` 与 `by-path`
- `tools/devices/images/` 下的相机截图
- [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)

## detect_system 结果怎么用

如果你现在最大的困惑是“不知道怎么分清主臂、从臂、top 相机、wrist 相机”，请先看：

- [02A. 如何根据截图和 device_simple 判断设备角色](basic_operation/02a_device_roles_filling_guide.md)

建议学生每次都按同一顺序操作：

1. 先运行 `python3 tools/detect_system.py`
2. 打开 [device_simple.json](/home/xuan/so101_education/tools/devices/device_simple.json)
3. 先看机械臂的 `tty` 和 `by-id`
4. 再看相机的 `dev`、`by-path` 和 `image`
5. 打开 `tools/devices/images/` 下的截图，确认哪一路是 `top`，哪一路是 `wrist`
6. 再把当前 `tty` / `dev` 手动填入 LeRobot 命令

这里要特别区分两类字段：

- `by-id` / `by-path`：帮助你识别这是哪一个物理设备
- 当前 `tty` / `dev`：用于本次实际执行的 LeRobot 命令

## 这门课里你必须真正看懂的 4 件事

- `leader` 和 `follower` 怎么区分
- `top_camera` 和 `wrist_camera` 怎么区分
- 为什么 `by-id` / `by-path` 更适合识别物理设备
- 为什么 LeRobot 命令里真正要填的是当前 `tty` / `dev`

## 导学资料来源说明

- 实验主线看 `labs/`
- 概念理解看 `primer/`
- 原网站参考链接统一放在每份导学文末的“资料来源”区块
- 链接优先使用官方文档、原始论文和官方仓库页面

## 统一角色名

- `leader`
- `follower`
- `top_camera`
- `wrist_camera`
- `side_camera`（可选扩展）

## 学生提交要求

- 学生提交自己修改后的命令
- 学生说明自己改了哪些参数、这些值来自 `device_simple.json` 的哪一项
- 每次课至少保留一次终端截图或 `device_simple.json`

## 附录与细化参考

下面这些文档保留为细化章节，用于教师备课或学生补查：

1. [00. 如何从检测结果改写命令](basic_operation/00_command_template_guide.md)
2. [01. 环境搭建与 CLI 验证](basic_operation/01_environment_setup.md)
3. [02. 设备映射与角色绑定](basic_operation/02_arm_detection.md)
4. [02A. 如何根据截图和 device_simple 判断设备角色](basic_operation/02a_device_roles_filling_guide.md)
5. [03. 主从臂校准](basic_operation/03_calibration.md)
6. [04. 带相机的遥操作](basic_operation/04_teleoperation.md)
7. [05. 数据采集与回放](basic_operation/05_dataset_recording.md)
8. [06. ACT 训练](basic_operation/06_act_training.md)
9. [07. 策略部署](basic_operation/07_policy_deployment.md)

## 推荐参考

- [LeRobot Installation](https://huggingface.co/docs/lerobot/en/installation)
- [LeRobot SO-101](https://huggingface.co/docs/lerobot/en/so101)
- [LeRobot Real Robot Data Collection](https://huggingface.co/docs/lerobot/en/il_robots)
- [LeRobot Inference / Rollout](https://huggingface.co/docs/lerobot/en/inference)
