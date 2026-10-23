# belgic-confession-20261023-v2-GROKstudy

**《比利时信条》（Belgic Confession, 1561）· 欧陆改革宗深读**：这是一个简体中文多页学习站，页脚版本号为 `v20261023-2`（v2.0.0）。

站点从整本圣经与圣约的大图景讲起，然后讲历史、地理与文化，再把 37 条逐条展开。每一条都从六个方面来读：为什么写、说了什么、圣经与圣约、对手与联系、重点与难点、怎样应用。之后是专题深析，以及三项联合信条的比较（为什么是三份而不是一份）和威斯敏斯特标准对照。站内还有 BC / HC / Dort 的原文背诵版、三大信经和记忆自测。

> **引文规则**：全站信条原文和中文引号内的引文，都逐字取自 [CCI《赞美手册》中文版](https://ccifellowship.org/books/book-of-praise)。构建时由程序做子串核对（`core.Q`、`tools/verify_exact.py`），核对不过就不能构建。CCI 没有的内容，用用户提供的《中国改革宗教会敬拜手册》2015 版逐字摘引，并标明页码。

## 在线地址（当前 v2.0.0）

| 部署 | 地址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/ |
| Surge | https://belgic-confession-20261023-v2-grokstudy.surge.sh/ |
| Netlify | https://belgic-confession-20261023-v2-grokstudy.netlify.app/ |
| 代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy |

v1.0.0 仍保留为还原点：标签 [`v1.0.0`](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v1.0.0)，以及 https://belgic-confession-20261023-v1-grokstudy.surge.sh/ 与 https://belgic-confession-20261023-v1-grokstudy.netlify.app/ 。

命名规则：仓库名只用主题（`Belgic-Confession-GROKstudy`）；Surge / Netlify 的域名用“主题-日期-版本-grokstudy”，因为域名只能小写。

## 页面结构（12 部分）

| # | 页面 | 内容 |
|---|---|---|
| 首页 | `index.html` | 十二站学习路径、阅读进度、可视化入口 |
| 一 | `bible.html` | 全本圣经与圣约：四幕剧、九个约（流程图）、八条圣经神学主线、五个唯独、37 条的内在逻辑 |
| 二 | `hist.html` | 图尔奈城墙（动画）、德布利故事线、时间线（1517–今）、Leaflet 交互地图与 SVG 版图、低地国家文化、五重处境、文本流变、人物、狱中书信 |
| 三 | `bc.html` | 37 条地图与七群；每条六个方面 + CCI 原文全文（可朗读） |
| 四 | `topics.html` | 三条战线（罗马、重洗派、路德宗与古代异端）、BC 与《法国信条》比较、八个难点（含 PDF 批注问题）、安慰线、误解、教会使用、数据图 |
| 五 | `compare.html` | 三项联合信条比较：体裁、问题、对照矩阵、签署书；为什么是三份 |
| 六 | `westminster.html` | 与威斯敏斯特标准（WCF/WLC/WSC）分主题对照 |
| 七 | `bct.html` | 比利时信条原文·背诵版（CCI 逐字，37 条） |
| 八 | `hct.html` | 海德堡要理问答原文·背诵版（52 主日 129 问） |
| 九 | `dtt.html` | 多特信经原文·背诵版（四项教义） |
| 十 | `creedsx.html` | 三大信经（使徒、尼西亚、亚他那修） |
| 十一 | `memory.html` | 七群口诀、思维导图、37 个钩子、15 句填空、翻卡、25 题自测、37 天计划 |
| 十二 | `sources.html` | 来源、图片版权、版本说明 |

站内功能：毛玻璃界面（v2 只留在少数大面板上）、可折叠与可拖宽的目录、六种主题、重点与难点按颜色标注、Mermaid 流程图、Leaflet 地图（OSM 底图）、SVG 动画、zh-CN 朗读、阅读进度保存在本地。

## v2.0.0 说明

**1. 性能（先测量，再改）。** 分析发现卡顿的主因是重复元素上的 `backdrop-filter`：bc 页每条六面卡都有毛玻璃，共几百个。v2 只在少数大面板保留毛玻璃，另外做了这些改动：
- 3 个 CSS 合并成 1 个，3 个 JS 合并成 1 个并 `defer`；
- Leaflet 地图和 Mermaid 流程图到可视区附近才加载；
- 流程图预留高度，消除布局位移；
- 区块使用 `content-visibility`，并加了锚点校正脚本；
- 动画只用 transform 和 opacity；
- 支持 `prefers-reduced-motion`、View Transitions 和 speculation rules 预取。

测量条件：Playwright 用 CDP 原生滚动手势。手机为 390 宽、4 倍 CPU 降速；桌面为 1280 宽。

| 页面 | 手机 fps（掉帧）v1 → v2 | 桌面 fps（掉帧）v1 → v2 |
|---|---|---|
| index | 58.9（3）→ **58.4（6）** | 58.0（5）→ **58.9（3）** |
| bible | 47.8（36）→ **42.0（60）** | 55.4（28）→ **53.8（32）** |
| hist | 45.5（78）→ **48.1（72）** | 54.4（41）→ **51.8（59）** |
| bc | 27.6（161）→ **46.4（68）** | 15.6（91）→ **38.0（120）** |
| topics | 55.9（32）→ **50.9（60）** | 57.8（18）→ **55.0（26）** |
| memory | 47.5（80）→ **48.2（79）** | 53.9（20）→ **56.2（26）** |
| hct | 52.9（58）→ **48.5（86）** | 38.0（164）→ **43.4（168）** |

上表是 v1、v2 在同一时段交替测量、各测两次的平均值。测量时机器负载较高，所以数值偏低；对比时请看同一行的前后差别。主要瓶颈在 bc 页：负载较低时单独测，手机从 36 fps（170 次掉帧）升到 58 fps（14 次），桌面从 17.8 fps 升到 57.8 fps。其余页面原本就接近 60 fps，前后差别在误差范围内。bible 页手机端的布局位移（CLS）从 0.09–0.64 降到 0。

Lighthouse（本地、未压缩，性能分 / FCP / LCP）：
- index：v1 98 / 1.8 s / 2.1 s → v2 99 / 1.7 s / 2.0 s
- bc：v1 85 / 3.2 s / 3.5 s → v2 87 / 3.0 s / 3.3 s
- hist：v1 92 / 2.4 s / 2.9 s → v2 97 / 1.8 s / 2.3 s

**2. 主题。** 共六种，点 🎨 切换，选择会保存在本地：🌌 夜空、🌅 晨曦、🌲 森林、🌊 海洋、🍇 葡萄、📜 羊皮纸。每种主题都在五种宽度下检查过，并截图核对了组件。

**3. 笔记式标注。** 每种标注只有一种含义，页内有图例，也可以一键关闭：

| 标注 | 含义 |
|---|---|
| 领域色粗体 | 术语 |
| 荧光底 | 必背 |
| 金实线 | 重点 |
| 红波浪线 | 难点 |
| 橙双线 | 误读 |
| 蓝虚线 | 经文 |
| 青点线 | 年代 |
| 绿底 | 应用 |

提示框分为：重点、难点、应用、说明、🚫 易错·误读（新增 12 条）、🧠 记忆。

**4. 可视化。** 新增 37 条篇幅柱状图（点柱子可跳到该条）和七群篇幅环形图。卡片悬浮时轻微上浮，背景有缓慢漂动的云层。

**5. 内容收紧。** 删去 13 个重复或偏题的小节，编号自动顺延，站内交叉引用已逐一核对。每条的“对手与界限 / 互参”默认折叠，主体只留四个方面：为什么写、说了什么、圣经与圣约、重点与难点。

**6. 按钮位置。** 🎨 和目录按钮上移，不再挡住 Netlify 右下角的徽标。

## 主要来源

- 原文：CCI《赞美手册》中文版 — ccifellowship.org
- 用户提供的 PDF：《中国改革宗教会敬拜手册》2015 版。只逐字摘引，PDF 本身不进仓库。
- 参考站：ccreformed.org、reformedbeginner.net、canrc.org、urcna.org、heritagereformed.com、prca.org、opc.org，以及各改革宗神学院的资料；威斯敏斯特标准。
- 图片：Wikimedia Commons（公有领域 / CC0 / CC BY-SA），出处与授权逐张列在 `sources.html`。
- 一般史实（年份、地名等）已在站内标注“约”或“一般史料”。

## 构建与检查

```bash
python3 build.py              # 生成全部 .html（引文不符即中止）
python3 tools/check_links.py  # 站内锚点：5460 个链接，0 失效
python3 tools/verify_exact.py # 原文逐字核对：513 段，0 缺失
python3 tools/qa.py           # 360/390/768/1280/1440 五种宽度：无溢出、无遮挡、无 JS 错误（THEME=night|dawn|jade|ocean|grape|parch）
W=390 CPU=4 python3 tools/perf2.py . bc.html   # 滚动帧率 / 掉帧 / CLS
```

## 版本记录

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v2.0.0 | 2026-10-23 | 性能与阅读体验版：去掉重复毛玻璃、合并资源、按需加载；六种主题；笔记式标注与图例；柱状图与环形图；收紧内容。地址：[Pages](https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/) · [Surge](https://belgic-confession-20261023-v2-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261023-v2-grokstudy.netlify.app/) |
| v1.0.0 | 2026-10-23 | 首发。12 部分完整上线；37 条逐条六个方面；交互地图、时间线、流程图、思维导图；CCI 逐字核对；BC/HC/Dort 背诵版；三项联合信条比较；记忆自测；夜间与晨光两种主题均通过五种宽度检查。地址：[Surge](https://belgic-confession-20261023-v1-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261023-v1-grokstudy.netlify.app/) · [标签 v1.0.0](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v1.0.0) |
