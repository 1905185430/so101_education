# 06. ACT 训练

本章的目标是根据你自己采集的数据集名称和训练输出目录，手动改写 ACT 训练命令。

## 1. 训练前先确认两件事

- 你已经完成数据采集
- 你知道自己的数据集名和准备保存模型的目录

可以先运行：

```bash
python3 tools/detect_system.py --stage train
```

## 2. 参考命令

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=<DATASET_REPO_ID> \
  --output_dir=<OUTPUT_DIR> \
  --job_name=act_so101_lab \
  --device=cuda
```

## 3. 你需要修改的参数

- `<DATASET_REPO_ID>`：改成你在上一章录制时使用的数据集名
- `<OUTPUT_DIR>`：改成你自己的训练输出目录

## 4. 修改后应达到的效果

- 训练能正常启动
- 输出目录中能看到日志、配置和 checkpoint
- 后续可以从该目录中选择模型做 rollout

## 5. 固定参数说明

以下参数在本课程中默认不改：

- `--policy.type=act`
- `--job_name=act_so101_lab`
- `--device=cuda`

## 6. 命令改写训练

如果你上一章的数据集名是 `${USER}/so101_pick_place`，想把训练结果保存到 `outputs/act_pick_place_run1`，那么：

- `<DATASET_REPO_ID>` 应改成 `${USER}/so101_pick_place`
- `<OUTPUT_DIR>` 应改成 `outputs/act_pick_place_run1`

## 7. 自检问题

- 为什么训练命令里不需要再写 `<LEADER_PORT>`？
- 哪些参数来自硬件检测，哪些参数来自你自己的实验命名？

## 8. 本章提交要求

- 提交你改写后的训练命令
- 说明你替换了哪两个核心占位符
- 提交训练输出目录截图

---
**上一节：** [05. 数据采集与回放](05_dataset_recording.md)
**下一节：** [07. 策略部署](07_policy_deployment.md)
