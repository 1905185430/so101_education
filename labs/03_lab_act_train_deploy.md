# 第三次课：ACT 训练启动与策略部署

本次课的目标是让学生基于第二次课采集的数据，改写训练命令，并根据当前设备扫描结果完成 rollout，同时看懂训练固定参数、输出目录和 checkpoint 的关系。

## 先修导学

- [04. ACT 导学](/home/xuan/so101_education/primer/04_act_intro.md)

建议先理解 `dataset`、`checkpoint`、`rollout` 和 ACT 的基本作用，再进入本次课的训练与部署链路。

## 课前准备

- 第二次课已经得到可用数据集
- 本机或服务器具备可用训练环境
- 学生知道本组的数据集名称

## 课内目标

- 会改写 `<DATASET_REPO_ID>`、`<OUTPUT_DIR>`、`<CHECKPOINT_PATH>`
- 能成功启动 ACT 训练
- 能看懂训练输出目录中的 checkpoint 和日志
- 能在已有 checkpoint 上直接执行或改写 rollout 命令

## 课内步骤

### 1. 先检查训练环境

```bash
python3 tools/detect_system.py
```

### 2. 启动 ACT 训练

执行前先确认：

- `--policy.type=act` 和 `--device=cuda` 是课程固定值
- `<DATASET_REPO_ID>`、`<OUTPUT_DIR>` 才是本组需要按任务改的值
- 输出目录要能让你在课后继续找到 checkpoint

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --output_dir=<OUTPUT_DIR> \
  --job_name=act_so101_lab \
  --device=cuda
```

### 3. 识别训练输出

课堂内至少完成：

- 训练命令改写
- 训练启动
- 理解输出目录
- 能指出后续 rollout 该使用哪个 checkpoint

### 4. rollout 前先确认

- `follower`、`top_camera`、`wrist_camera` 仍然是这次真实连接的设备
- checkpoint 路径要对照本组训练输出确认
- 如果你临时换了设备或重插相机，先重新运行一次检测，不要直接沿用旧命令

确认完以后，再执行下面这条命令。

```bash
lerobot-rollout \
  --robot.type=so101_follower \
  --robot.port=<FOLLOWER_PORT> \
  --robot.cameras='{"top": {"type": "opencv", "index_or_path": "<TOP_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}, "wrist": {"type": "opencv", "index_or_path": "<WRIST_CAMERA_DEV>", "width": 640, "height": 480, "fps": 30}}' \
  --policy.path=<CHECKPOINT_PATH>
```

## 你需要修改的参数

- `<DATASET_REPO_ID>`
- `<OUTPUT_DIR>`
- `<FOLLOWER_PORT>`
- `<TOP_CAMERA_DEV>`
- `<WRIST_CAMERA_DEV>`
- `<CHECKPOINT_PATH>`

## 修改后应达到的效果

- 课堂上能成功启动训练
- 能说明输出目录里 checkpoint 的位置
- 能在已有或课后完成的 checkpoint 上完成 rollout

## 扩展部署说明

如果本组额外接入了 `side_camera`，可以在默认 `top + wrist` 部署成功后，再把第三路视角加入 `robot.cameras` 配置，作为扩展部署练习。默认评分不要求这一项。

## 课内必须完成

- 改写训练命令
- 启动训练
- 截图保存训练日志或输出目录结构
- 改写 rollout 命令草稿

## 课后完成

- 等待训练收敛
- 选择 checkpoint
- 完成 rollout 验证

## 兜底路径

如果课堂机器训练时间过长，可以临时使用教师提供的 checkpoint 完成 rollout 命令改写和部署验证；但学生自己的训练命令和输出目录理解仍然必须提交。

## 提交要求

- 改写后的训练命令
- 训练启动截图或日志截图
- 一份输出目录说明
- 实际执行过的 rollout 命令
- 使用自训或教师 checkpoint 的 rollout 结果截图

## 评分点

- 能正确改写数据集与输出目录参数
- 能成功启动 ACT 训练
- 能解释 checkpoint 来源
- 能完成 rollout 命令改写并验证

## 细化参考

- [06. ACT 训练](/home/xuan/so101_education/basic_operation/06_act_training.md)
- [07. 策略部署](/home/xuan/so101_education/basic_operation/07_policy_deployment.md)
