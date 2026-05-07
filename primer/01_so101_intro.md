# 01. SO-101 导学：开源机械臂、主从控制与校准

## 这一节你会知道什么

- SO-101 在这门课里扮演什么角色
- `leader` 和 `follower` 分别是什么
- 为什么每次上课前都要先做识别和校准

## 核心概念

SO-101 是一类适合教学和模仿学习实验的开源机械臂平台。在本课程里，我们主要关心它和 LeRobot 的结合方式，而不是完整机械设计细节。官方硬件接入说明可参考 [LeRobot SO-101 文档](https://huggingface.co/docs/lerobot/en/so101)。

本课程里会反复出现两个角色：

- `leader`：由学生直接操作，用来示教
- `follower`：跟随 `leader` 的动作，用来执行和回放

这也是为什么后续命令里会分别出现 `--teleop.type=so101_leader` 和 `--robot.type=so101_follower`。

## 为什么角色比端口更重要

机械臂每次插拔之后，系统分配的 `/dev/ttyACM0`、`/dev/ttyACM1` 可能会变化。  
但教学上真正需要稳定的是：

- 哪台机械臂是 `leader`
- 哪台机械臂是 `follower`

所以课程里才会要求学生先通过检测工具确认“角色身份”，再去修改命令里的端口。

## 为什么要校准

机械臂并不是插上就能稳定示教。  
如果 `leader` 和 `follower` 的零位、姿态参考不一致，就会导致：

- 跟随偏差
- 回放不稳定
- 数据质量下降

因此校准不是附加步骤，而是后续遥操作、数据采集和训练的前提。

## 和本课程实验的关系

- 第一次课第一次真正用到本节内容
- 检测工具里最先关注的是 `leader`、`follower` 和当前 `tty`
- 第一批要改写的占位符就是 `<LEADER_PORT>` 和 `<FOLLOWER_PORT>`

## 常见误解

- 误解 1：只要记住 `/dev/ttyACM0` 是主臂就行  
  实际上端口会变，角色不会自动跟着记忆。
- 误解 2：校准只是形式，不影响数据采集  
  实际上校准质量会直接影响动作一致性和训练数据质量。
- 误解 3：`leader` 和 `follower` 的命令可以随便互换  
  两者在课程中的职责不同，对应的参数也不同。

## 资料来源

### 官方文档

- LeRobot SO-101 文档：https://huggingface.co/docs/lerobot/en/so101

### 原始论文

- ACT 原始论文（低成本硬件模仿学习背景）：https://arxiv.org/abs/2304.13705

### 项目/代码

- LeRobot GitHub 仓库：https://github.com/huggingface/lerobot

### 建议延伸阅读

- LeRobot 文档首页：https://huggingface.co/docs/lerobot
- LeRobot 安装文档：https://huggingface.co/docs/lerobot/en/installation
