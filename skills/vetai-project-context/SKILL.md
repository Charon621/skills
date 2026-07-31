---
name: vetai-project-context
description: VetAI 宠物皮肤初筛小程序项目背景、结构、测试命令与工作约定速查。Use when working on the vetai project, 修改 vetai 代码、跑测试、生成文档或交付文件时。
---

# VetAI 项目上下文速查

## 项目是什么

宠物皮肤病 AI 初筛微信小程序。用户上传宠物皮肤照片 + 填写信息 + 圈选患处，系统调用 Qwen 多模态模型（经微信云函数代理）生成初筛报告。

- **仓库**：`C:\Users\Administrator\Desktop\vetai-complete2`（GitHub 私有：`Charon621/vetai-complete2`）
- **形态**：原生微信小程序（无框架）+ 微信云函数后端
- **模型**：`qwen3.7-plus`（完整诊断）/ `qwen3.6-flash`（视觉预检、对话抽取）

## 架构分层

```
页面层    pages/index(拍照初筛) pages/chat(对话问诊) pages/result(完整报告)
          pages/chat/report(简版报告) pages/detail(档案时间线)
          pages/profile(宠物档案) pages/user(我的·数据驾驶舱)
逻辑层    utils/api.js(诊断编排2135行) utils/chatDoctor.js(对话状态机874行)
          utils/kb.js(知识库RAG 2706行, 65张疾病卡) utils/image.js(图片+ROI)
          utils/lesion.js(圈选) utils/storage.js(本机空间隔离) utils/knowledge.js(红线)
服务端    cloudfunctions/diagnose(云函数: 三阶段代理+限流+幂等+payload校验)
质量层    tests/(11个无框架node测试) evaluation/(评估体系) npm test 全绿
```

## 核心诊断链路（v2.0 并行编排）

`diagnose()` 并行发起视觉预检（flash）+ 完整诊断（plus）：
- 预检先回 → 烂图拦截（quality=unclear 或 diagnosabilityScore<40 立即拒答重拍）
- 口腔/黏膜 case → 清空皮肤库归因
- 完整诊断 → `parseModelJson` 5 层容错 → `normalizeDiagnosis`（护栏+置信度校准+清洗）→ 预检特征重算 KB 归因 + 覆盖一致性检查
- 快路径 `VISION_RAG_FAST_PATH` 已启用（BUG-G8）：预检强命中 KB（score≥8+症状≥2+top2 间隔≥3+组合规则/别名/3 非泛词视觉特征）时 ~3-5s 直接出报告，不等 plus；未达标准退回完整诊断

## 常用命令

```bash
cd /c/Users/Administrator/Desktop/vetai-complete2
npm test                      # 全部测试：11个脚本 + KB审计 + 召回探测（纯本地无API Key）
node evaluation/tools/kb_audit.js       # KB 审计（结构+行为探针）
node evaluation/tools/recall_probe.js   # 24条口语主诉召回探测
```

## 代码约定（改动时必须遵守）

- ES5 风格（`var`、无箭头函数、无模板字符串），与全仓库一致
- 中文注释；修复以 `BUG-编号` 标注在注释里
- 不把 API Key 写进前端（`utils/config.js` 的 `QWEN_API_KEY` 保持空）
- 路径引用用 `wx.env.USER_DATA_PATH`，不硬编码绝对路径
- 用户可见文案不得出现"知识库/RAG/提示词"等内部机制词

## 输出约定

- 交付文件（docx/pdf/图片等）一律存到 `E:\.hermes\`（含 `desktop-attachments` 子目录）
- 不放项目仓库，不放 `E:\CodexOutputs`（旧 AGENTS.md 约定已被用户新指示覆盖）
- 回复末尾附上文件所在文件夹路径

## 已知注意点

- **代码包大小**：evaluation/（含 8.5M 数据集图片）必须保持在 project.config.json 的 packOptions.ignore 里，否则主包 10MB 超 2048KB 限制无法上传（2026-07-31 已配置 evaluation/tests/tools/docs/node_modules/*.md/*.py 忽略，主包 ~632KB）。新增大型目录后先查打包大小
- 云函数修改后需在微信开发者工具手动"上传并部署"，Git 推送不会自动同步
- 未提交状态常见：改动前先 `git status` 确认
- 测试是纯 node assert 脚本（无 jest/mocha），直接 `node tests/xxx.test.js` 单跑也行
- 对话状态机 BUG-C7（2026-07-31 修）：名字缺失时 getReaskQuickReplies 必须返回 []（不得给性别/类型选项误导）；fallbackExtractInfo 排除单字性别词与症状句当名字；「跳过」→ 名字占位「宝贝」/主诉中立占位；PHOTO 阶段补充描述合并进 complaint；initSession 恢复草稿时用 createEmptyDraft 补齐缺失字段（防旧草稿 TypeError 卡死 _isProcessing）
- 本机空间资料 BUG-C9（2026-07-31 修）：storage.updateUser() 改昵称/头像（id 不变、knownUsers 同步、访客返回 null）；「我的」页头像点按换头像（prepareImages 落盘本地文件）、昵称旁「改名」按钮（重名检查排除自身）。空间入口在「我的→开发者选项→切换/新建本机空间」
- 单条记录删除 BUG-C8（2026-07-31 修）：档案时间线每条记录右侧 × 按钮 → storage.deleteRecord(id)；此前只有清空全部
- 对话链路对 AI 可用性敏感：AI 掉线时 GREETING 完整介绍句（无"叫"字）提取不到名字，用户需再答一次名字或用「跳过」
