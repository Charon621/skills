#!/usr/bin/env node
// skill-index — 为散乱的 skills 仓库生成索引、支持关键词检索、并检查常见配置问题
//
// 用法:
//   node skill-index.mjs scan <repo-root> [--out <dir>]   生成 INDEX.md + skills.json（默认写在 repo-root）
//   node skill-index.mjs search <repo-root> <关键词>...    按关键词检索，支持多个词（AND 优先）
//   node skill-index.mjs check <repo-root>                只输出问题清单
//
// 索引分组规则：优先用目录结构（相对路径中第一个非通用、非版本号的段落）；
// 若仓库是平铺的（每个 skill 直接放在一级目录下），则退化为按主题标签分组，并在条目后标注 ✱。
import { promises as fs } from 'node:fs';
import path from 'node:path';

const ANSI = process.stdout.isTTY && !process.env.NO_COLOR;
const bold = s => (ANSI ? `\x1b[1m${s}\x1b[0m` : s);
const dim = s => (ANSI ? `\x1b[2m${s}\x1b[0m` : s);
const red = s => (ANSI ? `\x1b[31m${s}\x1b[0m` : s);
const yellow = s => (ANSI ? `\x1b[33m${s}\x1b[0m` : s);

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--out') args.out = argv[++i] ?? null;
    else if (argv[i] === '--rules') args.rules = argv[++i] ?? null;
    else if (argv[i] === '--labels') args.labels = argv[++i] ?? null;
    else args._.push(argv[i]);
  }
  return args;
}

function parseFrontmatter(text) {
  const lines = text.replace(/^\uFEFF/, '').split(/\r?\n/);
  if ((lines[0] ?? '').trim() !== '---') return {};
  const data = {};
  let i = 1;
  while (i < lines.length && lines[i].trim() !== '---') {
    const m = lines[i].match(/^([A-Za-z0-9_-]+)\s*:(.*)$/);
    if (!m) { i++; continue; }
    const key = m[1].toLowerCase();
    let val = m[2].trim();
    if (val === '>' || val === '|' || val === '') {
      const folded = val !== '|';
      const block = [];
      i++;
      while (i < lines.length && lines[i].trim() !== '---' &&
             (/^\s/.test(lines[i]) || lines[i].trim() === '')) {
        if (lines[i].trim()) block.push(lines[i].trim());
        i++;
      }
      val = block.join(folded ? ' ' : '\n');
    } else {
      i++;
    }
    data[key] = val.replace(/^["']|["']$/g, '');
  }
  return data;
}

const SKIP_DIRS = new Set(['.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build']);

async function collectSkills(root) {
  const absRoot = path.resolve(root);
  const files = [];
  async function walk(dir) {
    let entries;
    try { entries = await fs.readdir(dir, { withFileTypes: true }); }
    catch { return; }
    for (const e of entries) {
      if (!e.isDirectory()) {
        if (e.name.toLowerCase() === 'skill.md') files.push(path.join(dir, e.name));
        continue;
      }
      if (e.name.startsWith('.') || SKIP_DIRS.has(e.name)) continue;
      await walk(path.join(dir, e.name));
    }
  }
  await walk(absRoot);

  const skills = [];
  for (const file of files) {
    let text = '';
    try { text = await fs.readFile(file, 'utf8'); } catch { continue; }
    const fm = parseFrontmatter(text);
    const dir = path.dirname(file);
    skills.push({
      name: fm.name || path.basename(dir),
      description: fm.description || '',
      path: path.relative(absRoot, file).split(path.sep).join('/'),
      segments: path.relative(absRoot, dir).split(path.sep).filter(Boolean),
      dirName: path.basename(dir),
    });
  }
  skills.sort((a, b) => a.path.localeCompare(b.path));
  return { absRoot, skills };
}

const GENERIC_DIRS = new Set(['skills', 'skill', 'commands', 'agents', 'src', 'docs', 'examples', 'scripts']);
const isVersionLike = s => /^(v)?\d+([.-]\d+)*$/.test(s);

function commonPrefix(segsList) {
  if (!segsList.length) return [];
  if (segsList.length === 1) return segsList[0].slice(0, -1);
  let prefix = [...segsList[0]];
  for (const segs of segsList) {
    const n = Math.min(prefix.length, segs.length);
    let i = 0;
    while (i < n && prefix[i] === segs[i]) i++;
    prefix = prefix.slice(0, i);
    if (!prefix.length) break;
  }
  return prefix;
}

const TAG_RULES = [
  ['document', /pdf|docx|xlsx|pptx|excel|word|powerpoint|spreadsheet|幻灯|文档|表格|报告|简历/i],
  ['browser', /browser|web.?gui|网页|浏览器|截图|frontend|playwright|puppeteer/i],
  ['dev-workflow', /\bgit\b|commit|refactor|debug|unit.?test|lint|代码|调试|重构/i],
  ['writing', /writ|blog|article|写作|文案|翻译|总结|摘要/i],
  ['data', /\bcsv\b|\bdata\b|chart|plot|数据|图表|分析|可视化/i],
  ['automation', /automat|workflow|schedule|batch|cron|自动化|定时|批量/i],
  ['ai', /\bllm\b|prompt|\bagent|大模型|提示词|模型/i],
];

function suggestTags(s) {
  const hay = `${s.name} ${s.description} ${s.path}`;
  const tags = TAG_RULES.filter(([, re]) => re.test(hay)).map(([t]) => t);
  return tags.length ? tags : ['other'];
}

async function loadRules(file) {
  if (!file) return null;
  const rules = JSON.parse(await fs.readFile(file, 'utf8'));
  if (!Array.isArray(rules) || !rules.every(r => r.category && r.match)) {
    throw new Error('规则文件须为 [{"category": "...", "match": "regex", "field"?: "name"}] 数组');
  }
  return rules.map(r => ({
    category: r.category,
    re: new RegExp(r.match, 'i'),
    field: r.field === 'name' ? 'name' : 'all',
  }));
}

async function loadLabels(file) {
  if (!file) return null;
  const labels = JSON.parse(await fs.readFile(file, 'utf8'));
  if (typeof labels !== 'object' || labels === null || Array.isArray(labels)) {
    throw new Error('简介文件须为 { "技能名": "中文简介" } 对象');
  }
  return labels;
}

function enrich(skills, rules = null, labels = null) {
  const prefix = commonPrefix(skills.map(s => s.segments));
  for (const s of skills) {
    const rest = s.segments.slice(prefix.length);
    s.category = rest.slice(0, -1)
      .find(seg => !GENERIC_DIRS.has(seg.toLowerCase()) && !isVersionLike(seg)) ?? null;
    s.tags = suggestTags(s);
  }
  if (rules) {
    for (const s of skills) {
      const hay = `${s.name} ${s.dirName}`.toLowerCase();
      const hit = rules.find(r => r.re.test(r.field === 'name' ? hay : `${hay} ${s.description.toLowerCase()} ${s.path.toLowerCase()}`));
      s.category = hit ? hit.category : null;
      s.tags = [hit ? hit.category : 'unmatched', ...s.tags.filter(t => t !== (hit?.category))];
    }
  }
  if (labels) {
    for (const s of skills) {
      s.zh = labels[s.name] ?? labels[s.dirName] ?? null;
    }
  }
}

function findIssues(skills) {
  const issues = [];
  const byName = new Map();
  for (const s of skills) {
    if (!s.description) {
      issues.push(['warn', s.path, 'frontmatter 缺少 description，自动触发会不稳定']);
    } else if (s.description.length > 1024) {
      issues.push(['warn', s.path, `description 过长（${s.description.length} 字符，建议 ≤1024）`]);
    }
    if (s.name !== s.dirName) {
      issues.push(['info', s.path, `name「${s.name}」与目录名「${s.dirName}」不一致`]);
    }
    const k = s.name.toLowerCase();
    byName.set(k, [...(byName.get(k) ?? []), s]);
  }
  for (const [k, list] of byName) {
    if (list.length > 1) {
      issues.push(['warn', list.map(s => s.path).join(' | '), `重名 skill「${k}」共 ${list.length} 个`]);
    }
  }
  return issues;
}

const cell = (s, max = 160) => {
  const oneLine = String(s).replace(/\s+/g, ' ').trim();
  return oneLine.length > max ? oneLine.slice(0, max - 1) + '…' : oneLine;
};

function buildIndexMd(root, skills, issues, rulesApplied = false, scanCmd = `node skill-index.mjs scan ${root}`) {
  const fallbackKey = rulesApplied ? 'other ⚠（未匹配任何规则）' : 'other ✱';
  const groups = new Map();
  for (const s of skills) {
    const key = s.category ?? fallbackKey;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(s);
  }
  const keys = [...groups.keys()].sort((a, b) => a.localeCompare(b));

  const lines = [
    `# Skills Index`,
    '',
    `> 由 skill-index.mjs 自动生成于 ${new Date().toISOString().slice(0, 10)}，请勿手改；重跑 \`${scanCmd}\` 更新。`,
    '',
    `共 **${skills.length}** 个 skills，**${keys.length}** 个分组，检出 **${issues.length}** 个问题。`,
    '',
  ];

  if (rulesApplied) {
    lines.push(`> 分组来自自定义规则文件，按 first-match 顺序匹配 name/description。`, '');
  } else if (skills.every(s => !s.category)) {
    lines.push(`> 仓库为平铺结构，以下按主题标签 ✱ 建议分组；如需按此重排目录，可作为迁移方案。`, '');
  }

  for (const key of keys) {
    lines.push(`## ${key} (${groups.get(key).length})`, '');
    lines.push('| Skill | 说明 | 路径 |', '| --- | --- | --- |');
    for (const s of groups.get(key)) {
      const desc = cell(s.zh || s.description || '（无 description）', 140).replace(/\|/g, '\\|');
      lines.push(`| ${s.name} | ${desc} | \`${s.path}\` |`);
    }
    lines.push('');
  }

  if (issues.length) {
    lines.push(`## 检出的问题 (${issues.length})`, '');
    for (const [level, where, what] of issues) {
      lines.push(`- **${level.toUpperCase()}** \`${where}\` — ${what}`);
    }
    lines.push('');
  }
  return lines.join('\n');
}

async function load(root, rulesFile = null, labelsFile = null) {
  const { absRoot, skills } = await collectSkills(root);
  enrich(skills, await loadRules(rulesFile), await loadLabels(labelsFile));
  return { absRoot, skills };
}

async function cmdScan(root, out, rulesFile, labelsFile) {
  const { absRoot, skills } = await load(root, rulesFile, labelsFile);
  if (!skills.length) {
    console.log(red(`在 ${absRoot} 下没有找到任何 SKILL.md`));
    process.exitCode = 1;
    return;
  }
  const issues = findIssues(skills);
  const outDir = path.resolve(out ?? absRoot);
  const rulesApplied = !!rulesFile;
  const flags = [
    rulesFile ? `--rules ${rulesFile}` : null,
    labelsFile ? `--labels ${labelsFile}` : null,
  ].filter(Boolean).join(' ');
  const scanCmd = `node skill-index.mjs scan ${root}${flags ? ' ' + flags : ''}`;
  await fs.mkdir(outDir, { recursive: true });
  await fs.writeFile(path.join(outDir, 'INDEX.md'), buildIndexMd(root, skills, issues, rulesApplied, scanCmd), 'utf8');
  await fs.writeFile(
    path.join(outDir, 'skills.json'),
    JSON.stringify({
      generatedAt: new Date().toISOString(),
      root: absRoot,
      count: skills.length,
      skills: skills.map(({ segments, ...s }) => s),
    }, null, 2),
    'utf8',
  );

  const cats = new Set(skills.map(s => s.category ?? 'other'));
  console.log(`共 ${bold(skills.length)} 个 skills，${bold(cats.size)} 个分组 →`);
  for (const c of [...cats].sort()) {
    console.log(`  ${dim('•')} ${c} (${skills.filter(s => (s.category ?? 'other') === c).length})`);
  }
  console.log(`\n已生成 ${bold(path.join(outDir, 'INDEX.md'))} 和 ${bold(path.join(outDir, 'skills.json'))}`);
  if (issues.length) {
    console.log(`\n检出 ${yellow(issues.length)} 个问题（详见 INDEX.md 末尾）：`);
    for (const [level, where, what] of issues.slice(0, 10)) {
      console.log(`  ${level === 'warn' ? yellow('WARN') : dim('INFO')} ${where} — ${what}`);
    }
    if (issues.length > 10) console.log(dim(`  … 其余 ${issues.length - 10} 个见 INDEX.md`));
  }
}

async function cmdSearch(root, query, rulesFile, labelsFile) {
  if (!query.length) {
    console.log(red('用法: node skill-index.mjs search <repo-root> <关键词>...'));
    process.exitCode = 1;
    return;
  }
  const { skills } = await load(root, rulesFile, labelsFile);
  const tokens = query.map(t => t.toLowerCase());
  const scored = [];
  for (const s of skills) {
    const hay = {
      name: s.name.toLowerCase(),
      dir: s.dirName.toLowerCase(),
      tags: s.tags.join(' ').toLowerCase(),
      desc: `${s.description} ${s.zh ?? ''}`.toLowerCase(),
      path: s.path.toLowerCase(),
    };
    let score = 0, matchedAll = true;
    for (const t of tokens) {
      let sc = 0;
      if (hay.name.includes(t)) sc += 10;
      if (hay.dir.includes(t)) sc += 6;
      if (hay.tags.includes(t)) sc += 5;
      if (hay.desc.includes(t)) sc += 2;
      if (hay.path.includes(t)) sc += 1;
      if (!sc) matchedAll = false;
      score += sc;
    }
    if (score > 0) scored.push({ s, score, matchedAll });
  }
  scored.sort((a, b) => (b.matchedAll - a.matchedAll) || (b.score - a.score));

  if (!scored.length) {
    console.log(dim(`没有匹配「${query.join(' ')}」的 skill`));
    return;
  }
  console.log(dim(`匹配 ${scored.length} 个（显示前 20，全词命中优先）：`));
  for (const { s } of scored.slice(0, 20)) {
    console.log(`${bold(s.name)}  ${dim(s.path)}  [${s.tags.join(', ')}]`);
    const desc = s.zh || s.description;
    if (desc) console.log(`  ${cell(desc, 150)}`);
  }
}

async function cmdCheck(root) {
  const { absRoot, skills } = await load(root);
  const issues = findIssues(skills);
  console.log(`${absRoot}：${skills.length} 个 skills，${issues.length} 个问题`);
  for (const [level, where, what] of issues) {
    console.log(`  ${level === 'warn' ? yellow('WARN') : dim('INFO')} ${where} — ${what}`);
  }
  if (!issues.length) console.log(bold('未发现问题 ✓'));
}

const args = parseArgs(process.argv.slice(2));
const [cmd, root, ...rest] = args._;
if (!cmd || !root) {
  console.log(`用法:
  node skill-index.mjs scan <repo-root> [--out <dir>] [--rules <rules.json>] [--labels <zh.json>]   生成 INDEX.md + skills.json
  node skill-index.mjs search <repo-root> <关键词>... [--rules <rules.json>] [--labels <zh.json>]    按关键词检索
  node skill-index.mjs check <repo-root>                检查常见问题`);
  process.exitCode = cmd ? 1 : 0;
} else if (cmd === 'scan') {
  await cmdScan(root, args.out, args.rules, args.labels);
} else if (cmd === 'search') {
  await cmdSearch(root, rest, args.rules, args.labels);
} else if (cmd === 'check') {
  await cmdCheck(root);
} else {
  console.log(red(`未知命令「${cmd}」，可用：scan / search / check`));
  process.exitCode = 1;
}
