---
name: paper-visual-report
description: Research a technical topic through primary papers and produce an illustrated, source-linked report with paper figures, complete title-and-abstract captures, and a self-contained offline HTML deliverable. Use for research explainers, technology histories, and paper comparisons; respect an explicitly requested presentation or document format.
---

# 论文图文报告

把论文证据组织成可阅读、可核查的图文叙事。默认使用用户的语言。适合“解释一条技术路线如何演化”“比较几种方法”“带论文原图与摘要的专题”。

## 决定表达方式

- 用户已指定格式就遵从。长篇解释、原图放大、完整摘要和引用追溯适合 HTML；面向现场讲述、页数或时长明确时适合演示文稿。不要把 HTML 改个扩展名当 PPT。
- 根据已有上下文确定读者、叙事主线、时间范围和交付范围；只询问影响结果且无法推断的信息。把“今年”“最新”转换为有日期的研究截止点。
- 自动选择 HTML 时说明原因即可，继续完成工作。这个 skill 不自行授权发布网站、推送仓库或向他人发消息。

## 先建证据，再写叙事

阅读 [研究与素材规范](references/research-and-evidence.md)。在线检索论文、作者项目页和官方技术资料；搜索结果用于发现，原文用于论证。建立本地证据记录，保存关键断言对应的页码、图号、版本、实验条件与来源。

每个主要阶段回答：此前什么做不到 → 方法改变了什么 → 数据、训练和推理怎样工作 → 实验证明到哪里 → 下一阶段解决什么。时间顺序不能代替因果关系；并行路线、早期先例和概念相似性要明确。把作者结论与报告自己的解释区分开。

## 图片与论文卡片

- 优先使用论文原图或作者项目图。原创机制图要标“示意”，生成图不能充当实验证据。每张图承担一个解释任务，配图源、作者、图号及裁切说明。
- 用户要求完整标题和摘要时，对每篇核心论文制作完整可读截图；标题和摘要跨栏或跨页时可拼接，标注来源区域，不删减摘要。不用改写文字冒充原文截图。
- 先核查适用的引用、转载或开放许可依据；开放获取不自动代表自由转载。不要默认 CC BY，也不要把元数据许可扩展到正文排版、图片或全文。依据不足时采用合规的短引、自己的摘要和原文链接，明确说明交付差异。
- 可用 `scripts/capture_regions.py` 将 PDF 中人工确认的区域拼接成图片。它只裁切，不自动判断摘要是否完整；始终目视核对开头、结尾、公式与跨页续文。

## 制作 HTML

阅读 [HTML 制作与验收](references/html-delivery.md)。可复制 `assets/starter/` 到独立工作目录，然后运行：

```sh
python3 <skill目录>/scripts/build_report.py <报告工作目录>
```

修改 `source/article.template.html` 的叙事、`source/style.css` 的视觉样式、`figures.json` 的插图和 `papers.json` 的论文卡片。构建器输出 `dist/index.html`，将本地图片、样式、交互内嵌，保留原文外链。模板只是起点，按主题调整，不强制沿用配色、篇幅或章节数量。

构建器负责机械检查；事实与图文语义必须由作者核查。不要以构建成功替代浏览器验收。

## 验收与交付

1. 核对关键日期、指标口径、训练/推理区别、实验条件及图片对应关系。
2. 检查所有核心论文标题与完整摘要截图；放大后应能读清。
3. 在可用的浏览器预览工具中检查桌面和手机布局、长标题、图片加载、目录、放大与键盘关闭。遵守工具的 URL 访问限制；受限时说明未完成的检查，不换手段绕过。
4. 检查最终文件没有未替换标记、外部样式/脚本依赖、坏锚点或缺图。交付目录只放成品；模板放 `source/` 且使用 `.template.html`，避免用户误开纯文字模板。
5. 最终给出明确的成品链接、内容范围与实际存在的限制。发布、上传或安装只在当前用户请求范围内执行。

相关脚本只处理本地素材，不负责联网检索、自动授权转载或自动发布。
