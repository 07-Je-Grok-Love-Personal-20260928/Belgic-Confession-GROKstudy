# belgic-confession-20261114-v3-GROKstudy

**《比利时信条》（Belgic Confession, 1561）· 欧陆改革宗深读**：简体中文多页学习站，页脚版本号为 `v20261114-3.1`（v3.1.0）。

站点从整本圣经与圣约的大图景讲起，然后讲历史、地理与文化（并配地图集），再把 37 条逐条展开。之后是专题深析、三项联合信条比较、威斯敏斯特对照，以及 BC / HC / Dort 与三大信经的原文背诵版、记忆自测。

> **引文规则**：全站信条原文和中文引号内的引文，都逐字取自 [CCI《赞美手册》中文版](https://ccifellowship.org/books/book-of-praise)。构建时由程序做子串核对（`core.Q`、`tools/verify_exact.py`），核对不过就不能构建。CCI 没有的内容，用用户提供的《中国改革宗教会敬拜手册》2015 版逐字摘引，并标明页码。

## 在线地址（当前 v3.1.0）

| 部署 | 地址 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/ |
| Surge | https://belgic-confession-20261114-v3-grokstudy.surge.sh/ |
| Netlify | https://belgic-confession-20261114-v3-grokstudy.netlify.app/ |
| 代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy |

较早版本仍保留为还原点：

- v2.0.0：[标签](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v2.0.0) · https://belgic-confession-20261023-v2-grokstudy.surge.sh/ · https://belgic-confession-20261023-v2-grokstudy.netlify.app/
- v1.0.0：[标签](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v1.0.0) · https://belgic-confession-20261023-v1-grokstudy.surge.sh/ · https://belgic-confession-20261023-v1-grokstudy.netlify.app/

命名规则：仓库名只用主题（`Belgic-Confession-GROKstudy`）；Surge / Netlify 的域名用“主题-日期-版本-grokstudy”。

## v3.1.0 说明（2026-11-14 13:10，台北时间）

- **流程图库本地化**：Mermaid 11.17.2（MIT，附 `assets/mermaid/LICENSE`）放在 `assets/mermaid/mermaid.min.js`，图表接近视口时才从本站加载。站内页面与资源已无任何 CDN 引用（jsdelivr、unpkg、cdnjs、googleapis 全站搜索为 0）；唯一的外部请求是实时地图的底图瓦片，屏蔽时自动回退并保留离线示意图。
- **离线测试**：新增 `tools/qa_mermaid.py`，屏蔽一切外部网络，流程图在 390 / 1280 宽度下都正常渲染（9 个节点，无溢出）。
- **清理**：删除构建脚本中残留的 unpkg Leaflet 与 jsdelivr 预连接代码；删除重复创建的空 Netlify 站点。
- **QA 全部 0 失败**：9 种宽度 × 14 页 × 6 种主题（全部展开 + 目录打开）、收起状态、底图屏蔽状态、点击测试、链接 5992 个 0 坏链、原文逐字 513 段 0 缺失、背诵版逐行核对、示意图标签重叠 0。

## v3.0.0 说明（2026-11-14，台北时间）

**1. 地图、历史、文化。** 新增独立页面「二续 · 地图集」。每一张图都是一对：

- **示意图**：页内 SVG，零网络也能看，用来讲关系和记忆钩；
- **实时地图**：可缩放、可点标记；底图可切换，某一源失败或超时会自动换下一个。

七张图：德布利足迹、宗教改革在欧洲的传播、腓利二世治下的低地十七省、逼迫与殉道地点、流亡教会（伦敦、埃姆登、法兰克福、韦瑟尔）、多特大会、三项联合信条的世界传播。

Leaflet 已放在 `assets/leaflet/`，不再依赖 CDN。底图来源（均无需密钥）：OpenStreetMap、OSM 德国、OSM France、OSM HOT、CARTO 浅色 / Voyager / 深色、Esri 街道 / 地形 / 卫星、OpenTopoMap；另有高德（中国大陆备用，GCJ-02 坐标，欧洲位置会偏移）。

**2. 性能。** 在 v2 去掉重复毛玻璃的基础上：本地托管 Leaflet、地图按需初始化、主题切换时暂停过渡与装饰动画、收紧阴影。滚动帧率在空闲机器上大多已接近 60 fps；v3 与 v2 的滚动差别多在误差范围内。主题切换仍会触发整页样式重算（地图集最明显），已尽量去掉过渡以免“拖泥带水”。交互与滚动的具体数字见下。

测量条件：Playwright + CDP 原生手势。手机 390 宽、4 倍 CPU 降速；桌面 1280 宽。以下为同一时段先测 v2、再测 v3 的一次完整滚动（空闲机器）：

| 页面 | 手机 fps（掉帧）v2 → v3 | 桌面 fps（掉帧）v2 → v3 |
|---|---|---|
| index | 59.6（1）→ **59.2（2）** | 59.3（2）→ **59.4（2）** |
| bible | 51.7（25）→ **55.0（18）** | 59.0（5）→ **54.5（19）** |
| hist | 57.0（17）→ **55.6（32）** | 59.4（5）→ **59.4（5）** |
| atlas（新） | — → **53.8（33）** | — → **59.5（4）** |
| bc | 57.3（17）→ **57.9（16）** | 58.6（12）→ **56.2（14）** |
| topics | 59.4（6）→ **59.3（7）** | 59.6（3）→ **59.9（1）** |
| memory | 55.1（32）→ **57.0（23）** | 59.2（7）→ **59.5（3）** |
| hct | 55.3（29）→ **58.3（12）** | 50.8（104）→ **31.7（174）** |

hct 桌面那一次偏差较大；随后在同一负载下交替各测两次，平均约为 v2 32.8 fps、v3 38.4 fps，v3 并不更差。bc 在该组平均为 v2 31.6、v3 41.5。

手机 390 宽、4 倍 CPU 降速下的交互（`tools/perf3.py`，v2 与 v3 各测 3 次取平均；“最长帧”越小越好）：

| 页面 | 连切 6 种主题 fps / 最长帧 v2 → v3 | 开关目录 v2 → v3 | 展开 20 个 details v2 → v3 | 地图平移 v3 |
|---|---|---|---|---|
| index | 45.0 / 111 ms → **50.0 / 83 ms** | 60 → 59.6 | 60.1 → 60.3 | — |
| bible | 51.1 / 78 ms → **51.7 / 72 ms** | 60 → 60 | 53.4 → **60.0** | — |
| hist | 51.1 / 72 ms → **52.4 / 72 ms** | 60 → 60 | 60.4 → 60.3 | 60.0 |
| bc | 49.4 / 89 ms → **49.3 / 83 ms** | 60 → 60 | 57.6 → 56.1 | — |
| atlas（新） | — → 49.1 / 100 ms | — → 58.8 | — → 60.0 | 52.6 |

主题切换的“去过渡”类改为在浏览器空闲时才移除（`requestIdleCallback`），把原来切换后约 0.4 s 的第二次整页样式重算移到空闲时段，不再与动画抢帧。连切 6 次是压力测试；单次点击在普通手机上只是一帧。

**3. 内容。** 在“南写北存”、流亡总会、十七省之名、多特的国际性等核心点上加深，不堆填词。圣经页增加“历史 / 告白 / 牧养”三个读法视角。地图集与历史页交叉引用。

**4. 笔记标记。** 含义与 v2 相同，加厚下划线、加大字距、荧光笔效果对浅色主题提高对比。图例仍可一键关闭。

**5. 可视化。** 七张示意动画 SVG（路线、船只、会场、世界弧线）、多源实时地图、已有的柱状图 / 环形图 / 城墙动画 / 故事线仍保留。不虚构来源。

**6. 示意图排版修正。** 时间轴站点按数量自动加宽，上下标注不再互压；十七省、多特会场、世界传播、德布利足迹几张示意图的标题与标签不再重叠，用 `tools/svg_overlap.py` 检查全站为 0。BC 2 的一处转述改成 CCI 原文“一部绝佳之作”“都如书中的字句”。

**7. 质量检查（全部 0 失败）。** 9 种宽度（320–1920）× 14 页 × 6 种主题，全部展开 + 目录打开；底图被屏蔽 / 正常加载两种状态；no-JS 与减少动态模式；新增 `tools/qa_click.py` 点击测试（目录、六个主题按钮、逐个点开所有折叠项、五个底图来源切换、屏蔽时自动回退提示）；站内链接 5992 个 0 坏链；原文逐字核对 513 段 0 缺失；背诵版逐行核对通过。

**8. 按钮位置。** 沿用 v2：🎨 与目录按钮上移，避开 Netlify 徽标。

## 页面结构

| # | 页面 | 内容 |
|---|---|---|
| 首页 | `index.html` | 学习路径与进度、可视化入口 |
| 一 | `bible.html` | 全本圣经与圣约；三个读法视角 |
| 二 | `hist.html` | 故事线、时间线、文化、人物、狱中书信；足迹成对地图 |
| 二续 | `atlas.html` | 七张成对地图（示意图 + 多源实时底图） |
| 三 | `bc.html` | 37 条逐条深读 |
| 四–六 | `topics.html` / `compare.html` / `westminster.html` | 专题、三项联合信条比较、威斯敏斯特对照 |
| 七–十 | `bct.html` / `hct.html` / `dtt.html` / `creedsx.html` | 原文背诵版 |
| 十一–十二 | `memory.html` / `sources.html` | 记忆自测、来源 |

六种主题（🌌 夜空、🌅 晨曦、🌲 森林、🌊 海洋、🍇 葡萄、📜 羊皮纸）点击切换，保存在本地。

## 主要来源

- 原文：CCI《赞美手册》中文版 — ccifellowship.org
- 用户提供的 PDF：《中国改革宗教会敬拜手册》2015 版。只逐字摘引，PDF 本身不进仓库。
- 参考站：ccreformed.org、reformedbeginner.net、canrc.org、urcna.org、heritagereformed.com、prca.org、opc.org，以及各改革宗神学院的资料；威斯敏斯特标准。
- 图片：Wikimedia Commons（公有领域 / CC0 / CC BY-SA），出处与授权逐张列在 `sources.html`。
- 地图底图：各提供方的公开瓦片，见上；示意图由本站绘制，不表示精确国界。
- 一般史实（年份、地名等）已在站内标注“约”或“一般史料”。

## 构建与检查

```bash
python3 build.py              # 生成全部 .html（引文不符即中止）
python3 tools/check_links.py  # 站内锚点
python3 tools/verify_exact.py # 原文逐字核对
python3 tools/qa.py           # 默认宽度 320/360/390/414/768/1024/1280/1440/1920
THEME=dawn python3 tools/qa.py --open --toc
python3 tools/qa.py --offline-tiles atlas.html hist.html
python3 tools/qa_click.py       # 点击交互 + 底图切换/回退
python3 tools/qa_mermaid.py     # 屏蔽外网时流程图渲染
python3 tools/svg_overlap.py atlas.html hist.html  # 示意图标签重叠
OUT=perf.json python3 tools/perf3.py . index.html atlas.html  # 交互帧率
```

## 版本记录

| 版本 | 日期（台北时间） | 说明 |
|---|---|---|
| v3.1.0 | 2026-11-14 13:10 | Mermaid 本站托管，全站无 CDN 依赖；离线流程图测试；清理残留 CDN 代码。地址同 v3：[Pages](https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/) · [Surge](https://belgic-confession-20261114-v3-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261114-v3-grokstudy.netlify.app/) · [发布 v3.1.0](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v3.1.0) |
| v3.0.0 | 2026-11-14 | 地图集：七张成对地图（离线示意 + 多源实时底图，Leaflet 本站托管）；加深历史地理；笔记标记加厚。地址：[Pages](https://07-je-grok-love-personal-20260928.github.io/Belgic-Confession-GROKstudy/) · [Surge](https://belgic-confession-20261114-v3-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261114-v3-grokstudy.netlify.app/) · [发布 v3.0.0](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v3.0.0)（2026-11-14 12:58 台北） |
| v2.0.0 | 2026-10-23 | 性能与阅读体验版：去掉重复毛玻璃、合并资源、按需加载；六种主题；笔记式标注与图例；柱状图与环形图；收紧内容。地址：[Surge](https://belgic-confession-20261023-v2-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261023-v2-grokstudy.netlify.app/) · [标签 v2.0.0](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v2.0.0) |
| v1.0.0 | 2026-10-23 | 首发。12 部分完整上线。地址：[Surge](https://belgic-confession-20261023-v1-grokstudy.surge.sh/) · [Netlify](https://belgic-confession-20261023-v1-grokstudy.netlify.app/) · [标签 v1.0.0](https://github.com/07-Je-Grok-Love-Personal-20260928/Belgic-Confession-GROKstudy/releases/tag/v1.0.0) |
