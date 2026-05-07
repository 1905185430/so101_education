# 00. 课程导览：这三次课在做什么

## 这一节你会知道什么

- 这门课为什么围绕 SO-101 和 LeRobot 展开
- 三次课分别解决什么问题
- 命令、数据、训练、部署之间是什么关系

## 核心概念

这门课的主线可以概括为一条完整链路：

1. 认识硬件和环境
2. 让机器人能够被正确识别和校准
3. 通过遥操作采集演示数据
4. 用演示数据训练策略
5. 把训练好的策略部署回机器人

这里的 LeRobot 是课程的统一实验框架。它把设备识别、数据采集、训练和部署串成了一条相对稳定的工程工作流，官方文档总入口见 [LeRobot Docs](https://huggingface.co/docs/lerobot)。

## 和本课程实验的关系

- 第一次课解决“设备能不能用、命令怎么改、机械臂怎么校准”
- 第二次课解决“怎么采到一份有效数据”
- 第三次课解决“怎么把数据变成策略，再部署回机器人”

如果把课程比作搭桥：

- 第一次课是在打地基
- 第二次课是在收集材料
- 第三次课是在把材料变成可执行策略

## 常见误解

- 误解 1：这门课的重点只是学几个 CLI 命令  
  实际上重点是理解“命令参数为什么这样改”，命令只是外在形式。
- 误解 2：采到数据就等于能训练  
  数据质量、相机视角和动作同步都会直接影响后续训练效果。
- 误解 3：训练成功就等于部署一定成功  
  部署阶段仍然依赖 follower 端口、相机节点和 checkpoint 路径的正确配置。

## 资料来源

### 官方文档

- LeRobot 文档总入口：https://huggingface.co/docs/lerobot
- LeRobot 安装文档：https://huggingface.co/docs/lerobot/en/installation
- LeRobot SO-101 文档：https://huggingface.co/docs/lerobot/en/so101

### 原始论文

- ACT 原始论文：https://arxiv.org/abs/2304.13705

### 项目/代码

- LeRobot GitHub 仓库：https://github.com/huggingface/lerobot

### 建议延伸阅读

- LeRobot 真实机器人数据采集文档：https://huggingface.co/docs/lerobot/en/il_robots
- LeRobot 推理与部署文档：https://huggingface.co/docs/lerobot/en/inference
