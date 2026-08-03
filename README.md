# Charon621 Skills

个人 AI 技能仓库（Hermes Agent / Claude 等支持 SKILL.md 规范的 agent 通用）。

每个子目录是一个独立技能，包含 `SKILL.md`（必填）及可选的 `scripts/`、`references/`、`templates/`。

## 技能列表

### 📝 学术写作与去 AI

| 技能 | 说明 | 来源 |
|------|------|------|
| `humanize-academic-writing` | 学术文本去 AI 痕迹，改写为自然的人类学术表达（含 AI 特征检测脚本） | 自装 |
| `research-paper-writing` | 论文写作辅助（完整版） | 预装（Orchestra Research） |
| `academic-writing-assistant` | 学术写作：段落组织、语言润色、论文结构 | 社区 |
| `citation-management` | BibTeX 引用管理：Semantic Scholar 补引、cite key 校验、去重、格式化 | 社区 |

### 🔬 生命科学与医学

| 技能 | 说明 | 来源 |
|------|------|------|
| `biology` | 生物学科普/讲解（按学习者水平适配） | 社区 |
| `arxiv-search` | arXiv 论文检索 | 社区（OpenClaw-Medical-Skills） |
| `bgpt-paper-search` | 论文检索 | 社区（OpenClaw-Medical-Skills） |

### 🐾 兽医与统计

| 技能 | 说明 | 来源 |
|------|------|------|
| `veterinary` | 兽医知识：宠物护理到临床实践与研究 | 社区 |
| `statistics` | 统计学：从基础概率到高级方法 | 社区 |

### 🐶 VetAI 项目专用

| 技能 | 说明 |
|------|------|
| `vetai-project-context` | VetAI 项目速查：结构、测试命令、代码约定、输出规则 |
| `vetai-evaluation` | 评估工具链：三层参考标准、指标口径、不可越过的边界 |

## 本次新增（2026-08-03 批量收录）

以下技能来自公开仓库，按功能分组收录：

### 📄 专利、简历与学术写作

| 技能 | 功能说明 | 来源 |
|------|----------|------|
| `patent-disclosure-skill` | 中国专利：从项目文档挖掘专利点并生成可交付技术交底书（查新、脱敏成文、自检与迭代）；或将已有专利解读为通俗笔记与 Obsidian 知识图谱（叙事故事线、公开线索辅助）。\| China patents: draft technical disclosures from project docs,  | handsomestWei/patent-disclosure-skill |
| `resume-master` | 通过直接编写可编辑的 HTML 源文件，来创建新简历或根据职位描述（JD）量身定制现有简历，最终交付可打印 PDF。当用户需要以下操作时使用：(1) 从头开始创建一份全新的简历；(2) 修改旧简历特别是根据 JD 进行调整。 | wangyafu/resume-skills |

### 📚 Nature 学术工作流（Yuan1z0825/nature-skills）

| 技能 | 功能说明 |
|------|----------|
| `nature-academic-search` | Multi-source literature search, citation verification, strict independent other-citation audits, article-level citation metric tables, influential cit |
| `nature-citation` | Add strict Nature/CNS citations to manuscript text by splitting long passages into citable segments, searching only accepted flagship and subjournal t |
| `nature-data` | Prepare, audit, or revise Nature-ready Data Availability statements, data repository plans, dataset citations, and FAIR metadata checklists for manusc |
| `nature-downloader` |  |
| `nature-experiment-log` | 标准化实验日志记录——直接上传或读取本地图片、语音和文字，产出带 YAML frontmatter 的 Markdown；可选集成飞书 CLI 与 Obsidian。 |
| `nature-figure` | Create, revise, audit, and export submission-grade scientific figures for Nature-family and other high-impact venues in Python (matplotlib/seaborn) or |
| `nature-literature-pipeline` | Complete automated literature discovery pipeline: multi-source search → six-dimension scoring → fine reading → formatted delivery → archival. Combines |
| `nature-paper-card` | Build a source-grounded deep-reading Paper Card for one scientific paper, preprint, PDF, DOI, arXiv page, publisher article, or pasted paper text. Use |
| `nature-paper-to-patent` | Convert scientific papers, theses, technical reports, source code, figures, inventor notes, or research manuscripts into evidence-grounded Chinese inv |
| `nature-paper2ppt` | Build a complete Nature-style Chinese PPTX presentation from a scientific paper, preprint, PDF, article text, figure legends, or reading notes. Use fo |
| `nature-polishing` | Polish, restructure, or translate academic prose into Nature-leaning English using writing-strategy principles, curated Nature/Nature Communications a |
| `nature-reader` | Build full-paper Chinese-English side-by-side, figure/table/equation-aware, source-grounded Markdown readers for journal or conference papers from PDF |
| `nature-ref-verifier` | 对学术文献逐条执行多源交叉验证，逐字段对比作者、标题、年份、卷期、页码， 标记卷年/DOI年冲突、作者顺序异常、页码偏差等问题，输出结构化验证报告。 可批量处理整篇论文/开题报告的参考文献列表，也可单条校验，支持与 Zotero 同步修正。 |
| `nature-response` | Draft, audit, or revise Nature-style revision correspondence packages: point-by-point reviewer response letters, rebuttal letters, revision cover lett |
| `nature-reviewer` | Simulate a Nature-style reviewer assessment from the referee perspective rather than an author rebuttal. Use when the user wants a pre-submission revi |
| `nature-shared` | Internal shared-reference support package for installed nature-writing, nature-polishing, nature-reader, and nature-paper2ppt skills. Do not invoke it |
| `nature-statistics` | Audit, revise, or draft manuscript statistical reporting for Nature / high-impact journal submissions. Use when the user asks to check statistical ana |
| `nature-writing` | Draft, restructure, or plan Nature-style manuscript sections and initial-submission materials from author-provided claims, results, figures, notes, or |
| `researchwrite` |  |

### 🎓 学术研究流水线（Imbad0202/academic-research-skills）

| 技能 | 功能说明 |
|------|----------|
| `academic-paper` | 12-agent academic paper writing pipeline. 11 modes (full/plan/outline/revision/revision-coach/abstract/lit-review/format-convert/citation-check/disclo |
| `academic-paper-reviewer` | Multi-perspective academic paper review with dynamic reviewer personas. Simulates 5 independent reviewers (Journal-Fit Reviewer + 3 peer reviewers + D |
| `academic-pipeline` | Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> re-revise -> final inte |
| `deep-research` | Universal deep research agent team. 13-agent pipeline for rigorous academic research on any topic. 8 modes: full research, quick brief, paper review,  |

### 🤖 LLM/AI 研究技能（Orchestra-Research/AI-research-SKILLs，98 个）

| 技能 | 功能说明 |
|------|----------|
**研究产物**
| `ara-compiler` | Compiles any research input — PDF papers, GitHub repositories, experiment logs, code directories, or raw notes — into a complete Agent-Native Research |
| `ara-research-manager` | Records research provenance as a post-task epilogue, scanning conversation history at the end of a coding or research session to extract decisions, ex |
| `ara-rigor-reviewer` | Performs ARA Seal Level 2 semantic epistemic review on Agent-Native Research Artifacts, scoring six dimensions (evidence relevance, falsifiability, sc |
**Agent 框架**
| `autogpt-agents` | Autonomous AI agent platform for building and deploying continuous agents. Use when creating visual workflow agents, deploying persistent autonomous a |
| `crewai-multi-agent` | Multi-agent orchestration framework for autonomous AI collaboration. Use when building teams of specialized agents working together on complex tasks,  |
| `evolving-ai-agents` | Provides guidance for automatically evolving and optimizing AI agents across any domain using LLM-driven evolution algorithms. Use when building self- |
| `langchain` | Framework for building LLM-powered applications with agents, chains, and RAG. Supports multiple providers (OpenAI, Anthropic, Google), 500+ integratio |
| `llamaindex` | Data framework for building LLM applications with RAG. Specializes in document ingestion (300+ connectors), indexing, and querying. Features vector in |
**自主研究**
| `autoresearch` | Orchestrates end-to-end autonomous AI research projects using a two-loop architecture. The inner loop runs rapid experiment iterations with clear opti |
**数据处理**
| `nemo-curator` | GPU-accelerated data curation for LLM training. Supports text/image/video/audio. Features fuzzy deduplication (16× faster), quality filtering (30+ heu |
| `ray-data` | Scalable data processing for ML workloads. Streaming execution across CPU/GPU, supports Parquet/CSV/JSON/images. Integrates with Ray Train, PyTorch, T |
**分布式训练**
| `deepspeed` | Expert guidance for distributed training with DeepSpeed - ZeRO optimization stages, pipeline parallelism, FP16/BF16/FP8, 1-bit Adam, sparse attention |
| `huggingface-accelerate` | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic de |
| `pytorch-fsdp2` | Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpointing. Use w |
| `pytorch-lightning` | High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerplate. Scale |
| `ray-train` | Distributed training orchestration across clusters. Scales PyTorch/TensorFlow/HuggingFace from laptop to 1000s of nodes. Built-in hyperparameter tunin |
| `training-llms-megatron` | Trains large language models (2B-462B parameters) using NVIDIA Megatron-Core with advanced parallelism strategies. Use when training models >1B parame |
**前沿技术**
| `knowledge-distillation` | Compress large language models using knowledge distillation from teacher to student models. Use when deploying smaller models with retained performanc |
| `long-context` | Extend context windows of transformer models using RoPE, YaRN, ALiBi, and position interpolation techniques. Use when processing long documents (32k-1 |
| `model-merging` | Merge multiple fine-tuned models using mergekit to combine capabilities without retraining. Use when creating specialized models by blending domain-sp |
| `model-pruning` | Reduce LLM size and accelerate inference using pruning techniques like Wanda and SparseGPT. Use when compressing models without retraining, achieving  |
| `moe-training` | Train Mixture of Experts (MoE) models using DeepSpeed or HuggingFace. Use when training large-scale models with limited compute (5× cost reduction vs  |
| `speculative-decoding` | Accelerate LLM inference using speculative decoding, Medusa multiple heads, and lookahead decoding techniques. Use when optimizing inference speed (1. |
**评测**
| `evaluating-code-models` | Evaluates code generation models across HumanEval, MBPP, MultiPL-E, and 15+ benchmarks with pass@k metrics. Use when benchmarking code models, compari |
| `evaluating-llms-harness` | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models,  |
| `nemo-evaluator-sdk` | Evaluates LLMs across 100+ benchmarks from 18+ harnesses (MMLU, HumanEval, GSM8K, safety, VLM) with multi-backend execution. Use when needing scalable |
**微调**
| `axolotl` | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support |
| `llama-factory` | Expert guidance for fine-tuning LLMs with LLaMA-Factory - WebUI no-code, 100+ models, 2/3/4/5/6/8-bit QLoRA, multimodal support |
| `peft-fine-tuning` | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when  |
| `unsloth` | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization |
**推理服务**
| `llama-cpp` | Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when C |
| `serving-llms-vllm` | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference lat |
| `sglang` | Fast structured generation and serving for LLMs with RadixAttention prefix caching. Use for JSON/regex outputs, constrained decoding, agentic workflow |
| `tensorrt-llm` | Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when |
**基础设施**
| `lambda-labs-gpu-cloud` | Reserved and on-demand GPU cloud instances for ML training and inference. Use when you need dedicated GPU instances with simple SSH access, persistent |
| `modal-serverless-gpu` | Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models  |
| `skypilot-multi-cloud-orchestration` | Multi-cloud orchestration for ML workloads with automatic cost optimization. Use when you need to run training or batch jobs across multiple clouds, l |
**可解释性**
| `nnsight-remote-interpretability` | Provides guidance for interpreting and manipulating neural network internals using nnsight with optional NDIF remote execution. Use when needing to ru |
| `pyvene-interventions` | Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative intervention framework. Use when conducting causal  |
| `sparse-autoencoder-training` | Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable featu |
| `transformer-lens-interpretability` | Provides guidance for mechanistic interpretability research using TransformerLens to inspect and manipulate transformer internals via HookPoints and a |
**论文写作**
| `academic-plotting` | Generates publication-quality figures for ML papers from research context. Given a paper section or description, extracts system components and relati |
| `ml-paper-writing` | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, ve |
| `presenting-conference-talks` | Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script. Use when prepa |
| `systems-paper-writing` | Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys. Provides paragraph-level structural blueprints, writin |
**MLOps**
| `experiment-tracking-swanlab` | Provides guidance for experiment tracking with SwanLab. Use when you need open-source run tracking, local or self-hosted dashboards, and lightweight m |
| `mlflow` | Track ML experiments, manage model registry with versioning, deploy models to production, and reproduce experiments with MLflow - framework-agnostic M |
| `tensorboard` | Visualize training metrics, debug models with histograms, compare experiments, visualize model graphs, and profile performance with TensorBoard - Goog |
| `weights-and-biases` | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B |
**模型架构**
| `distributed-llm-pretraining-torchtitan` | Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP). Use when pretraining Llama 3.1, DeepSeek |
| `implementing-llms-litgpt` | Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama, Gemma, Phi, Qwen, Mistral). Use when need clean model |
| `mamba-architecture` | State-space model with O(n) complexity vs Transformers' O(n²). 5× faster inference, million-token sequences, no KV cache. Selective SSM with hardware- |
| `nanogpt` | Educational GPT implementation in ~300 lines. Reproduces GPT-2 (124M) on OpenWebText. Clean, hackable code for learning transformers. By Andrej Karpat |
| `rwkv-architecture` | RNN+Transformer hybrid with O(n) inference. Linear time, infinite context, no KV cache. Train like GPT (parallel), infer like RNN (sequential). Linux  |
**多模态**
| `audiocraft-audio-generation` | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text de |
| `blip-2-vision-language` | Vision-language pre-training framework bridging frozen image encoders and LLMs. Use when you need image captioning, visual question answering, image-t |
| `clip` | OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M |
| `evaluating-cosmos-policy` | Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments. Use when setting up cosmos-policy for robot manipulation evaluation, ru |
| `fine-tuning-openvla-oft` | Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot action generation with continuous action heads, LoRA adaptation, and FiLM con |
| `fine-tuning-serving-openpi` | Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast, pi0.5) using JAX or PyTorch backends for robot policy inference across ALOHA,  |
| `llava` | Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA l |
| `segment-anything-model` | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as pr |
| `stable-diffusion-image-generation` | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, perfor |
| `whisper` | OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six mode |
**可观测性**
| `langsmith-observability` | LLM observability platform for tracing, evaluation, and monitoring. Use when debugging LLM applications, evaluating model outputs against datasets, mo |
| `phoenix-observability` | Open-source AI observability platform for LLM tracing, evaluation, and monitoring. Use when debugging LLM applications with detailed traces, running e |
**优化**
| `awq-quantization` | Activation-aware weight quantization for 4-bit LLM compression with 3x speedup and minimal accuracy loss. Use when deploying large models (7B-70B) on  |
| `gguf-quantization` | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing |
| `gptq` | Post-training 4-bit quantization for LLMs with minimal accuracy loss. Use for deploying large models (70B, 405B) on consumer GPUs, when you need 4× me |
| `hqq-quantization` | Half-Quadratic Quantization for LLMs without calibration data. Use when quantizing models to 4/3/2-bit precision without needing calibration datasets, |
| `ml-training-recipes` | Battle-tested PyTorch training recipes for all domains — LLMs, vision, diffusion, medical imaging, protein/drug discovery, spatial omics, genomics. Co |
| `optimizing-attention-flash` | Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long se |
| `quantizing-models-bitsandbytes` | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memory is limited, need to fit larger models, or |
**后训练**
| `fine-tuning-with-trl` | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and |
| `grpo-rl-training` | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training |
| `miles-rl-training` | Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime. Use when training large MoE models with FP8/INT4, ne |
| `openrlhf-training` | High-performance RLHF framework with Ray+vLLM acceleration. Use for PPO, GRPO, RLOO, DPO training of large models (7B-70B+). Built on Ray, vLLM, ZeRO- |
| `simpo-training` | Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No refere |
| `slime-rl-training` | Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. Use when training GLM models, implementing custom data gener |
| `torchforge-rl-training` | Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra from algorithms. Use when you want clean RL abstract |
| `verl-rl-training` | Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL). Use when implementing RLHF, GRPO, PPO, or other RL alg |
**提示工程**
| `dspy` | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP' |
| `guidance` | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with  |
| `instructor` | Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and  |
| `outlines` | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and m |
**RAG**
| `chroma` | Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-f |
| `faiss` | Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index  |
| `pinecone` | Managed vector database for production AI applications. Fully managed, auto-scaling, with hybrid search (dense + sparse), metadata filtering, and name |
| `qdrant-vector-search` | High-performance vector similarity search engine for RAG and semantic search. Use when building production RAG systems requiring fast nearest neighbor |
| `sentence-transformers` | Framework for state-of-the-art sentence, text, and image embeddings. Provides 5000+ pre-trained models for semantic similarity, clustering, and retrie |
**研究构思**
| `brainstorming-research-ideas` | Guides researchers through structured ideation frameworks to discover high-impact research directions. Use when exploring new problem spaces, pivoting |
| `creative-thinking-for-research` | Applies cognitive science frameworks for creative thinking to CS and AI research ideation. Use when seeking genuinely novel research directions by lev |
**安全对齐**
| `constitutional-ai` | Anthropic's method for training harmless AI through self-improvement. Two-phase approach - supervised learning with self-critique/revision, then RLAIF |
| `llamaguard` | Meta's 7-8B specialized moderation model for LLM input/output filtering. 6 safety categories - violence/hate, sexual content, weapons, substances, sel |
| `nemo-guardrails` | NVIDIA's runtime safety framework for LLM applications. Features jailbreak detection, input/output validation, fact-checking, hallucination detection, |
| `prompt-guard` | Meta's 86M prompt injection and jailbreak detector. Filters malicious prompts and third-party data for LLM apps. 99%+ TPR, <1% FPR. Fast (<2ms GPU). M |
**分词**
| `huggingface-tokenizers` | Fast tokenizers optimized for research and production. Rust-based implementation tokenizes 1GB in <20 seconds. Supports BPE, WordPiece, and Unigram al |
| `sentencepiece` | Language-independent tokenizer treating text as raw Unicode. Supports BPE and Unigram algorithms. Fast (50k sentences/sec), lightweight (6MB memory),  |

## 安装方法

### 方式一：hermes skills install（推荐，直接走仓库 URL）

```bash
# 单个技能
hermes skills install "https://raw.githubusercontent.com/Charon621/skills/main/skills/<技能名>/SKILL.md" --yes
```

### 方式二：克隆到用户技能目录

```bash
git clone https://github.com/Charon621/skills.git
# 把需要的技能目录复制到 ~/AppData/Local/hermes/skills/ 下即可
```

### 方式三：skills.sh 注册后（可选）

本仓库结构符合 skills.sh 多技能仓库规范（`owner/repo/skill-name`），
发布到 skills.sh 后可直接 `hermes skills install skills-sh/Charon621/skills/<技能名>`。

## 技能规范

- `SKILL.md` 使用 YAML frontmatter：`name`、`description`
- 脚本放 `scripts/`，参考资料放 `references/`，模板放 `templates/`
- 社区技能保留原作者 frontmatter（`metadata`、license 字段原样保留）
- 仓库内不存放任何 API Key 或敏感信息
