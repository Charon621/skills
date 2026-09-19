#!/usr/bin/env python3
"""Build searchable catalog pages for the category-organized skills collection."""

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


CATEGORY_ORDER = [
    "nature-suite", "paper-writing", "research-workflow",
    "fine-tuning", "rl-training", "training-infra",
    "quantization-compression", "inference-serving", "model-architecture",
    "rag-vector", "agent-frameworks", "multimodal-media", "robotics",
    "interpretability", "evaluation-benchmarks", "safety-guardrails",
    "observability-tracking", "data-engineering", "gpu-cloud",
    "domain-science", "productivity", "project-vetai",
]

CATEGORY_LABELS = {
    "nature-suite": "Nature 论文套件",
    "paper-writing": "论文写作与投稿",
    "research-workflow": "文献检索与研究流程",
    "fine-tuning": "微调与对齐训练",
    "rl-training": "强化学习训练",
    "training-infra": "分布式训练基础设施",
    "quantization-compression": "量化、压缩与合并",
    "inference-serving": "推理部署与加速",
    "model-architecture": "模型架构与分词",
    "rag-vector": "RAG 与向量检索",
    "agent-frameworks": "Agent 框架与结构化输出",
    "multimodal-media": "多模态与媒体生成",
    "robotics": "机器人与具身策略",
    "interpretability": "可解释性研究",
    "evaluation-benchmarks": "模型评测",
    "safety-guardrails": "安全与护栏",
    "observability-tracking": "实验跟踪与可观测",
    "data-engineering": "数据处理与清洗",
    "gpu-cloud": "云算力平台",
    "domain-science": "学科知识",
    "productivity": "职业与效率",
    "project-vetai": "项目专用（VetAI）",
}

CATEGORY_TAGS = {
    "nature-suite": ["论文", "Nature"],
    "paper-writing": ["论文", "投稿"],
    "research-workflow": ["查论文", "研究"],
    "fine-tuning": ["微调"],
    "rl-training": ["强化学习"],
    "training-infra": ["训练", "分布式"],
    "quantization-compression": ["量化", "压缩"],
    "inference-serving": ["部署", "推理"],
    "model-architecture": ["模型研究"],
    "rag-vector": ["RAG", "向量检索"],
    "agent-frameworks": ["Agent", "结构化输出"],
    "multimodal-media": ["图像", "音视频"],
    "robotics": ["机器人"],
    "interpretability": ["可解释性"],
    "evaluation-benchmarks": ["评测"],
    "safety-guardrails": ["安全"],
    "observability-tracking": ["实验记录"],
    "data-engineering": ["数据"],
    "gpu-cloud": ["算力"],
    "domain-science": ["生命科学"],
    "productivity": ["简历"],
    "project-vetai": ["VetAI"],
}


def classify(name: str, description: str, category_dir: str) -> tuple[str, list[str]]:
    del description, name
    label = CATEGORY_LABELS.get(category_dir)
    if not label:
        raise ValueError(f"unclassified category dir: {category_dir}")
    return label, CATEGORY_TAGS[category_dir]


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
    if name in {"vetai-project-context", "vetai-evaluation", "humanize-academic-writing",
                "cn-academic-paper-standards"}:
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


def read_skill(path: Path, category_dir: str) -> dict[str, object]:
    skill_file = path / "SKILL.md"
    if not skill_file.exists():
        return {"dir": path.name, "name": path.name, "category_dir": category_dir, "missing": True}
    text = skill_file.read_text(encoding="utf-8-sig", errors="replace")
    fm = frontmatter(text)
    name = field(fm, "name") or path.name
    description = field(fm, "description")
    author = field(fm, "author")
    category, tags = classify(path.name, description, category_dir)
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
    return {
        "dir": path.name,
        "category_dir": category_dir,
        "name": name,
        "description": first_sentence(description or "暂无说明"),
        "author": author,
        "source": skill_source,
        "category": category,
        "tags": tags,
        "chars": len(text),
        "flags": flags,
        "missing": False,
    }


def collect() -> list[dict[str, object]]:
    rows = []
    for category_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if (category_dir / "SKILL.md").exists():
            rows.append(read_skill(category_dir, category_dir.name))
            continue
        for path in sorted(category_dir.iterdir()):
            if path.is_dir() and not path.name.startswith("."):
                rows.append(read_skill(path, category_dir.name))
    return rows


def link(row: dict[str, object]) -> str:
    return f"[`{row['name']}`](../skills/{row['category_dir']}/{row['dir']}/SKILL.md)"


def write_catalog(rows: list[dict[str, object]]) -> None:
    CATALOG.mkdir(exist_ok=True)
    usable = [r for r in rows if not r.get("missing")]
    categories = defaultdict(list)
    for row in usable:
        categories[str(row["category"])].append(row)
    order = [CATEGORY_LABELS[category_dir] for category_dir in CATEGORY_ORDER]

    featured = [
        ("deep-research", "做完整调研、事实核查或系统综述"),
        ("nature-reader", "精读一篇论文，保留图表、公式和原文位置"),
        ("nature-writing", "根据研究材料起草或重建论文正文"),
        ("humanize-academic-writing", "清理学术文本里的机械句式和 AI 痕迹"),
        ("cn-academic-paper-standards", "按国标写中文论文、排三线表和参考文献"),
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
    readme = """# 技能库入口\n\n这里按“要做什么”找技能。技能按分类存放在 `skills/<分类>/<技能名>/`，分类目录与 [`catalog/`](catalog/技能总索引.md) 一一对应。\n\n## 独立维护的原创技能\n\n[`high-stakes-ai-evaluation`](https://github.com/Charon621/high-stakes-ai-evaluation)：检查医疗、法律、金融等高风险 AI 的效果声明能不能公开，并指出缺失证据。\n\n## 常用精选\n\n| 技能 | 适合做什么 |\n|---|---|\n"""
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
完整清单见 [`catalog/技能总索引.md`](catalog/技能总索引.md)，按用户目标重排的入口见 [`catalog/按任务找.md`](catalog/按任务找.md)，来源和维护状态见 [`catalog/来源与待核对.md`](catalog/来源与待核对.md)。\n\n## 安装\n\n单个技能直接安装原始 `SKILL.md`（注意 URL 带分类目录）：\n\n```bash\nhermes skills install "https://raw.githubusercontent.com/Charon621/skills/main/skills/<分类>/<技能名>/SKILL.md" --yes\n```\n\n克隆后，按需把 `skills/<分类>/<技能名>/` 复制到当前 profile 的 `$HERMES_HOME/skills/`。\n\n## 维护\n\n技能按分类目录存放（22 个分类，清单与中文名见 `scripts/build_catalog.py` 的 `CATEGORY_ORDER` / `CATEGORY_LABELS`）。新增技能放进对应分类目录后运行：\n\n```bash\npython scripts/build_catalog.py\nnode skill-index.mjs scan . --rules ml-skills-rules.json\n```\n\n`skill-index.mjs` 额外生成机器可读的 `skills.json` 与 `INDEX.md`，并支持关键词检索：`node skill-index.mjs search . <关键词> --rules ml-skills-rules.json`。\n\n这个仓库同时包含社区技能、个人维护技能和项目专用技能。来源未标注或带项目路径的条目见待核对清单。\n"""
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
            ("academic-paper-workflow", "端到端学术论文准备与撰写全流程工作流（带双门禁）"),
            ("nature-writing", "从材料起草或重建论文正文"),
            ("nature-polishing", "已有稿件的英文润色与重写"),
            ("academic-paper-reviewer", "投稿前模拟审稿"),
            ("nature-response", "写审稿回复和修订说明"),
            ("humanize-academic-writing", "清理明显的 AI 写作痕迹"),
            ("cn-academic-paper-standards", "按国标（GB/T 7713.2、GB/T 7714）写中文论文并排版"),
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
