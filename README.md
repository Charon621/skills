# 技能库入口

按“要做什么”找技能。技能按分类存放在 `skills/<分类>/<技能名>/`，与下方中文分类一一对应。

## 查找技能

- **按任务**：[`catalog/按任务找.md`](catalog/按任务找.md) —— 按使用场景挑推荐技能
- **按分类**：下方“完整分类”表，或 [`catalog/技能总索引.md`](catalog/技能总索引.md)（含每个技能的中文简介）
- **按关键词**：`node skill-index.mjs search . <关键词> --rules ml-skills-rules.json --labels scripts/summaries-zh.json`（中英文均可，中文命中中文简介）

## 常用精选

| 技能 | 适合做什么 |
|---|---|
| [`deep-research`](skills/research-workflow/deep-research/SKILL.md) | 做完整调研、事实核查或系统综述 |
| [`nature-reader`](skills/nature-suite/nature-reader/SKILL.md) | 精读一篇论文，保留图表、公式和原文位置 |
| [`nature-writing`](skills/nature-suite/nature-writing/SKILL.md) | 根据研究材料起草或重建论文正文 |
| [`humanize-academic-writing`](skills/paper-writing/humanize-academic-writing/SKILL.md) | 清理学术文本里的机械句式和 AI 痕迹 |
| [`cn-academic-paper-standards`](skills/paper-writing/cn-academic-paper-standards/SKILL.md) | 按国标写中文论文、排三线表和参考文献 |
| [`citation-management`](skills/paper-writing/citation-management/SKILL.md) | 管理 BibTeX、补引用、查重复和格式问题 |
| [`academic-paper-reviewer`](skills/paper-writing/academic-paper-reviewer/SKILL.md) | 投稿前模拟多视角同行评审 |
| [`patent-disclosure-skill`](skills/research-workflow/patent-disclosure-skill/SKILL.md) | 从项目材料挖专利点并写技术交底书 |
| [`llama-factory`](skills/fine-tuning/llama-factory/SKILL.md) | 用 LLaMA-Factory 做 SFT、LoRA、DPO 等训练 |
| [`serving-llms-vllm`](skills/inference-serving/serving-llms-vllm/SKILL.md) | 搭建高吞吐 OpenAI 兼容推理服务 |
| [`llama-cpp`](skills/inference-serving/llama-cpp/SKILL.md) | 在 CPU、Mac 或消费级显卡上运行 GGUF 模型 |
| [`qdrant-vector-search`](skills/rag-vector/qdrant-vector-search/SKILL.md) | 构建带过滤和混合检索的生产级 RAG |
| [`vetai-project-context`](skills/project-vetai/vetai-project-context/SKILL.md) | 查看 VetAI 仓库结构、测试命令和工作约定 |

## 完整分类

| 分类 | 数量 | 目录 | 示例 |
|---|---:|---|---|
| Nature 论文套件 | 18 | [`skills/nature-suite/`](skills/nature-suite/) | `nature-academic-search`、`nature-citation`、`nature-data`、`nature-downloader`、`nature-experiment-log` |
| 论文写作与投稿 | 14 | [`skills/paper-writing/`](skills/paper-writing/) | `academic-paper`、`academic-paper-reviewer`、`academic-paper-workflow`、`academic-pipeline`、`academic-plotting` |
| 文献检索与研究流程 | 10 | [`skills/research-workflow/`](skills/research-workflow/) | `ara-compiler`、`ara-research-manager`、`ara-rigor-reviewer`、`arxiv-search`、`autoresearch` |
| 微调与对齐训练 | 6 | [`skills/fine-tuning/`](skills/fine-tuning/) | `axolotl`、`fine-tuning-with-trl`、`llama-factory`、`peft-fine-tuning`、`simpo-training` |
| 强化学习训练 | 6 | [`skills/rl-training/`](skills/rl-training/) | `grpo-rl-training`、`miles-rl-training`、`openrlhf-training`、`slime-rl-training`、`torchforge-rl-training` |
| 分布式训练基础设施 | 11 | [`skills/training-infra/`](skills/training-infra/) | `deepspeed`、`distributed-llm-pretraining-torchtitan`、`huggingface-accelerate`、`implementing-llms-litgpt`、`ml-training-recipes` |
| 量化、压缩与合并 | 8 | [`skills/quantization-compression/`](skills/quantization-compression/) | `awq-quantization`、`gguf-quantization`、`gptq`、`hqq-quantization`、`knowledge-distillation` |
| 推理部署与加速 | 6 | [`skills/inference-serving/`](skills/inference-serving/) | `llama-cpp`、`optimizing-attention-flash`、`serving-llms-vllm`、`sglang`、`speculative-decoding` |
| 模型架构与分词 | 5 | [`skills/model-architecture/`](skills/model-architecture/) | `huggingface-tokenizers`、`long-context`、`mamba-architecture`、`rwkv-architecture`、`sentencepiece` |
| RAG 与向量检索 | 6 | [`skills/rag-vector/`](skills/rag-vector/) | `chroma`、`faiss`、`llamaindex`、`pinecone`、`qdrant-vector-search` |
| Agent 框架与结构化输出 | 8 | [`skills/agent-frameworks/`](skills/agent-frameworks/) | `autogpt-agents`、`crewai-multi-agent`、`dspy`、`evolving-ai-agents`、`guidance` |
| 多模态与媒体生成 | 7 | [`skills/multimodal-media/`](skills/multimodal-media/) | `audiocraft-audio-generation`、`blip-2-vision-language`、`clip`、`llava`、`segment-anything-model` |
| 机器人与具身策略 | 3 | [`skills/robotics/`](skills/robotics/) | `evaluating-cosmos-policy`、`fine-tuning-openvla-oft`、`fine-tuning-serving-openpi` |
| 可解释性研究 | 4 | [`skills/interpretability/`](skills/interpretability/) | `nnsight-remote-interpretability`、`pyvene-interventions`、`sparse-autoencoder-training`、`transformer-lens-interpretability` |
| 模型评测 | 3 | [`skills/evaluation-benchmarks/`](skills/evaluation-benchmarks/) | `evaluating-code-models`、`evaluating-llms-harness`、`nemo-evaluator-sdk` |
| 安全与护栏 | 4 | [`skills/safety-guardrails/`](skills/safety-guardrails/) | `constitutional-ai`、`llamaguard`、`nemo-guardrails`、`prompt-guard` |
| 实验跟踪与可观测 | 6 | [`skills/observability-tracking/`](skills/observability-tracking/) | `experiment-tracking-swanlab`、`langsmith-observability`、`mlflow`、`phoenix-observability`、`tensorboard` |
| 数据处理与清洗 | 2 | [`skills/data-engineering/`](skills/data-engineering/) | `nemo-curator`、`ray-data` |
| 云算力平台 | 3 | [`skills/gpu-cloud/`](skills/gpu-cloud/) | `lambda-labs-gpu-cloud`、`modal-serverless-gpu`、`skypilot-multi-cloud-orchestration` |
| 学科知识 | 3 | [`skills/domain-science/`](skills/domain-science/) | `biology`、`statistics`、`veterinary` |
| 职业与效率 | 1 | [`skills/productivity/`](skills/productivity/) | `resume-master` |
| 项目专用（VetAI） | 2 | [`skills/project-vetai/`](skills/project-vetai/) | `vetai-evaluation`、`vetai-project-context` |

完整清单见 [`catalog/技能总索引.md`](catalog/技能总索引.md)，按用户目标重排的入口见 [`catalog/按任务找.md`](catalog/按任务找.md)，来源和维护状态见 [`catalog/来源与待核对.md`](catalog/来源与待核对.md)。

## 安装

单个技能直接安装原始 `SKILL.md`（注意 URL 带分类目录）：

```bash
hermes skills install "https://raw.githubusercontent.com/Charon621/skills/main/skills/<分类>/<技能名>/SKILL.md" --yes
```

克隆后，按需把 `skills/<分类>/<技能名>/` 复制到当前 profile 的 `$HERMES_HOME/skills/`。

## 维护

技能按分类目录存放（22 个分类，清单与中文名见 `scripts/build_catalog.py` 的 `CATEGORY_ORDER` / `CATEGORY_LABELS`）。新增技能放进对应分类目录后运行：

```bash
python scripts/build_catalog.py
node skill-index.mjs scan . --rules ml-skills-rules.json --labels scripts/summaries-zh.json
```

`skill-index.mjs` 额外生成机器可读的 `skills.json` 与 `INDEX.md`，并支持关键词检索：`node skill-index.mjs search . <关键词> --rules ml-skills-rules.json --labels scripts/summaries-zh.json`。中文简介统一维护在 `scripts/summaries-zh.json`，新增技能时补一条即可。

这个仓库同时包含社区技能、个人维护技能和项目专用技能。来源未标注或带项目路径的条目见待核对清单。
