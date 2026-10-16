# HTML 制作与验收

## 目录与构建

```text
report-work/
  source/article.template.html
  source/style.css
  source/app.js
  assets/
  figures.json
  papers.json
  dist/index.html                 ← 用户应打开的成品
```

把 starter 复制到独立工作目录再修改。不要修改 skill 自带模板来存放某次报告。构建器只写 `dist/index.html`，不用网络或 CDN，Python 标准库即可构建。PDF 裁切工具另需 Pillow 和 `pdftoppm`。在 Codex 桌面端可以查询 workspace dependencies 获取可用运行时；其他环境使用已有 Python。

模板标记：`/*INLINE_CSS*/`、`/*INLINE_JS*/`、`<!--PAPER_CARDS-->`；插图用 `<figure data-figure="某个id"></figure>`。每个插图 ID 只用一次。目录链接必须对应存在的章节 ID。

`figures.json` 是以 ID 为键的对象，各项字段：

- `file`：相对 `assets/` 的本地图片路径，支持 PNG/JPEG/WebP/GIF/SVG。
- `title`、`alt`、`desc`：纯文本标题、替代文本及解释。
- `credit`、`url`：作者/图号/裁切说明及实际图源 HTTP(S) URL。
- `rights`：明确的来源许可或其他适用依据；自制图写“原创示意”。
- `width`、`height`：图片实际像素尺寸；SVG 可用 viewBox 比例尺寸。

`papers.json` 是数组，各项字段：`id, title, authors, date, summary, file, width, height, url, pdf, crop, rights`。`file` 为完整标题/摘要截图；`date` 用文字区分首次预印本和发表日期；`url` 和 `pdf` 是 HTTP(S) 来源。文本字段被转义；需要富文本叙事时在模板中编辑。

构建检查包括路径越界、缺图、未使用/重复插图、未替换标记、重复 ID、坏锚点、图片 alt 与尺寸，以及外部脚本/样式/媒体。正文模板是可信的作者输入，不是第三方 HTML 的清洗器。SVG 应为已审阅的静态素材，不能引用外部资源、包含脚本或事件处理器。不要直接复制网页上的可执行代码。

## 视觉与交互

- 使用清晰的封面观点、章节层次、留白和统一图注；一屏一个主要阅读焦点。
- 正文图显示全貌，原论文中的小字在弹窗中可放大阅读。保留原始比例，不用裁切式封面样式展示实验图。
- 设置图片的真实宽高，并用 CSS `height:auto` 保持比例，避免懒加载导致目录跳动。
- 完整摘要卡片可用受控高度预览，但弹窗必须展示完整图像。打印时取消摘要图高度截断。
- 交互要帮助解释真实差异：路线切换、训练/推理步骤、统一维度比较。避免只为装饰增加交互。
- 不依赖字体 CDN、远程 CSS、模块导入、运行时 fetch 或远程图片；外部论文链接保留联网访问。

## 浏览器验收

实际打开 `dist/index.html` 或通过获准的本地 HTTP 预览加载该文件。检查桌面约 1280px、手机约 390px，及足够长的英文论文标题：

1. 图片加载、全页无意外横向溢出；表格可在自己的容器内横向滚动。
2. 正文、摘要弹窗的文字可读，图片不变形；弹窗能滚动看完全文。
3. 目录、关闭按钮、Escape、焦点返回和任何交互都有效。
4. 浏览器控制台无阻止功能的错误；抽查来源链接。
5. 完成最终修改后再检查受影响的布局与交互；保存真实预览图用于交付。

若浏览器工具拒绝 file URL，不能通过另一工具绕过限制。可使用工具允许的本地 HTTP 预览验证文件内容，但不能宣称已检查用户受限的现有标签页。无法完成的部分如实说明。

不要把源码模板作为打开入口。用户说“只有纯文字”时，先核对打开的是成品还是模板，再排查样式占位符、文件下载是否完整和资源路径，不先归咎于浏览器。
