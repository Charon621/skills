---
name: vetai-evaluation
description: VetAI 评估体系（gold_standard / V1参考集 / 探针工具链）使用方法、指标口径与不可越过的边界。Use when 评估 vetai 诊断效果、跑审计、算一致率或写评估报告时。
---

# VetAI 评估体系使用指南

## 三层参考标准（强度递降，用途不重叠）

| 层级 | 位置 | 标签来源 | 规模 | 可支撑什么 |
|------|------|----------|------|-----------|
| G1/G2 冻结核心集 | `evaluation/gold_standard/` | 本项目收集，双专家盲标+第三方裁决 | 40 例（未开始，阻塞于专家招募） | 唯一能支撑对外准确率结论的路径 |
| V1 参考集 | `evaluation/dataset_reference_set/` | 公开数据集（Mendeley 5dbht54kw7.1）兽医宽泛标签 | 62 例（已就位） | 弃答恰当性/编造部位探针、回归护栏、跨版本比较 |
| 开发集 | `evaluation/pilot_public_images/` | 公开数据集 8 张 | 8 张 | 界面/解析/鲁棒性开发 |

## 不可越过的边界（违反即失去可信度）

1. **V1 不是冻结核心集**：不参与 `top3_etiology_recall` 等核心病因指标，**不能发布准确率**
2. `model_generated_labels_allowed: false` 保持 false——模型自产标签永远不能建立任何评估层级（共享失败模式会让安全指标主动误导）
3. V1 图片是**皮肤镜特写**，与产品真实输入（手机照片）分布不符：主指标是**弃答恰当性**与**是否编造部位**，四类准确率只作探索性数字
4. 金标准完成前，不得对外宣称任何形式的准确率

## 工具链使用顺序

```bash
# 1. 结构审计（无需 API Key）
node evaluation/tools/run_dev_set.js --out evaluation/runs/dev_audit_$(date +%Y%m%d).json

# 2. KB 审计 + 行为探针（npm test 的一部分，也可单跑）
node evaluation/tools/kb_audit.js
node evaluation/tools/recall_probe.js

# 3. V1 评分（弃答恰当性主指标 + 四类探索性指标）
python evaluation/tools/score_v1_reference.py

# 4. 拿到专家标注后：先校验协议再算统计（顺序不能颠倒）
python evaluation/tools/validate_annotations.py --expert X.csv --manifest case_manifest.csv --adjudication Y.csv
python evaluation/tools/agreement_stats.py    # Cohen's κ / Gwet's AC1 / Fleiss' κ / Wilson CI / cluster bootstrap
python evaluation/tools/repeatability.py      # 重测信度
```

## 运行记录规范

- 每次运行写 `evaluation/runs/` 下一个文件，不覆盖旧运行
- 运行记录要带 prompt 版本 SHA-256、KB_VERSION、日期
- 用 V1 调过的提示词版本，其在冻结核心集上的结果仍是首次解盲——必须在运行记录里写清楚

## 指标口径

- 弃答判定五条：图片全不可用 / 边界或部位不清 / 支持证据<2条 / 候选不可区分 / 需触诊实验室
- 正确弃答与正确判断为无异常都算命中 V1 的 `Healthy`（口径需在结果里声明）
- 不可映射的输出不计入分子分母，单独作 `unmappable` 报告
- 置信度是"模型匹配分"不是概率；校准前禁止把分数当真实概率展示

## 版本快照（2026-07-31）

- KB: `2026-07-26-v6`，65 张卡（63 张附来源，全部 draft 待兽医签审）
- Prompt: `vetai-derm-v2.0.0`
- 检索探针：纯文字命中 22/24、方向 19/24；+视觉预检 24/24
