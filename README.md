# Charon621 Skills

个人 AI 技能仓库（Hermes Agent / Claude 等支持 SKILL.md 规范的 agent 通用）。

每个子目录是一个独立技能，包含 `SKILL.md`（必填）及可选的 `scripts/`、`references/`、`templates/`。

## 技能列表

### 📝 学术写作与去 AI

| 技能 | 说明 | 来源 |
|------|------|------|
| `humanize-academic-writing` | 学术文本去 AI 痕迹，改写为自然的人类学术表达（含 AI 特征检测脚本） | 自装 |
| `research-paper-writing` | 论文写作辅助 | 预装 |
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
