# Charon621 Skills

个人 AI 技能仓库（Hermes Agent / Claude 等支持 SKILL.md 规范的 agent 通用）。

每个子目录是一个独立技能，包含 `SKILL.md`（必填）及可选的 `scripts/`、`references/`、`templates/`。

## 技能列表

| 技能 | 类别 | 说明 |
|------|------|------|
| `humanize-academic-writing` | 学术写作 | 学术文本去 AI 痕迹，改写为自然的人类学术表达（含 AI 特征检测脚本） |
| `vetai-project-context` | 项目 | VetAI 宠物皮肤初筛小程序的项目背景、结构、测试与约定速查 |
| `vetai-evaluation` | 项目 | VetAI 评估体系（gold_standard / V1 参考集 / 探针工具链）使用方法与边界 |

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
- 仓库内不存放任何 API Key 或敏感信息
