# 安徽华森氢能源科技 · 官网

安徽华森氢能源科技有限公司官方网站，中文 / English 双语，纯静态、零依赖，部署在 GitHub Pages。

**线上地址**：https://jeeftang.github.io/DESS-Calc/

## 网站定位

以燃气为源头的分布式冷、热、电联产整体解决方案：

- **四类气源**：沼气、煤层气 / 瓦斯、油田伴生气、城市天然气
- **核心产品**：100–150 kW 燃气重整制氢 + 燃料电池热电联产（CHP）
- **制冷产品**：30–480 kW 沼气源热泵空调（BHP），燃气发动机直驱压缩机
- **上游装备**：沼气发电 300 kW–2 MW、生物天然气提纯 CH₄ ≥97%
- **生产基地**：安徽海普克电气有限公司（安徽省宣城市泾县琴溪路 18 号）

## 目录结构

| 路径 | 内容 |
|---|---|
| `/` | 中文首页 |
| `/solutions/hydrogen-chp.html` | 重整制氢热电联产 CHP（四气源） |
| `/solutions/bhp.html` | 沼气源热泵空调 BHP |
| `/solutions/biogas.html` | 沼气发电与生物天然气提纯 |
| `/equipment.html` | 核心装备与供货范围 |
| `/cases.html` | 案例与场景 |
| `/about.html` | 公司与海普克生产基地 |
| `/contact.html` | 联系我们 |
| `/tools/` | 工程测算工具入口 |
| `/en/` | 英文镜像（同结构） |

## 工程测算工具（保留并迁移）

原 DESS 计算器已迁移到 `tools/`，逻辑未改：

| 文件 | 说明 |
|---|---|
| `tools/chp-industrial.html` | 工业版：百千瓦级重整制氢 CHP，协议口径 |
| `tools/chp-residential.html` | 民用版：别墅 / 自建房 |
| `tools/biogas.html` | 沼气工程 7 个计算器（发电、选型、提纯、经济性、CHP、BHP） |
| `tools/calc.js` | 沼气计算器脚本（纯前端） |
| `tools/selfcheck*.js` | 原自检脚本 |

所有计算均在浏览器本地完成，不上传数据。

## 生成与发布

页面由 `build_site.py` 生成（中文与英文共用一套模板）：

```sh
python3 build_site.py       # 重新生成全部 HTML、sitemap.xml、robots.txt
```

发布：提交到 `main` 分支后，GitHub Actions（`.github/workflows/pages.yml`）自动部署 GitHub Pages。

## 图片来源

- 华森产品与系统图：公司素材
- 沼气站现场：合作项目素材
- 海普克车间 / 设备照片：安徽海普克电气有限公司官网（www.hopcoelectric.com / www.hpkdq.com），仅用于介绍生产基地

## 数据口径

页面中的效率、气耗、余热等均为参考值，具体项目以气样分析、技术协议、厂家保证书与正式报价为准。
