# 02. LeRobot 导学：课程里的统一软件工作流

## 这一节你会知道什么

- LeRobot 在这门课里负责什么
- 为什么课程围绕命令行组织
- 从识别到部署的工作流是怎样串起来的

## 核心概念

[LeRobot](https://huggingface.co/docs/lerobot) 是 Hugging Face 提供的机器人学习框架。对这门课来说，它不是一个抽象名词，而是学生真正使用的实验工作流。

本课程主要使用的命令链路是：

`find-port -> calibrate -> teleoperate -> record -> replay -> train -> rollout`

对应关系如下：

- `lerobot-find-port`：帮助确认设备端口
- `lerobot-calibrate`：校准机械臂
- `lerobot-teleoperate`：进行主从遥操作
- `lerobot-record`：录制演示数据
- `lerobot-replay`：回放已录制轨迹
- `lerobot-train`：训练策略
- `lerobot-rollout`：部署策略执行

官方安装说明见 [Installation](https://huggingface.co/docs/lerobot/en/installation)。

## 为什么课程强调“参考命令 + 学生改写”

本课程不是要训练学生背命令，而是要训练学生从检测结果中找到正确的替换值。

例如：

- 机械臂端口来自检测工具的 `leader/follower`
- 相机节点默认来自 `top_camera/wrist_camera`
- 数据集名和输出目录来自学生自己的实验命名

因此课程提供的是模板，不是成品命令。

## 和本课程实验的关系

- 第一次课主要用到 `find-port` 和 `calibrate`
- 第二次课主要用到 `teleoperate`、`record`、`replay`
- 第三次课主要用到 `train` 和 `rollout`

检测工具并不是替代 LeRobot，而是帮助学生把本机硬件映射成正确的 LeRobot 参数。

## 常见误解

- 误解 1：LeRobot 只是一个训练脚本集合  
  实际上它贯穿设备接入、数据采集、训练和部署。
- 误解 2：只要命令能运行就说明参数一定正确  
  实际上角色、相机、路径写错时，命令也可能运行但结果无效。
- 误解 3：检测工具和 LeRobot 是两套独立系统  
  实际上检测工具是课程对 LeRobot CLI 的教学辅助层。

## 资料来源

### 官方文档

- LeRobot 文档首页：https://huggingface.co/docs/lerobot
- LeRobot 安装文档：https://huggingface.co/docs/lerobot/en/installation
- LeRobot 真实机器人数据采集文档：https://huggingface.co/docs/lerobot/en/il_robots
- LeRobot 推理与部署文档：https://huggingface.co/docs/lerobot/en/inference

### 原始论文

- ACT 原始论文：https://arxiv.org/abs/2304.13705

### 项目/代码

- LeRobot GitHub 仓库：https://github.com/huggingface/lerobot

### 建议延伸阅读

- LeRobot SO-101 文档：https://huggingface.co/docs/lerobot/en/so101
