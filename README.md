# belgic-confession-20261023-v1-GROKstudy

**《比利时信条》（Belgic Confession, 1561）· 欧陆改革宗深读**：这是一个简体中文多页学习站，页脚版本号为 `v20261023-1`。

站点从整本圣经与圣约的大图景讲起，然后讲历史、地理与文化，再把 37 条逐条展开。每一条都从六个方面来读：为什么写、说了什么、圣经与圣约、对手与联系、重点与难点、怎样应用。之后是专题深析，以及三项联合信条的比较（为什么是三份而不是一份）和威斯敏斯特标准对照。站内还有 BC / HC / Dort 的原文背诵版、三大信经和记忆自测。

> **引文规则**：全站信条原文和中文引号内的引文，都逐字取自 [CCI《赞美手册》中文版](https://ccifellowship.org/books/book-of-praise)。构建时由程序做子串核对（`core.Q`、`tools/verify_exact.py`），核对不过就不能构建。CCI 没有的内容，用用户提供的《中国改革宗教会敬拜手册》2015 版逐字摘引，并标明页码。

## 在线地址（v1.0.0）

| 部署 | 地址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/ |
| Surge | https://belgic-confession-20261023-v1-grokstudy.surge.sh/ |
| Netlify | https://belgic-confession-20261023-v1-grokstudy.netlify.app/ |
| 代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy |

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

站内功能：毛玻璃界面、可折叠与可拖宽的目录、夜间/晨光两种主题、重点与难点按颜色标注、Mermaid 流程图、Leaflet 地图（OSM 底图）、SVG 动画、zh-CN 朗读、阅读进度保存在本地。

## 主要来源

- 原文：CCI《赞美手册》中文版 — ccifellowship.org
- 用户提供的 PDF：《中国改革宗教会敬拜手册》2015 版。只逐字摘引，PDF 本身不进仓库。
- 参考站：ccreformed.org、reformedbeginner.net、canrc.org、urcna.org、heritagereformed.com、prca.org、opc.org，以及各改革宗神学院的资料；威斯敏斯特标准。
- 图片：Wikimedia Commons（公有领域 / CC0 / CC BY-SA），出处与授权逐张列在 `sources.html`。
- 一般史实（年份、地名等）已在站内标注“约”或“一般史料”。

## 构建与检查

```bash
python3 build.py              # 生成全部 .html（引文不符即中止）
python3 tools/check_links.py  # 站内锚点：5695 个链接，0 失效
python3 tools/verify_exact.py # 原文逐字核对：513 段，0 缺失
python3 tools/qa.py           # 360/390/768/1280/1440 五种宽度：无溢出、无遮挡、无 JS 错误
```

## 版本记录

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v1.0.0 | 2026-10-23 | 首发。12 部分完整上线；37 条逐条六个方面；交互地图、时间线、流程图、思维导图；CCI 逐字核对；BC/HC/Dort 背诵版；三项联合信条比较；记忆自测；夜间与晨光两种主题均通过五种宽度检查。 |
