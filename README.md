# 技能库入口

这里按“要做什么”找技能。`skills/` 保持原来的平铺路径，现有安装链接不会失效。

## 独立维护的原创技能

[`high-stakes-ai-evaluation`](https://github.com/Charon621/high-stakes-ai-evaluation)：检查医疗、法律、金融等高风险 AI 的效果声明能不能公开，并指出缺失证据。

## 常用精选

| 技能 | 适合做什么 |
|---|---|
| [`deep-research`](skills/deep-research/SKILL.md) | 做完整调研、事实核查或系统综述 |
| [`nature-reader`](skills/nature-reader/SKILL.md) | 精读一篇论文，保留图表、公式和原文位置 |
| [`nature-writing`](skills/nature-writing/SKILL.md) | 根据研究材料起草或重建论文正文 |
| [`humanize-academic-writing`](skills/humanize-academic-writing/SKILL.md) | 清理学术文本里的机械句式和 AI 痕迹 |
| [`cn-academic-paper-standards`](skills/cn-academic-paper-standards/SKILL.md) | 按国标写中文论文、排三线表和参考文献 |
| [`citation-management`](skills/citation-management/SKILL.md) | 管理 BibTeX、补引用、查重复和格式问题 |
| [`academic-paper-reviewer`](skills/academic-paper-reviewer/SKILL.md) | 投稿前模拟多视角同行评审 |
| [`patent-disclosure-skill`](skills/patent-disclosure-skill/SKILL.md) | 从项目材料挖专利点并写技术交底书 |
| [`llama-factory`](skills/llama-factory/SKILL.md) | 用 LLaMA-Factory 做 SFT、LoRA、DPO 等训练 |
| [`serving-llms-vllm`](skills/serving-llms-vllm/SKILL.md) | 搭建高吞吐 OpenAI 兼容推理服务 |
| [`llama-cpp`](skills/llama-cpp/SKILL.md) | 在 CPU、Mac 或消费级显卡上运行 GGUF 模型 |
| [`qdrant-vector-search`](skills/qdrant-vector-search/SKILL.md) | 构建带过滤和混合检索的生产级 RAG |
| [`vetai-project-context`](skills/vetai-project-context/SKILL.md) | 查看 VetAI 仓库结构、测试命令和工作约定 |

## 完整分类

| 分类 | 数量 | 示例 |
|---|---:|---|
| 学术写作与出版 | 25 | `academic-paper`、`academic-paper-reviewer`、`academic-pipeline`、`academic-plotting`、`academic-writing` |
| 文献检索与研究 | 11 | `arxiv-search`、`autoresearch`、`bgpt-paper-search`、`brainstorming-research-ideas`、`creative-thinking-for-research` |
| 研究记录与知识产物 | 3 | `ara-compiler`、`ara-research-manager`、`ara-rigor-reviewer` |
| 模型评测、安全与可观测 | 13 | `constitutional-ai`、`evaluating-code-models`、`evaluating-llms-harness`、`experiment-tracking-swanlab`、`langsmith-observability` |
| 训练、微调与强化学习 | 21 | `axolotl`、`deepspeed`、`distributed-llm-pretraining-torchtitan`、`fine-tuning-with-trl`、`grpo-rl-training` |
| 模型结构、压缩与可解释性 | 12 | `implementing-llms-litgpt`、`knowledge-distillation`、`long-context`、`mamba-architecture`、`model-merging` |
| 推理、量化与部署 | 11 | `awq-quantization`、`gguf-quantization`、`gptq`、`hqq-quantization`、`llama-cpp` |
| 云算力与基础设施 | 3 | `lambda-labs-gpu-cloud`、`modal-serverless-gpu`、`skypilot-multi-cloud-orchestration` |
| RAG、Agent与结构化输出 | 14 | `autogpt-agents`、`chroma`、`crewai-multi-agent`、`dspy`、`evolving-ai-agents` |
| 数据处理与分词 | 4 | `huggingface-tokenizers`、`nemo-curator`、`ray-data`、`sentencepiece` |
| 多模态、机器人与媒体 | 10 | `audiocraft-audio-generation`、`blip-2-vision-language`、`clip`、`evaluating-cosmos-policy`、`fine-tuning-openvla-oft` |
| 生物医学与统计 | 3 | `Biology`、`Statistics`、`Veterinary` |
| 专利与职业 | 3 | `nature-paper-to-patent`、`patent-disclosure-skill`、`resume-master` |
| 项目专用 | 2 | `vetai-evaluation`、`vetai-project-context` |

完整清单见 [`catalog/技能总索引.md`](catalog/技能总索引.md)，按用户目标重排的入口见 [`catalog/按任务找.md`](catalog/按任务找.md)，来源和维护状态见 [`catalog/来源与待核对.md`](catalog/来源与待核对.md)。

## 安装

单个技能直接安装原始 `SKILL.md`：

```bash
hermes skills install "https://raw.githubusercontent.com/Charon621/skills/main/skills/<技能名>/SKILL.md" --yes
```

克隆后，按需把 `skills/<技能名>/` 复制到当前 profile 的 `$HERMES_HOME/skills/`。

## 维护

技能目录保持平铺，分类由 `catalog/` 索引提供。新增或修改技能后运行：

```bash
python scripts/build_catalog.py
```

这个仓库同时包含社区技能、个人维护技能和项目专用技能。来源未标注或带项目路径的条目见待核对清单。
