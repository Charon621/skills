#!/usr/bin/env python3
"""Build searchable catalog pages for the flat skills collection."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CATALOG = ROOT / "catalog"


def frontmatter(text: str) -> str:
    if text.startswith("---") and text.count("---") >= 2:
        return text.split("---", 2)[1]
    return ""


def field(fm: str, key: str) -> str:
    lines = fm.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^" + re.escape(key) + r":\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip().strip('"')
        if value not in {"|", "|-", ">", ">-"}:
            return value
        collected = []
        for following in lines[index + 1:]:
            if following and not following[0].isspace():
                break
            stripped = following.strip()
            if stripped:
                collected.append(stripped)
        return " ".join(collected)
    return ""


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:180] + ("…" if len(text) > 180 else "")


CATEGORY_MEMBERS = {
    "学术写作与出版": {
        "academic-paper", "academic-paper-reviewer", "academic-pipeline", "academic-plotting",
        "academic-writing-assistant", "citation-management", "humanize-academic-writing",
        "ml-paper-writing", "nature-citation", "nature-data", "nature-experiment-log",
        "nature-figure", "nature-paper2ppt", "nature-polishing", "nature-ref-verifier",
        "nature-response", "nature-reviewer", "nature-shared", "nature-statistics",
        "nature-writing", "presenting-conference-talks", "research-paper-writing",
        "researchwrite", "systems-paper-writing",
    },
    "文献检索与研究": {
        "arxiv-search", "autoresearch", "bgpt-paper-search", "brainstorming-research-ideas",
        "creative-thinking-for-research", "deep-research", "nature-academic-search",
        "nature-downloader", "nature-literature-pipeline", "nature-paper-card", "nature-reader",
    },
    "研究记录与知识产物": {
        "ara-compiler", "ara-research-manager", "ara-rigor-reviewer",
    },
    "模型评测、安全与可观测": {
        "constitutional-ai", "evaluating-code-models", "evaluating-llms-harness",
        "experiment-tracking-swanlab", "langsmith-observability", "llamaguard", "mlflow",
        "nemo-evaluator-sdk", "nemo-guardrails", "phoenix-observability", "prompt-guard",
        "tensorboard", "weights-and-biases",
    },
    "训练、微调与强化学习": {
        "axolotl", "deepspeed", "distributed-llm-pretraining-torchtitan",
        "fine-tuning-with-trl", "grpo-rl-training", "huggingface-accelerate", "llama-factory",
        "miles-rl-training", "ml-training-recipes", "moe-training", "openrlhf-training",
        "peft-fine-tuning", "pytorch-fsdp2", "pytorch-lightning", "ray-train", "simpo-training",
        "slime-rl-training", "torchforge-rl-training", "training-llms-megatron", "unsloth",
        "verl-rl-training",
    },
    "模型结构、压缩与可解释性": {
        "implementing-llms-litgpt", "knowledge-distillation", "long-context", "mamba-architecture",
        "model-merging", "model-pruning", "nanogpt", "nnsight-remote-interpretability",
        "pyvene-interventions", "rwkv-architecture", "sparse-autoencoder-training",
        "transformer-lens-interpretability",
    },
    "推理、量化与部署": {
        "awq-quantization", "gguf-quantization", "gptq", "hqq-quantization", "llama-cpp",
        "optimizing-attention-flash", "quantizing-models-bitsandbytes", "serving-llms-vllm",
        "sglang", "speculative-decoding", "tensorrt-llm",
    },
    "云算力与基础设施": {
        "lambda-labs-gpu-cloud", "modal-serverless-gpu", "skypilot-multi-cloud-orchestration",
    },
    "RAG、Agent与结构化输出": {
        "autogpt-agents", "chroma", "crewai-multi-agent", "dspy", "evolving-ai-agents",
        "faiss", "guidance", "instructor", "langchain", "llamaindex", "outlines", "pinecone",
        "qdrant-vector-search", "sentence-transformers",
    },
    "数据处理与分词": {
        "huggingface-tokenizers", "nemo-curator", "ray-data", "sentencepiece",
    },
    "多模态、机器人与媒体": {
        "audiocraft-audio-generation", "blip-2-vision-language", "clip", "evaluating-cosmos-policy",
        "fine-tuning-openvla-oft", "fine-tuning-serving-openpi", "llava", "segment-anything-model",
        "stable-diffusion-image-generation", "whisper",
    },
    "生物医学与统计": {"biology", "statistics", "veterinary"},
    "专利与职业": {"nature-paper-to-patent", "patent-disclosure-skill", "resume-master"},
    "项目专用": {"vetai-evaluation", "vetai-project-context"},
}

CATEGORY_TAGS = {
    "学术写作与出版": ["论文", "投稿"],
    "文献检索与研究": ["查论文", "研究"],
    "研究记录与知识产物": ["研究记录"],
    "模型评测、安全与可观测": ["评测", "安全"],
    "训练、微调与强化学习": ["训练", "微调"],
    "模型结构、压缩与可解释性": ["模型研究"],
    "推理、量化与部署": ["部署", "推理"],
    "云算力与基础设施": ["算力"],
    "RAG、Agent与结构化输出": ["RAG", "Agent"],
    "数据处理与分词": ["数据"],
    "多模态、机器人与媒体": ["图像", "音视频"],
    "生物医学与统计": ["生命科学"],
    "专利与职业": ["专利", "简历"],
    "项目专用": ["VetAI"],
}

NAME_TO_CATEGORY = {
    name: category for category, names in CATEGORY_MEMBERS.items() for name in names
}


def classify(name: str, description: str) -> tuple[str, list[str]]:
    del description
    category = NAME_TO_CATEGORY.get(name)
    if not category:
        raise ValueError(f"unclassified skill: {name}")
    return category, CATEGORY_TAGS[category]


KNOWN_SOURCES = {
    "academic-paper": "Imbad0202/academic-research-skills",
    "academic-paper-reviewer": "Imbad0202/academic-research-skills",
    "academic-pipeline": "Imbad0202/academic-research-skills",
    "deep-research": "Imbad0202/academic-research-skills",
    "academic-writing-assistant": "社区技能",
    "arxiv-search": "OpenClaw-Medical-Skills",
    "bgpt-paper-search": "OpenClaw-Medical-Skills",
    "biology": "社区技能",
    "citation-management": "社区技能",
    "statistics": "社区技能",
    "veterinary": "社区技能",
    "patent-disclosure-skill": "handsomestWei/patent-disclosure-skill",
    "resume-master": "wangyafu/resume-skills",
}


def source(author: str, name: str) -> str:
    if name in {"vetai-project-context", "vetai-evaluation", "humanize-academic-writing"}:
        return "个人维护"
    if name in KNOWN_SOURCES:
        return KNOWN_SOURCES[name]
    if name.startswith("nature-") or name == "researchwrite":
        return "Yuan1z0825/nature-skills"
    if author == "Orchestra Research":
        return "Orchestra Research 批量收录"
    if author:
        return author
    return "来源未标注"


def collect() -> list[dict[str, object]]:
    rows = []
    for path in sorted(SKILLS.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        skill_file = path / "SKILL.md"
        if not skill_file.exists():
            rows.append({"dir": path.name, "name": path.name, "missing": True})
            continue
        text = skill_file.read_text(encoding="utf-8-sig", errors="replace")
        fm = frontmatter(text)
        name = field(fm, "name") or path.name
        description = field(fm, "description")
        author = field(fm, "author")
        category, tags = classify(path.name, description)
        skill_source = source(author, path.name)
        flags = []
        if skill_source == "来源未标注":
            flags.append("来源未标注")
        if not field(fm, "version"):
            flags.append("版本未标注")
        if len(text) > 50000:
            flags.append("正文很长")
        if (path / ".git").exists():
            flags.append("含嵌套 Git")
        if any(x in text for x in ("C:\\Users\\Administrator", "E:\\", "dataset_reference_set", "score_v1_reference")):
            flags.append("含本机或旧项目引用")
        rows.append({
            "dir": path.name,
            "name": name,
            "description": first_sentence(description or "暂无说明"),
            "author": author,
            "source": skill_source,
            "category": category,
            "tags": tags,
            "chars": len(text),
            "flags": flags,
            "missing": False,
        })
    return rows


def link(row: dict[str, object]) -> str:
    return f"[`{row['name']}`](../skills/{row['dir']}/SKILL.md)"


def write_catalog(rows: list[dict[str, object]]) -> None:
    CATALOG.mkdir(exist_ok=True)
    usable = [r for r in rows if not r.get("missing")]
    categories = defaultdict(list)
    for row in usable:
        categories[str(row["category"])].append(row)
    order = [
        "学术写作与出版", "文献检索与研究", "研究记录与知识产物",
        "模型评测、安全与可观测", "训练、微调与强化学习",
        "模型结构、压缩与可解释性", "推理、量化与部署", "云算力与基础设施",
        "RAG、Agent与结构化输出", "数据处理与分词", "多模态、机器人与媒体",
        "生物医学与统计", "专利与职业", "项目专用",
    ]

    featured = [
        ("deep-research", "做完整调研、事实核查或系统综述"),
        ("nature-reader", "精读一篇论文，保留图表、公式和原文位置"),
        ("nature-writing", "根据研究材料起草或重建论文正文"),
        ("humanize-academic-writing", "清理学术文本里的机械句式和 AI 痕迹"),
        ("citation-management", "管理 BibTeX、补引用、查重复和格式问题"),
        ("academic-paper-reviewer", "投稿前模拟多视角同行评审"),
        ("patent-disclosure-skill", "从项目材料挖专利点并写技术交底书"),
        ("llama-factory", "用 LLaMA-Factory 做 SFT、LoRA、DPO 等训练"),
        ("serving-llms-vllm", "搭建高吞吐 OpenAI 兼容推理服务"),
        ("llama-cpp", "在 CPU、Mac 或消费级显卡上运行 GGUF 模型"),
        ("qdrant-vector-search", "构建带过滤和混合检索的生产级 RAG"),
        ("vetai-project-context", "查看 VetAI 仓库结构、测试命令和工作约定"),
    ]
    by_dir = {str(r["dir"]): r for r in usable}
    readme = """# 技能库入口\n\n这里按“要做什么”找技能。`skills/` 保持原来的平铺路径，现有安装链接不会失效。\n\n## 独立维护的原创技能\n\n[`high-stakes-ai-evaluation`](https://github.com/Charon621/high-stakes-ai-evaluation)：检查医疗、法律、金融等高风险 AI 的效果声明能不能公开，并指出缺失证据。\n\n## 常用精选\n\n| 技能 | 适合做什么 |\n|---|---|\n"""
    for name, note in featured:
        row = by_dir[name]
        readme += f"| {link(row).replace('../skills/', 'skills/')} | {note} |\n"
    readme += "\n## 完整分类\n\n| 分类 | 数量 | 示例 |\n|---|---:|---|\n"
    for category in order:
        items = categories.get(category, [])
        if not items:
            continue
        examples = "、".join(f"`{r['name']}`" for r in items[:5])
        readme += f"| {category} | {len(items)} | {examples} |\n"
    readme += """
完整清单见 [`catalog/技能总索引.md`](catalog/技能总索引.md)，按用户目标重排的入口见 [`catalog/按任务找.md`](catalog/按任务找.md)，来源和维护状态见 [`catalog/来源与待核对.md`](catalog/来源与待核对.md)。\n\n## 安装\n\n单个技能直接安装原始 `SKILL.md`：\n\n```bash\nhermes skills install "https://raw.githubusercontent.com/Charon621/skills/main/skills/<技能名>/SKILL.md" --yes\n```\n\n克隆后，按需把 `skills/<技能名>/` 复制到当前 profile 的 `$HERMES_HOME/skills/`。\n\n## 维护\n\n技能目录保持平铺，分类由 `catalog/` 索引提供。新增或修改技能后运行：\n\n```bash\npython scripts/build_catalog.py\n```\n\n这个仓库同时包含社区技能、个人维护技能和项目专用技能。来源未标注或带项目路径的条目见待核对清单。\n"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    index = "# 技能总索引\n\n共 **%d** 个技能。按主要用途排列；一个技能只放一个主类，避免同一条目在多个目录重复出现。\n\n" % len(usable)
    for category in order:
        items = categories.get(category, [])
        if not items:
            continue
        index += f"## {category}（{len(items)}）\n\n| 技能 | 用途简介 | 来源 | 备注 |\n|---|---|---|---|\n"
        for row in items:
            flags = "、".join(row["flags"]) if row["flags"] else ""
            index += f"| {link(row)} | {row['description'].replace('|', '/')} | {row['source']} | {flags} |\n"
        index += "\n"
    (CATALOG / "技能总索引.md").write_text(index, encoding="utf-8")

    task = "# 按任务找技能\n\n这页只放优先推荐。需要完整清单时看 [`技能总索引.md`](技能总索引.md)。\n\n"
    recommendations = [
        ("我想写论文、改稿、投稿", [
            ("nature-writing", "从材料起草或重建论文正文"),
            ("nature-polishing", "已有稿件的英文润色与重写"),
            ("academic-paper-reviewer", "投稿前模拟审稿"),
            ("nature-response", "写审稿回复和修订说明"),
            ("humanize-academic-writing", "清理明显的 AI 写作痕迹"),
            ("citation-management", "管理 BibTeX、查缺漏引用"),
        ]),
        ("我想查论文、做综述、精读文献", [
            ("nature-academic-search", "多源查文献并核验引用"),
            ("deep-research", "做完整研究或系统综述"),
            ("nature-reader", "精读一篇论文，保留图表和原文锚点"),
            ("nature-paper-card", "把一篇论文整理成深读卡片"),
            ("nature-literature-pipeline", "从检索一路做到交付和归档"),
        ]),
        ("我想训练、微调或做强化学习", [
            ("llama-factory", "用 LLaMA-Factory 做 SFT、LoRA、DPO 等"),
            ("unsloth", "显存有限时加速 LoRA/QLoRA"),
            ("axolotl", "用 YAML 配置训练流程"),
            ("fine-tuning-with-trl", "用 TRL 做 SFT、DPO、PPO、GRPO"),
            ("deepspeed", "大模型分布式训练和 ZeRO"),
            ("pytorch-fsdp2", "用 PyTorch FSDP2 做分片训练"),
        ]),
        ("我想部署模型、量化或提速", [
            ("serving-llms-vllm", "高吞吐 OpenAI 兼容推理服务"),
            ("sglang", "前缀复用、结构化生成和 Agent 推理"),
            ("llama-cpp", "CPU、Apple Silicon 或消费级显卡本地推理"),
            ("gguf-quantization", "制作和选择 GGUF 量化"),
            ("tensorrt-llm", "NVIDIA GPU 上追求极致吞吐"),
        ]),
        ("我想做 RAG、Agent 或结构化输出", [
            ("qdrant-vector-search", "生产级向量检索和过滤"),
            ("faiss", "本地高性能向量索引"),
            ("sentence-transformers", "生成文本或图像嵌入"),
            ("langchain", "构建 Agent、链和 RAG 应用"),
            ("llamaindex", "文档接入、索引和查询"),
            ("instructor", "用 Pydantic 约束模型输出"),
        ]),
        ("我想评测模型、做安全检查或看训练记录", [
            ("evaluating-llms-harness", "跑 MMLU、GSM8K、HumanEval 等通用基准"),
            ("evaluating-code-models", "专门评测代码模型"),
            ("nemo-evaluator-sdk", "跨多种评测框架做大规模评估"),
            ("prompt-guard", "检测提示注入和越狱"),
            ("nemo-guardrails", "给 LLM 应用加输入输出护栏"),
            ("weights-and-biases", "记录实验、扫参和管理模型"),
        ]),
        ("我想处理图像、语音或多模态", [
            ("whisper", "语音转文字和多语言转录"),
            ("stable-diffusion-image-generation", "文生图、图生图和局部重绘"),
            ("segment-anything-model", "按点、框或自动方式分割图像"),
            ("llava", "视觉问答和多模态对话"),
            ("audiocraft-audio-generation", "生成音乐或音效"),
        ]),
        ("我想写专利、简历或处理 VetAI", [
            ("patent-disclosure-skill", "从项目材料挖专利点并写技术交底书"),
            ("resume-master", "新建简历或按岗位要求修改简历"),
            ("vetai-project-context", "查看 VetAI 仓库结构和工作约定"),
            ("vetai-evaluation", "查看旧版 VetAI 评估约定；使用前先看待核对标记"),
        ]),
    ]
    for question, items in recommendations:
        task += f"## {question}\n\n"
        for name, note in items:
            task += f"{link(by_dir[name])}：{note}。\n"
        task += "\n"
    (CATALOG / "按任务找.md").write_text(task, encoding="utf-8")

    sources = Counter(str(r["source"]) for r in usable)
    flagged = [r for r in usable if r["flags"]]
    source_doc = "# 来源与待核对\n\n## 来源分布\n\n"
    for src, count in sources.most_common():
        source_doc += f"| {src} | {count} 个 |\n"
    source_doc += "\n## 待核对条目\n\n这些条目没有自动删除，只是标出来，方便后续逐个处理。\n\n| 技能 | 标记 |\n|---|---|\n"
    for row in flagged:
        source_doc += f"| {link(row)} | {'、'.join(row['flags'])} |\n"
    missing = [r for r in rows if r.get("missing")]
    if missing:
        source_doc += "\n## 缺少 SKILL.md 的目录\n\n"
        source_doc += "\n".join(f"- `{r['dir']}`" for r in missing) + "\n"
    (CATALOG / "来源与待核对.md").write_text(source_doc, encoding="utf-8")


def main() -> None:
    rows = collect()
    write_catalog(rows)
    print(f"catalog built: {len(rows)} skill directories")


if __name__ == "__main__":
    main()
