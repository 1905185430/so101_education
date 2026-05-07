# 04. ACT 导学：为什么用 Action Chunking with Transformers

## 这一节你会知道什么

- ACT 在这门课里解决什么问题
- 为什么它适合从演示数据学习机器人策略
- 数据集、checkpoint 和 rollout 分别对应算法流程的哪一环

## 核心概念

ACT 全称是 Action Chunking with Transformers，来源于论文 [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)。

这类方法的直观思路是：

- 输入：相机画面、机器人状态等观测
- 输出：不是只预测单步动作，而是预测一段连续动作

“一次预测一段动作”就是 action chunking 的核心思想。  
这样做的好处是，在模仿学习场景里可以降低逐步预测带来的误差累积，也更适合连续操作任务。

## 为什么和这门课匹配

本课程的第二次课会采集多模态演示数据：

- 多路相机
- 主从臂动作
- 明确的 episode 结构

第三次课里，ACT 就是把这些 demonstration 数据变成一个可执行策略。  
课程只要求学生理解训练链路，不要求完整推导论文中的模型细节。

## dataset、checkpoint、rollout 分别是什么

- `dataset`：第二次课采到的数据，是训练输入
- `checkpoint`：训练过程中的模型保存点，是第三次课部署的候选模型
- `rollout`：把选定 checkpoint 部署回真实机器人，看策略能否执行任务

LeRobot 中与训练和部署相关的工作流可参考 [IL Robots](https://huggingface.co/docs/lerobot/en/il_robots) 和 [Inference](https://huggingface.co/docs/lerobot/en/inference)。

## 和本课程实验的关系

- 第三次课第一次集中使用 ACT
- 学生真正要改的是 `<DATASET_REPO_ID>`、`<OUTPUT_DIR>`、`<CHECKPOINT_PATH>`
- 训练和部署不是两件独立的事，而是同一条策略学习链路的前后两端

## 常见误解

- 误解 1：ACT 就是“训练一个模型”，和前两次课关系不大  
  实际上它完全依赖前两次课采到的数据质量。
- 误解 2：checkpoint 只是中间缓存  
  在课程里它是 rollout 的直接输入。
- 误解 3：只要训练启动就等于学会了 ACT  
  真正关键的是理解训练输入是什么、输出保存在哪里、部署时如何选模型。

## 资料来源

### 官方文档

- LeRobot 真实机器人数据采集文档：https://huggingface.co/docs/lerobot/en/il_robots
- LeRobot 推理与部署文档：https://huggingface.co/docs/lerobot/en/inference

### 原始论文

- ACT 原始论文 arXiv：https://arxiv.org/abs/2304.13705
- RSS proceedings PDF：https://roboticsproceedings.org/rss19/p016.pdf

### 项目/代码

- LeRobot GitHub 仓库：https://github.com/huggingface/lerobot

### 建议延伸阅读

- LeRobot 文档首页：https://huggingface.co/docs/lerobot
- LeRobot SO-101 文档：https://huggingface.co/docs/lerobot/en/so101
