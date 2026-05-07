# SO-101 LeRobot 三次课实验书

这套仓库面向课堂教学，当前学生主入口已经重组为 3 次课、3 个实验。当前推荐路径是：先沿着 `detect_system` 给出的基线完成实验，但在每个关键节点都先完成角色和端口确认，再执行命令。

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
python3 tools/detect_system.py --show-template calibrate
python3 tools/detect_system.py --show-template teleoperate
python3 tools/detect_system.py --show-template record
python3 tools/detect_system.py --show-template replay
python3 tools/detect_system.py --show-template rollout
```

检测工具会输出：

- 当前识别到的设备
- `leader`、`follower`、`top_camera`、`wrist_camera` 的当前端口
- 每一路相机当前对应的固定身份标识 `by_path`
- `tools/devices/images/` 下的相机截图
- `tools/devices/report.md`
- 可直接执行命令
- 教学版参考命令模板
- 学生本机应参考的候选替换值

如果第一次使用本仓库，可以先生成角色配置模板：

```bash
python3 tools/detect_system.py --write-roles-template
```

然后由教师或助教根据真实设备填写 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)。

## detect_system 结果怎么用

如果你现在最大的困惑是“不知道怎么分清主臂、从臂、top 相机、wrist 相机，也不知道 `device_roles.json` 该怎么填”，请先看：

- [02A. 如何填写 device_roles.json](basic_operation/02a_device_roles_filling_guide.md)

建议学生每次都按同一顺序操作：

1. 先运行 `python3 tools/detect_system.py`
2. 先看角色是否已经恢复：`leader`、`follower`、`top_camera`、`wrist_camera`
3. 再看固定身份：机械臂优先看 `by-id`，相机优先看 `by_path`
4. 再看这一次真正要执行的当前 `tty` / `dev`
5. 如果角色还是 `missing`，先填写 [device_roles.json](/home/xuan/so101_education/tools/devices/device_roles.json)
6. 重新运行一次 `python3 tools/detect_system.py`，确认角色已经从 `missing` 变成 `connected`
7. 确认截图、角色名和当前端口都对上之后，再执行报告里的“可直接执行命令”
8. 执行完成后，再对照“教学版参考命令”理解参数来源

这里要特别区分两类字段：

- 固定身份标识：用于填写 `device_roles.json`，帮助你在断电重连后恢复角色
- 当前 `tty` / `dev`：用于本次实际执行的 LeRobot 命令

## 这门课里你必须真正看懂的 4 件事

- `leader` 和 `follower` 怎么区分
- `top_camera` 和 `wrist_camera` 怎么区分
- 为什么 `by-id` / `by-path` 用来保存固定身份
- 为什么 LeRobot 命令里填的是当前 `tty` / `dev`，而不是固定身份

## 命令输出模式

现在 `detect_system` 采用“双模式并存”：

- `可直接执行命令`：检测工具已经把当前硬件端口填好，完成关键确认项后可以直接复制
- `教学版参考命令`：保留占位符，用于执行后回看“这些参数为什么这样写”

对于 `record`、`replay`、`rollout` 这类还需要数据集名或 checkpoint 的命令，工具会自动填一组保底默认值。  
报告里会明确标注这些值是“自动默认值，执行前请确认”。

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

## 统一占位符

- `<LEADER_PORT>`
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<WRIST_CAMERA_DEV>`
- `<SIDE_CAMERA_DEV>`（仅扩展说明使用）
- `<DATASET_REPO_ID>`
- `<OUTPUT_DIR>`
- `<CHECKPOINT_PATH>`

## 学生提交要求

- 学生提交自己修改后的命令，而不是原始模板
- 学生说明自己改了哪些参数、这些值来自哪条检测结果
- 每次课至少保留一次终端截图或 `report.md`

## 附录与细化参考

下面这些文档保留为细化章节，用于教师备课或学生补查：

1. [00. 如何从检测结果改写命令](basic_operation/00_command_template_guide.md)
2. [01. 环境搭建与 CLI 验证](basic_operation/01_environment_setup.md)
3. [02. 设备映射与角色绑定](basic_operation/02_arm_detection.md)
4. [02A. 如何填写 device_roles.json](basic_operation/02a_device_roles_filling_guide.md)
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
