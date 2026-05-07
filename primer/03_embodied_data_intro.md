# 03. 具身智能数据采集导学：为什么要录制 demonstration

## 这一节你会知道什么

- 什么是机器人具身智能中的演示数据
- 什么是 observation、action、episode、replay
- 为什么第二次课的数据质量会直接决定第三次课训练效果

## 核心概念

在具身智能任务里，机器人不是只看文本或图片，而是要同时处理视觉、状态和动作。  
本课程里的数据采集，就是把“人怎么操作机器人完成任务”记录成可训练的数据。

在本课程里，默认多视角配置是 `top + wrist`，如果教学现场额外提供第三路 `side` 视角，它被当作可选扩展，而不是主流程必需项。

常见概念包括：

- `observation`：机器人看到和感知到的输入，例如相机画面、关节状态
- `action`：机器人要执行的动作
- `episode`：一次完整任务演示
- `replay`：把录下来的动作重新执行一遍，检查数据是否可信

LeRobot 的真实机器人数据采集流程说明见 [IL Robots](https://huggingface.co/docs/lerobot/en/il_robots)。

## 为什么 replay 很重要

采集完成后，不能直接假设数据可用。  
如果 replay 时都不能稳定复现，就说明可能存在：

- 视角不稳定
- 动作记录异常
- 机械臂状态不同步
- 任务分段不合理

这也是课程里“先录制、再回放、再训练”的原因。

## 什么样的数据更适合训练

对本课程来说，好的数据通常具有这些特点：

- 相机视角稳定
- 任务起止清晰
- 主从臂动作连续
- 回放结果基本可复现

第二次课真正产出的不是“几条视频”，而是一份后续可以进入训练流程的数据集。

## 和本课程实验的关系

- 第二次课第一次集中使用这些概念
- 命令里和数据最直接相关的是 `<DATASET_REPO_ID>`、`<TASK_DESCRIPTION>`、`<EPISODE_INDEX>`
- 第三次课训练时，学生要用第二次课生成的数据集作为输入

## 常见误解

- 误解 1：只要录到了画面就算有数据  
  实际上动作、状态和时间同步同样重要。
- 误解 2：数据条数越多越好  
  低质量数据会拖累训练，课程更强调可回放和稳定性。
- 误解 3：replay 只是演示效果，不影响训练  
  replay 是训练前最直接的数据质量检查。

## 资料来源

### 官方文档

- LeRobot 真实机器人数据采集文档：https://huggingface.co/docs/lerobot/en/il_robots

### 原始论文

- ACT 原始论文：https://arxiv.org/abs/2304.13705

### 项目/代码

- LeRobot GitHub 仓库：https://github.com/huggingface/lerobot

### 建议延伸阅读

- LeRobot 文档首页：https://huggingface.co/docs/lerobot
- LeRobot 推理与部署文档：https://huggingface.co/docs/lerobot/en/inference
