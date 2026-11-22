#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""安徽华森氢能源科技官网生成器（中文 / English 双语，纯静态）。
运行：python3 build_site.py
输出：index.html、各内页、en/ 镜像页。
"""
from pathlib import Path
import json

BASE = "https://jeeftang.github.io/DESS-Calc"
HERE = Path(__file__).resolve().parent

NAV = {
    "zh": [
        ("首页", ""),
        ("重整制氢 CHP", "solutions/hydrogen-chp.html"),
        ("沼气源空调 BHP", "solutions/bhp.html"),
        ("沼气发电与提纯", "solutions/biogas.html"),
        ("核心装备", "equipment.html"),
        ("工程工具", "tools/"),
        ("关于华森", "about.html"),
    ],
    "en": [
        ("Home", ""),
        ("H₂ CHP", "solutions/hydrogen-chp.html"),
        ("BHP Air-Con", "solutions/bhp.html"),
        ("Biogas Power", "solutions/biogas.html"),
        ("Equipment", "equipment.html"),
        ("Tools", "tools/"),
        ("About", "about.html"),
    ],
}

BRAND = {
    "zh": ("华森氢能", "HUASEN HYDROGEN"),
    "en": ("HUASEN HYDROGEN", "Anhui Huasen Hydrogen Energy"),
}
CTA = {"zh": "获取方案", "en": "Request a study"}
FOOT_DESC = {
    "zh": "安徽华森氢能源科技有限公司，聚焦沼气、煤层气、油田伴生气与城市天然气的重整制氢热电联产，以及沼气源热泵空调 BHP，提供分布式冷、热、电联产整体解决方案。",
    "en": "Anhui Huasen Hydrogen Energy Technology Co., Ltd. delivers distributed cooling, heating and power from biogas, coal mine gas, oilfield associated gas and city natural gas — methane reforming hydrogen CHP and biogas-driven heat-pump air conditioning (BHP).",
}


def rel(depth):
    return "../" * depth


def depth_of(slug, lang="zh"):
    """页面相对站点根的目录层数。slug 含文件名，故目录层数 = '/' 数量。"""
    return slug.count("/") + (1 if lang == "en" else 0)


def other_lang_url(lang, slug, depth):
    r = rel(depth)
    if lang == "zh":
        return r + "en/" + slug
    return r + slug


def canonical(lang, slug):
    if lang == "zh":
        return BASE + "/" + slug
    return BASE + "/en/" + slug


def header(lang, slug, depth):
    r = rel(depth)
    lr = rel(depth - (1 if lang == "en" else 0))
    b1, b2 = BRAND[lang]
    items = []
    for label, s in NAV[lang]:
        href = (lr + "index.html") if s == "" else (lr + s)
        cur = ' aria-current="page"' if s == slug else ""
        items.append(f'<a href="{href}"{cur}>{label}</a>')
    lang_href = other_lang_url(lang, slug, depth)
    if lang == "zh":
        lang_html = f'<a href="{lang_href}" class="on">中文</a><a href="{lang_href}" hreflang="en">EN</a>'
        # 当前语言链接用 #，另一语言才跳转
        lang_html = f'<a href="#" class="on">中文</a><a href="{lang_href}" hreflang="en">EN</a>'
    else:
        zh_href = lang_href
        lang_html = f'<a href="{zh_href}" hreflang="zh">中文</a><a href="#" class="on">EN</a>'
    contact = lr + "contact.html"
    return f'''<header class="site-header">
  <div class="wrap nav-bar">
    <a class="brand" href="{lr}index.html" aria-label="{'安徽华森氢能源科技' if lang=='zh' else 'Anhui Huasen Hydrogen Energy'}">
      <span style="display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:11px;background:#0b1f1a;padding:4px"><img src="{r}assets/img/huasen-logo.png" alt="{'华森氢能 logo' if lang=='zh' else 'Huasen Hydrogen logo'}" style="height:38px;width:auto"></span>
      <span class="bt"><b>{b1}</b><span>{b2}</span></span>
    </a>
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false">☰</button>
    <nav class="main-nav" id="mainNav">{''.join(items)}</nav>
    <div class="nav-tools">
      <div class="lang" role="group" aria-label="Language">{lang_html}</div>
      <a class="btn sm" href="{contact}">{CTA[lang]}</a>
    </div>
  </div>
</header>'''


def footer(lang, depth):
    r = rel(depth)
    lr = rel(depth - (1 if lang == "en" else 0))
    if lang == "zh":
        sol = f'''<li><a href="{lr}solutions/hydrogen-chp.html">重整制氢热电联产</a></li>
        <li><a href="{lr}solutions/bhp.html">沼气源热泵空调 BHP</a></li>
        <li><a href="{lr}solutions/biogas.html">沼气发电与提纯</a></li>
        <li><a href="{lr}equipment.html">核心装备与供货范围</a></li>'''
        comp = f'''<li><a href="{lr}about.html">关于华森</a></li>
        <li><a href="{lr}about.html#base">生产基地</a></li>
        <li><a href="{lr}cases.html">案例与场景</a></li>
        <li><a href="{lr}contact.html">联系我们</a></li>'''
        contact = '''<li>安徽华森氢能源科技有限公司</li>
        <li>商务咨询：刘洋　<a href="tel:+8613252949897">132 5294 9897</a></li>
        <li>生产基地：安徽省宣城市泾县琴溪路 18 号</li>
        <li><a href="tel:+8619565726668">195-6572-6668</a>　<a href="mailto:Hopco@hpkdq.com">Hopco@hpkdq.com</a></li>'''
        copy = f'<span>© <span id="year">2026</span> 安徽华森氢能源科技有限公司</span><span>参数为参考值，具体以气样分析、技术协议与正式报价为准。</span>'
        tools = f'<li><a href="{lr}tools/">CHP 工程测算工具</a></li><li><a href="{lr}tools/biogas.html">沼气工程计算器</a></li>'
    else:
        sol = f'''<li><a href="{lr}solutions/hydrogen-chp.html">Reforming hydrogen CHP</a></li>
        <li><a href="{lr}solutions/bhp.html">Biogas heat-pump air-con (BHP)</a></li>
        <li><a href="{lr}solutions/biogas.html">Biogas power &amp; upgrading</a></li>
        <li><a href="{lr}equipment.html">Equipment &amp; scope</a></li>'''
        comp = f'''<li><a href="{lr}about.html">About Huasen</a></li>
        <li><a href="{lr}about.html#base">Manufacturing base</a></li>
        <li><a href="{lr}cases.html">Cases &amp; scenarios</a></li>
        <li><a href="{lr}contact.html">Contact</a></li>'''
        contact = '''<li>Anhui Huasen Hydrogen Energy Technology Co., Ltd.</li>
        <li>Sales: Liu Yang　<a href="tel:+8613252949897">+86 132 5294 9897</a></li>
        <li>Production base: No. 18 Qinxi Road, Jing County, Xuancheng, Anhui, China</li>
        <li><a href="tel:+8619565726668">+86 195-6572-6668</a>　<a href="mailto:Hopco@hpkdq.com">Hopco@hpkdq.com</a></li>'''
        copy = f'<span>© <span id="year">2026</span> Anhui Huasen Hydrogen Energy Technology Co., Ltd.</span><span>Figures are indicative; project values are confirmed by gas analysis, technical agreement and formal quotation.</span>'
        tools = f'<li><a href="{lr}tools/">CHP engineering calculators</a></li><li><a href="{lr}tools/biogas.html">Biogas calculators</a></li>'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a class="brand" href="{lr}index.html">
          <img src="{r}assets/img/huasen-logo.png" alt="Huasen Hydrogen" style="height:44px">
          <span class="bt"><b>{BRAND[lang][0]}</b><span>{BRAND[lang][1]}</span></span>
        </a>
        <p class="small" style="color:#9fb6ac;margin:10px 0 0;max-width:340px">{FOOT_DESC[lang]}</p>
      </div>
      <div><h4>{'解决方案' if lang=='zh' else 'Solutions'}</h4><ul>{sol}</ul></div>
      <div><h4>{'公司' if lang=='zh' else 'Company'}</h4><ul>{comp}</ul></div>
      <div><h4>{'联系' if lang=='zh' else 'Contact'}</h4><ul>{contact}</ul></div>
    </div>
    <div class="copy">{copy}</div>
  </div>
</footer>'''


def fix_body_links(body, lang, depth):
    """把正文里相对站点根/语言根的链接，按页面层级补全前缀。"""
    import re as _re
    site_root = rel(depth)
    lang_root = rel(depth - (1 if lang == "en" else 0))
    def repl(m):
        attr, u = m.group(1), m.group(2)
        if (not u) or u.startswith(("#", "http", "https", "mailto:", "tel:", "data:", "javascript:", "/", "../")):
            return m.group(0)
        prefix = site_root if u.startswith("assets/") else lang_root
        return f'{attr}="{prefix}{u}"'
    return _re.sub(r'(href|src)="([^"]+)"', repl, body)


def page(lang, slug, title, desc, body, extra_head=""):
    depth = depth_of(slug, lang)
    r = rel(depth)
    body = fix_body_links(body, lang, depth)
    lang_attr = "zh-CN" if lang == "zh" else "en"
    alt = other_lang_url(lang, slug, depth)
    canon = canonical(lang, slug)
    suffix = "安徽华森氢能源科技" if lang == "zh" else "Anhui Huasen Hydrogen Energy"
    full_title = title if (title == suffix or suffix in title) else f"{title} | {suffix}"
    org_name = "安徽华森氢能源科技有限公司" if lang == "zh" else "Anhui Huasen Hydrogen Energy Technology Co., Ltd."
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org_name,
        "alternateName": "Huasen Hydrogen",
        "url": canon,
        "logo": BASE + "/assets/img/huasen-logo.png",
        "description": desc,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "泾县琴溪路18号" if lang == "zh" else "No. 18 Qinxi Road, Jing County",
            "addressLocality": "宣城市" if lang == "zh" else "Xuancheng",
            "addressRegion": "安徽省" if lang == "zh" else "Anhui",
            "addressCountry": "CN",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+86-13252949897",
            "contactType": "sales",
            "availableLanguage": ["zh-CN", "en"],
        },
    }
    return f'''<!doctype html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="{'zh-CN' if lang=='zh' else 'en'}" href="{canon}">
<link rel="alternate" hreflang="{'en' if lang=='zh' else 'zh-CN'}" href="{BASE + '/' + alt if lang=='zh' else BASE + '/' + alt.lstrip('../')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{suffix}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/img/og-huasen.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1f1a">
<link rel="icon" href="{r}assets/img/huasen-logo.png">
<link rel="stylesheet" href="{r}assets/css/site.css">
<script src="{r}assets/js/site.js" defer></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{extra_head}
</head>
<body>
{header(lang, slug, depth)}
{body}
{footer(lang, depth)}
</body>
</html>
'''


def write(path, text):
    p = HERE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path, len(text))


# =====================================================================
# 中文页面
# =====================================================================

def zh_home():
    body = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">分布式氢能 · 冷热电联产</span>
      <h1>把每一方燃气<br>变成<em>电、热、冷</em></h1>
      <p class="lead">沼气、煤层气、油田伴生气、城市天然气，经重整制氢进入燃料电池热电联产；沼气源热泵空调补齐制冷。从气源到末端，一套系统、一份责任。</p>
      <div class="hero-actions">
        <a class="btn light" href="contact.html">获取项目方案</a>
        <a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.3)" href="tools/">打开工程测算工具</a>
      </div>
      <div class="hero-stats">
        <div><b>100–150 kW</b><span>单机发电功率，撬装交付</span></div>
        <div><b>≥40%</b><span>发电效率（按氢 LHV）</span></div>
        <div><b>≥85%</b><span>热电综合效率</span></div>
        <div><b>≥8,000 h</b><span>年设计运行时间</span></div>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-card">
        <img src="assets/img/huasen/assembly-skid.jpg" alt="重整制氢燃料电池热电联产撬装装置">
        <div class="cap"><span>重整制氢 + 燃料电池热电联产撬装</span><span>100–150 kW</span></div>
      </div>
      <div class="hero-badge"><b>CHP ≥85%</b>电 + 热，一次产出</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">四类气源，一条技术路线</span>
      <h2>有什么气，就做什么样的分布式能源</h2>
      <p class="lead">不挑气源，只挑气质。我们先把气净化到重整器能接受的范围，再按用能负荷配置制氢、发电与余热回收。</p>
    </div>
    <div class="grid g4">
      <article class="card gas-card"><div class="ico">沼</div><h3>沼气</h3>
        <p>畜禽粪污、食品废水、秸秆、垃圾填埋、棕榈油厂 POME。</p>
        <ul><li>CH₄ 50–65%</li><li>脱硫 + 脱水 + 稳压</li><li>养殖场自用或并网</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">煤</div><h3>煤层气 / 瓦斯</h3>
        <p>煤矿井下抽采瓦斯、瓦斯泵站与瓦斯电站。</p>
        <ul><li>CH₄ 30–80%</li><li>浓缩 / 掺混 + 精脱硫</li><li>以电为主、余热供暖</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">油</div><h3>油田伴生气</h3>
        <p>边远井、集输站、放空与火炬气资源化。</p>
        <ul><li>CH₄ 60–90%</li><li>脱重烃 + 脱水 + 稳压</li><li>替代柴油机与火炬</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">气</div><h3>城市天然气</h3>
        <p>门站、工商业园区、酒店、医院与数据中心。</p>
        <ul><li>CH₄ 90–99%</li><li>调压 + 精脱硫</li><li>电、热、冷三联供</li></ul>
      </article>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">系统怎么走</span>
      <h2>从气源到冷热电，五步闭合</h2>
      <p class="lead">核心装备做成撬装，现场只做接管、接电、接水与调试。氢气按需现制、机内即用，不设高压储氢。</p>
    </div>
    <div class="flow">
      <div class="step"><b>净化稳压</b><span>脱硫至 H₂S ≤ 20 ppm，脱水、过滤、稳压。</span></div>
      <div class="step"><b>重整制氢</b><span>700–850℃ 蒸汽重整，甲烷 + 水 → 氢 + CO。</span></div>
      <div class="step"><b>变换提纯</b><span>水煤气变换 + PSA，产品氢 ≥70%，CO &lt; 10 ppm。</span></div>
      <div class="step"><b>燃料电池</b><span>PEMFC 电化学发电，无高温火焰、低噪声。</span></div>
      <div class="step"><b>余热回收</b><span>并出 40–50℃ 热水，供发酵罐、供暖或生活热水。</span></div>
    </div>
    <div class="split" style="margin-top:46px">
      <div class="visual"><img src="assets/img/huasen/principle-system.png" alt="燃气重整制氢燃料电池热电联产系统流程"></div>
      <div>
        <h2 style="font-size:28px;margin-bottom:14px">电和热，本来就该一起算</h2>
        <p class="lead">燃料电池发电效率 ≥40%，其余大部分以余热形式回收，综合效率 ≥85%。对养殖场、油田站场和园区来说，热往往比电更值钱。</p>
        <ul class="checklist">
          <li>余热优先回用厌氧罐增温，破解寒区冬季产气衰减</li>
          <li>热水、蒸汽、吸收制冷按负荷梯级利用</li>
          <li>并网 / 孤岛 / 黑启动可选，适配弱电网</li>
          <li>模块化并联，按气量分期扩容</li>
        </ul>
        <a class="btn ghost" href="solutions/hydrogen-chp.html">看技术细节</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">产品与装备</span>
      <h2>四条产品线，覆盖从气到冷热电</h2>
    </div>
    <div class="grid g4">
      <article class="card prod-card">
        <img src="assets/img/huasen/assembly-skid.jpg" alt="重整制氢燃料电池热电联产机组">
        <div class="body"><span class="tag">CHP</span><h3>重整制氢热电联产</h3>
          <p>100–150 kW 撬装，电 + 热水，适用于沼气、煤层气、伴生气与天然气。</p>
          <a class="mini-link" href="solutions/hydrogen-chp.html">查看机型</a></div>
      </article>
      <article class="card prod-card">
        <img src="assets/img/bhp/bhp-unit.svg" alt="沼气源热泵空调 BHP 室外机" style="object-fit:contain;background:#f2f7f5;padding:14px">
        <div class="body"><span class="tag">BHP</span><h3>沼气源热泵空调</h3>
          <p>30–480 kW，燃气发动机直驱压缩机，不靠电网制冷，余热还可出热水。</p>
          <a class="mini-link" href="solutions/bhp.html">查看机型</a></div>
      </article>
      <article class="card prod-card">
        <img src="assets/img/biogas/plant-01.jpg" alt="沼气发电站">
        <div class="body"><span class="tag">POWER</span><h3>沼气发电机组</h3>
          <p>300 kW–2 MW，集装箱或撬装，孤岛 / 并网，配套净化与余热回收。</p>
          <a class="mini-link" href="solutions/biogas.html">查看范围</a></div>
      </article>
      <article class="card prod-card">
        <img src="assets/img/biogas/plant-02.jpg" alt="生物天然气提纯装置">
        <div class="body"><span class="tag">UPGRADING</span><h3>生物天然气提纯</h3>
          <p>PSA / 水洗 / 膜分离，CH₄ ≥97%，供锅炉、车用或 Bio-CNG。</p>
          <a class="mini-link" href="solutions/biogas.html">查看工艺</a></div>
      </article>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">为什么是华森</span>
      <h2>工艺包、装备、现场，一条责任链</h2>
      <p class="lead">重整制氢不是把几台设备拼在一起。气源、催化剂、燃料电池、余热与并网，必须有人对整条链负责。</p>
    </div>
    <div class="grid g4">
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
        <h3 style="color:#fff">工艺包</h3><p style="color:#b8ccc4">与中石化大连石油化工研究院联合开发重整制氢工艺包、催化剂与系统设计。</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
        <h3 style="color:#fff">装备制造</h3><p style="color:#b8ccc4">安徽海普克电气有限公司承担撬装集成与成套制造，西门子 ICP 体系、ISO 三体系与 CE 认证。</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
        <h3 style="color:#fff">技术团队</h3><p style="color:#b8ccc4">清华大学、天津大学、中科院大连化物所博士领衔，覆盖工艺、装备、控制与调试。</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
        <h3 style="color:#fff">商业模型</h3><p style="color:#b8ccc4">设备成套 / EPC、EMC 合同能源管理、EaaS 能源即服务，按业主偏好选择。</p></div>
    </div>
    <div class="stat-band" style="margin-top:30px;background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">1</b><span>套系统对冷热电负责</span></div>
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">2</b><span>家院所联合研发</span></div>
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">3</b><span>地博士团队</span></div>
      <div><b style="color:#8fe0b8">4</b><span>类气源全覆盖</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">样板与场景</span>
        <h2 style="font-size:32px;margin:12px 0 14px">寒区猪场，余热回罐</h2>
        <p class="lead">黑龙江宝泉岭，常年存栏 9,000 头以上规模化猪场。粪污厌氧发酵产沼气，配置 120–150 kW 沼气重整制氢热电联产机组。</p>
        <ul class="checklist">
          <li>年发电约 105–131 万 kWh，余热 150–250 kW</li>
          <li>余热回用发酵罐增温，最冷月需求 80–120 kW</li>
          <li>破解北方寒区沼气池冬季产气衰减 70–90% 的行业难题</li>
          <li>已获黑龙江省农业科学院推荐</li>
        </ul>
        <a class="btn ghost" href="cases.html">更多案例与场景</a>
      </div>
      <div class="visual"><img src="assets/img/biogas/plant-03.jpg" alt="沼气工程现场"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>把你的气源数据发给我们</h2><p>气源类型、流量、甲烷与硫化氢含量、用能负荷——有这几项，我们就能给出机型、投资区间与回收期。</p></div>
      <div class="actions"><a class="btn light" href="contact.html">联系华森</a><a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="tools/">先自己算一遍</a></div>
    </div>
  </div>
</section>
'''
    return page("zh", "", "安徽华森氢能源科技 · 分布式冷热电联产", "安徽华森氢能源科技：沼气、煤层气、油田伴生气、城市天然气重整制氢热电联产 CHP，沼气源热泵空调 BHP，分布式冷热电联产整体解决方案。", body)


def zh_chp():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 解决方案 / 重整制氢 CHP</div>
    <span class="eyebrow">100–150 kW · 撬装交付</span>
    <h1>燃气重整制氢 · 燃料电池热电联产</h1>
    <p class="lead">把沼气、煤层气、油田伴生气或城市天然气，就地变成电和热水。发电效率 ≥40%，热电综合效率 ≥85%，年运行 ≥8,000 小时。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split img-right">
      <div>
        <span class="eyebrow">技术路线</span>
        <h2 style="font-size:30px;margin:12px 0 14px">不储氢，现制现用</h2>
        <p class="lead">天然气或沼气经净化后进入重整器，生成富氢合成气，再经变换与 PSA 提纯到燃料电池可用的氢气。氢气不装瓶、不高压储存，即产即用。</p>
        <ul class="checklist">
          <li>进气要求：H₂S ≤ 20 ppm、CO₂ ≤ 20%（更高 CO₂ 需前端脱碳）</li>
          <li>产品氢 ≥70%，CO &lt; 10 ppm</li>
          <li>PEMFC 发电，40–50℃ 热水回收</li>
          <li>并网、孤岛、黑启动可选</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/huasen/principle-fuelcell.png" alt="燃料电池热电联产原理"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">气源适配</span>
      <h2>四类气源，各自的净化重点</h2>
      <p class="lead">同一套重整与燃料电池平台，前端按气源配置。气质分析是选型的第一步，也是质保边界。</p>
    </div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>气源</th><th>典型甲烷含量</th><th>前端净化要点</th><th>典型场景</th></tr></thead>
        <tbody>
          <tr><td><b>沼气</b></td><td>50–65%</td><td>脱硫至 H₂S ≤20 ppm、脱水、过滤；CO₂ 高时增设脱碳</td><td>畜禽养殖、食品废水、秸秆、垃圾填埋、POME</td></tr>
          <tr><td><b>煤层气 / 瓦斯</b></td><td>30–80%</td><td>浓缩或掺混、精脱硫、脱水、稳压</td><td>煤矿抽采瓦斯、瓦斯泵站、瓦斯电站</td></tr>
          <tr><td><b>油田伴生气</b></td><td>60–90%</td><td>脱重烃、脱硫、脱水、稳压</td><td>边远井、集输站、放空火炬气</td></tr>
          <tr><td><b>城市天然气</b></td><td>90–99%</td><td>调压、精脱硫（含加臭剂）、过滤</td><td>门站、园区、酒店、医院、数据中心</td></tr>
          <tr><td><b>生物天然气 / CNG（延伸）</b></td><td>96–99%</td><td>减压、调压、过滤</td><td>管网未覆盖站点、瓶装气/槽车供气</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">煤层气浓度低于 30% 时，需先浓缩或与天然气掺混；具体边界按气样与流量逐项确认。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">机型</span>
      <h2>三个标准机型，按气量与负荷选</h2>
      <p class="lead">发电效率按氢 LHV 计 ≥40%；余热按燃料输入约 45% 估算。多台并联可扩展到数百千瓦。</p>
    </div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>机型</th><th class="num">发电功率</th><th class="num">燃料输入</th><th class="num">纯甲烷耗量</th><th class="num">60% 沼气耗量</th><th class="num">可回收余热</th></tr></thead>
        <tbody>
          <tr><td><b>HS-CHP-100</b></td><td class="num">100 kW</td><td class="num">250 kW</td><td class="num">25.2 Nm³/h</td><td class="num">41.9 Nm³/h</td><td class="num">≈112 kW</td></tr>
          <tr class="hl"><td><b>HS-CHP-120</b></td><td class="num">120 kW</td><td class="num">300 kW</td><td class="num">30.2 Nm³/h</td><td class="num">50.3 Nm³/h</td><td class="num">≈135 kW</td></tr>
          <tr><td><b>HS-CHP-150</b></td><td class="num">150 kW</td><td class="num">375 kW</td><td class="num">37.7 Nm³/h</td><td class="num">62.9 Nm³/h</td><td class="num">≈169 kW</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">按甲烷 LHV 9.94 kWh/Nm³、发电效率 40%、余热回收 45% 估算；实际以气样分析、环境条件与厂家保证值为准。热水温度 40–50℃，可按项目提升或用于吸收制冷。</p>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">运行特征</span>
      <h2>没有发动机，没有明火</h2>
      <p class="lead">燃料电池是电化学发电，不是燃烧。对居民区、养殖场、油田站场和园区来说，这意味着更低的噪声与更简单的排放治理。</p>
    </div>
    <div class="grid g3">
      <div class="card"><h3>低噪声</h3><p>主要运动部件是风机与水泵，1 米处约 55 dB(A)，可直接布置在站房或宿舍附近。</p></div>
      <div class="card"><h3>低排放</h3><p>无高温火焰，NOx、SOx 与颗粒物排放极低；燃气先脱硫，硫不进工艺也不出排气。</p></div>
      <div class="card"><h3>工艺产水</h3><p>燃料电池电化学反应生成水，可回收用于冲洗或灌溉；不产生废油与黑烟。</p></div>
      <div class="card"><h3>负荷跟随</h3><p>按用电负荷自动调节出力，气量不足时降功率运行，避免频繁启停。</p></div>
      <div class="card"><h3>无人值守</h3><p>PLC + 远程监控，关键参数越限报警；可选远程诊断与运维托管。</p></div>
      <div class="card"><h3>模块扩容</h3><p>单机 100–150 kW，多台并联；先上一台，气量增加后再扩。</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">交付边界</span>
        <h2 style="font-size:30px;margin:12px 0 14px">我们供什么，不供什么</h2>
        <p class="lead">把边界写清楚，是项目最便宜的风险控制。</p>
        <ul class="checklist">
          <li>供货：净化撬、重整撬、PSA、燃料电池、余热回收、控制柜与撬内管路</li>
          <li>服务：气样分析、工艺设计、安装指导、调试、培训、运维托管</li>
          <li>不含：土建基础、外部燃气管线、并网审批、业主侧用电改造</li>
          <li>可含：并网柜、黑启动、吸收制冷、远程监控平台</li>
        </ul>
        <a class="btn" href="contact.html">索取技术协议与报价</a>
      </div>
      <div class="visual"><img src="assets/img/huasen/inside-01.jpg" alt="热电联产机组内部"></div>
    </div>
  </div>
</section>
'''
    return page("zh", "solutions/hydrogen-chp.html", "燃气重整制氢热电联产 CHP 100–150 kW", "沼气、煤层气、油田伴生气、城市天然气重整制氢，燃料电池热电联产。发电效率≥40%，综合效率≥85%，100–150 kW 撬装交付。", body)


def zh_bhp():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 解决方案 / 沼气源热泵空调 BHP</div>
    <span class="eyebrow">30–480 kW · 燃气发动机直驱</span>
    <h1>沼气源热泵空调 BHP</h1>
    <p class="lead">锅炉停了，空调不停。小型燃气发动机直接驱动压缩机，燃料是沼气或生物天然气，驱动链里没有电机，制冷不依赖电网。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split img-right">
      <div>
        <span class="eyebrow">为什么需要它</span>
        <h2 style="font-size:30px;margin:12px 0 14px">切断“锅炉—汽机—市电”的单点依赖</h2>
        <p class="lead">养殖场、沼气站、食品厂和园区的空调，常常挂在同一条链上：锅炉停、汽机停、厂用电紧张，办公室和宿舍最先失去制冷。BHP 把这条链切断。</p>
        <ul class="checklist">
          <li>燃气发动机直驱开式压缩机，不经过发电机与电动机</li>
          <li>单机制冷 30–480 kW，最多 8 台并联到 MW 级</li>
          <li>97% 甲烷进气，5–20 kPa；H₂S &lt; 10 ppm</li>
          <li>发动机余热可选回收 60–90℃ 热水</li>
          <li>撬装室外机，落地或屋顶安装，无需机房</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/bhp/bhp-unit.svg" alt="BHP 沼气源热泵空调室外机" style="background:#f2f7f5;padding:18px"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">工作原理</span>
      <h2>进气、出冷，顺带出热水</h2>
      <p class="lead">它不是吸收式冷水机。发动机对压缩机做机械功，1 方甲烷约出 10 度冷量，比同气量进单效吸收式机组大约多 50%。</p>
    </div>
    <div class="split">
      <div class="visual"><img src="assets/img/bhp/bhp-principle-zh.svg" alt="BHP 工作原理" style="background:#fff;padding:14px"></div>
      <div>
        <div class="flow" style="grid-template-columns:1fr 1fr">
          <div class="step"><b>进气</b><span>97% 甲烷、5–20 kPa，过滤调压后进机。</span></div>
          <div class="step"><b>发动机</b><span>火花点火燃气机，联轴器或皮带输出轴功。</span></div>
          <div class="step"><b>压缩制冷</b><span>开式往复/涡旋压缩机，转速与卸载调节冷量。</span></div>
          <div class="step"><b>余热</b><span>缸套水与烟气换热，出 60–90℃ 热水。</span></div>
        </div>
        <div class="callout" style="margin-top:20px"><b>COP 口径：</b>按燃气低热值计，典型 COP 约 1.0；若按电等效看，压缩机本身 COP 约 3.0。变的是轴功从哪来，不是制冷效率变差。</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">机型</span>
      <h2>五个标称机型，30 到 480 kW</h2>
      <p class="lead">燃料输入按额定制冷量与燃气 COP 1.0 口径；余热为制冷模式下可回收的发动机余热，热水温升按 50 K 估算。</p>
    </div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>机型</th><th class="num">制冷量</th><th class="num">燃气输入</th><th class="num">97% 甲烷耗量</th><th class="num">可回收余热</th><th class="num">热水 50 K</th></tr></thead>
        <tbody>
          <tr><td><b>BHP-30</b></td><td class="num">30 kW</td><td class="num">30.0 kW</td><td class="num">3.0 Nm³/h</td><td class="num">7.5 kW</td><td class="num">129 L/h</td></tr>
          <tr><td><b>BHP-60</b></td><td class="num">60 kW</td><td class="num">60.0 kW</td><td class="num">6.0 Nm³/h</td><td class="num">15.0 kW</td><td class="num">258 L/h</td></tr>
          <tr class="hl"><td><b>BHP-120</b></td><td class="num">120 kW</td><td class="num">120.0 kW</td><td class="num">12.1 Nm³/h</td><td class="num">30.0 kW</td><td class="num">517 L/h</td></tr>
          <tr><td><b>BHP-240</b></td><td class="num">240 kW</td><td class="num">240.0 kW</td><td class="num">24.1 Nm³/h</td><td class="num">60.0 kW</td><td class="num">1,034 L/h</td></tr>
          <tr><td><b>BHP-480</b></td><td class="num">480 kW</td><td class="num">480.0 kW</td><td class="num">48.3 Nm³/h</td><td class="num">120.0 kW</td><td class="num">2,069 L/h</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">更大负荷多台并联。性能数据为参考值，每个项目以厂家保证书与现场气样为准。原料为原沼气时，需先提纯至 97% 甲烷或配置前端净化。</p>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">适用场景</span><h2>哪里最适合</h2></div>
    <div class="grid g3">
      <div class="card"><h3>养殖场与沼气站</h3><p>用自产沼气给办公区、宿舍、化验室供冷，余热回用发酵罐或生活热水。</p></div>
      <div class="card"><h3>食品与农产品加工</h3><p>屠宰、酿造、果蔬加工有稳定沼气与冷负荷，替代电空调与柴油机组。</p></div>
      <div class="card"><h3>园区与离网站点</h3><p>电网薄弱或增容昂贵的园区、矿区、岛屿，用燃气空调解决夏季制冷。</p></div>
      <div class="card"><h3>油气田站场</h3><p>伴生气或天然气就地驱动，为值班室、控制室与生活区供冷供热。</p></div>
      <div class="card"><h3>数据中心与通信站</h3><p>对供电可靠性要求高，BHP 不占用电网容量，可做备用冷源。</p></div>
      <div class="card"><h3>酒店与商业</h3><p>天然气价格合适时，BHP 同时供冷与热水，降低夏季电费峰值。</p></div>
    </div>
  </div>
</section>
'''
    return page("zh", "solutions/bhp.html", "沼气源热泵空调 BHP 30–480 kW", "沼气源热泵空调 BHP：燃气发动机直驱压缩机，30–480 kW，不依赖电网制冷，可回收 60–90℃ 热水，适用于养殖场、食品厂、园区与油气田。", body)


def zh_biogas():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 解决方案 / 沼气发电与提纯</div>
    <span class="eyebrow">300 kW–2 MW · CH₄ ≥97%</span>
    <h1>沼气发电与生物天然气提纯</h1>
    <p class="lead">从池塘到母线，从原沼气到锅炉级燃气。沼气站是一条链，不是一台机器；机组进气质量决定两次大修之间是 8,000 小时还是 4,000 小时。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">工艺链</span><h2>六个环节，一套气质标准</h2></div>
    <div class="flow">
      <div class="step"><b>收集</b><span>覆盖塘或 CSTR，覆盖膜、冷凝水收集、集气总管。</span></div>
      <div class="step"><b>缓冲</b><span>储气柜吸收产气与用气波动。</span></div>
      <div class="step"><b>脱硫</b><span>生物脱硫塔 + 氧化铁精脱。</span></div>
      <div class="step"><b>净化</b><span>降温、除水除油，风机送至机组压力。</span></div>
      <div class="step"><b>发电</b><span>燃气机 + 发电机，孤岛或并网，余热回收。</span></div>
      <div class="step"><b>提纯</b><span>PSA / 水洗 / 膜分离，CH₄ ≥97%。</span></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">发电选型</span><h2>气量与机组容量</h2><p class="lead">60% 甲烷、38–40% 发电效率下，1 立方米沼气约可发 2.2 度电。长期低于 70% 负荷运行会积碳，宁可选小一号或拆成两台。</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>发电功率</th><th class="num">60% 甲烷所需气量</th><th class="num">55% 甲烷所需气量</th><th class="num">可回收热量</th></tr></thead>
        <tbody>
          <tr><td>300 kW</td><td class="num">132–140 Nm³/h</td><td class="num">144–153 Nm³/h</td><td class="num">330–390 kW</td></tr>
          <tr><td>500 kW</td><td class="num">220–234 Nm³/h</td><td class="num">240–255 Nm³/h</td><td class="num">550–650 kW</td></tr>
          <tr class="hl"><td>600 kW</td><td class="num">265–280 Nm³/h</td><td class="num">289–306 Nm³/h</td><td class="num">660–780 kW</td></tr>
          <tr><td>800 kW</td><td class="num">353–373 Nm³/h</td><td class="num">385–407 Nm³/h</td><td class="num">880–1,040 kW</td></tr>
          <tr><td>1,000 kW</td><td class="num">441–466 Nm³/h</td><td class="num">481–509 Nm³/h</td><td class="num">1,100–1,300 kW</td></tr>
          <tr><td>1,500 kW</td><td class="num">662–699 Nm³/h</td><td class="num">722–763 Nm³/h</td><td class="num">1,650–1,950 kW</td></tr>
          <tr><td>2,000 kW</td><td class="num">883–932 Nm³/h</td><td class="num">963–1,017 Nm³/h</td><td class="num">2,200–2,600 kW</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">满负荷参考值。机组进气要求：CH₄ ≥50%（设计 55–65%）、H₂S ≤200 ppm（目标 ≤100）、进气压力 5–15 kPa、温度 ≤40℃。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">提纯路线</span><h2>PSA、水洗、膜分离怎么选</h2><p class="lead">没有放之四海而皆准的答案，取决于气量、纯度要求、电价与场地。</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>路线</th><th>甲烷纯度</th><th>甲烷回收率</th><th>电耗</th><th>适用场景</th></tr></thead>
        <tbody>
          <tr><td><b>PSA</b></td><td>96–98%</td><td>95–98%</td><td>0.25–0.30 kWh/Nm³</td><td>200–1,500 Nm³/h，大型站</td></tr>
          <tr><td><b>水洗</b></td><td>97–99%</td><td>98–99%</td><td>0.20–0.30 kWh/Nm³</td><td>大中型、连续性气源</td></tr>
          <tr class="hl"><td><b>膜分离</b></td><td>96–98%</td><td>96–99%</td><td>0.20–0.28 kWh/Nm³</td><td>中小型、撬装、快速部署</td></tr>
        </tbody>
      </table>
    </div>
    <div class="split" style="margin-top:40px">
      <div>
        <h2 style="font-size:28px;margin-bottom:12px">500 Nm³/h 原气能出多少产品</h2>
        <ul class="checklist">
          <li>原沼气 500 Nm³/h @ 60% CH₄</li>
          <li>甲烷输入 300 Nm³/h，回收率 97%</li>
          <li>97% 甲烷产品 ≈300 Nm³/h</li>
          <li>产品热值 ≈2,890 kW（LHV），提纯电耗 ≈125–150 kW</li>
        </ul>
        <p class="note">保证气质：CH₄ ≥97%（可调 96–99%）、CO₂ ≤2–3%、H₂S ≤5 ppm、带压下露点 ≤−40℃、O₂ ≤0.5%。</p>
      </div>
      <div class="visual"><img src="assets/img/biogas/plant-02.jpg" alt="生物天然气提纯装置"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>沼气只发电，往往不是最优解</h2><p>如果现场有蒸汽、热水或车用燃料需求，提纯、热电联产与 BHP 组合，通常比单纯发电回本更快。</p></div>
      <div class="actions"><a class="btn light" href="contact.html">做一次气量与经济性测算</a></div>
    </div>
  </div>
</section>
'''
    return page("zh", "solutions/biogas.html", "沼气发电与生物天然气提纯", "沼气发电 300 kW–2 MW、生物天然气提纯 CH₄≥97%（PSA/水洗/膜分离），含气质标准、选型表与 500 Nm³/h 提纯示例。", body)


def zh_equipment():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 核心装备</div>
    <span class="eyebrow">撬装集成 · 出厂测试</span>
    <h1>核心装备与供货范围</h1>
    <p class="lead">重整撬、净化撬、PSA、燃料电池、余热回收与控制系统，在工厂内完成集成与跑合，到场接管、接电、接水即可调试。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g3">
      <article class="card prod-card"><img src="assets/img/huasen/assembly-skid.jpg" alt="重整制氢燃料电池机组撬装"><div class="body">
        <span class="tag">CHP SKID</span><h3>重整制氢 CHP 撬</h3><p>100–150 kW，含重整、变换、PSA、PEMFC、余热与控制。</p></div></article>
      <article class="card prod-card"><img src="assets/img/huasen/unit-10kw.jpg" alt="10 kW 级紧凑型机组"><div class="body">
        <span class="tag">COMPACT</span><h3>紧凑型 / 户用机型</h3><p>10 kW 级紧凑机组，占地小，适合户用、小商业与场地受限站点。</p></div></article>
      <article class="card prod-card"><img src="assets/img/huasen/inside-01.jpg" alt="机组内部集成"><div class="body">
        <span class="tag">INTEGRATION</span><h3>撬内集成</h3><p>管路、阀组、控制柜、消防与报警在厂内预制，减少现场焊接。</p></div></article>
      <article class="card prod-card"><img src="assets/img/bhp/bhp-unit.svg" alt="BHP 室外机" style="object-fit:contain;background:#f2f7f5;padding:14px"><div class="body">
        <span class="tag">BHP</span><h3>沼气源热泵空调</h3><p>30–480 kW 撬装室外机，发动机、压缩机、冷凝器与控制器一体。</p></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-01.jpg" alt="沼气发电机组"><div class="body">
        <span class="tag">GAS ENGINE</span><h3>沼气发电机组</h3><p>300 kW–2 MW，集装箱或撬装，孤岛 / 并网，余热回收。</p></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-02.jpg" alt="提纯撬"><div class="body">
        <span class="tag">UPGRADING</span><h3>提纯与净化撬</h3><p>脱硫、脱水、脱碳、增压，按气量与气质组合。</p></div></article>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">供货边界</span><h2>把“谁负责什么”写进合同</h2></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>范围</th><th>华森 / 制造基地</th><th>业主 / 第三方</th></tr></thead>
        <tbody>
          <tr><td>工艺设计与气量平衡</td><td>负责</td><td>提供气样与运行数据</td></tr>
          <tr><td>核心装备制造与集成</td><td>负责</td><td>—</td></tr>
          <tr><td>运输、安装指导、调试</td><td>负责</td><td>现场配合与吊装</td></tr>
          <tr><td>土建基础、站房</td><td>提资</td><td>负责</td></tr>
          <tr><td>外部燃气管线、并网审批</td><td>技术配合</td><td>负责</td></tr>
          <tr><td>运维托管</td><td>可选</td><td>按合同</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout" style="margin-top:22px"><b>出厂前：</b>撬内管路试压、气密、绝缘、控制逻辑与联锁在工厂完成；到场后主要工作是接管、接电、接水、通气与并网调试。</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div><span class="eyebrow">制造基地</span><h2 style="font-size:30px;margin:12px 0 14px">安徽海普克电气有限公司</h2>
        <p class="lead">位于安徽省宣城市泾县琴溪路 18 号，由皖南电机与京能电力共同投资。西门子 ICP 合格集成商，ISO 9001 / 14001 / 45001、IQNET 与 CE 认证，关键工序采用德国通快、瑞士金马与埃斯顿机器人设备。</p>
        <a class="btn ghost" href="about.html#base">看生产基地</a></div>
      <div class="visual"><img src="assets/img/hopco/workshop-01.jpg" alt="海普克生产车间"></div>
    </div>
  </div>
</section>
'''
    return page("zh", "equipment.html", "核心装备与供货范围", "重整制氢 CHP 撬、沼气源热泵空调、沼气发电机组、提纯净化撬；安徽海普克电气制造基地，西门子 ICP、ISO 三体系与 CE 认证。", body)


def zh_cases():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 案例与场景</div>
    <span class="eyebrow">示范项目 · 典型场景</span>
    <h1>案例与场景</h1>
    <p class="lead">我们更愿意把“已运行的”和“可复制的”分开讲。以下标注了项目状态，便于你判断哪些数据可以直接参考。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g2">
      <article class="card">
        <span class="num">示范项目 · 已获推荐</span>
        <h3>黑龙江宝泉岭寒区猪场沼气重整制氢 CHP</h3>
        <p>依托常年存栏 9,000 头以上规模化猪场，粪污厌氧发酵产沼气，配置 120–150 kW 热电联产机组。</p>
        <ul class="checklist" style="margin-top:14px">
          <li>年发电约 105–131 万 kWh，余热 150–250 kW</li>
          <li>余热回用发酵罐增温，最冷月需求 80–120 kW</li>
          <li>破解寒区沼气池冬季产气衰减 70–90% 的行业难题</li>
          <li>已获黑龙江省农业科学院推荐</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">典型场景 · 方案可复制</span>
        <h3>油田伴生气资源化</h3>
        <p>边远井、集输站与火炬气，过去常被放空或燃烧。净化后进入重整制氢 CHP，为站场供电、供热，替代柴油机。</p>
        <ul class="checklist" style="margin-top:14px">
          <li>气量 30–200 Nm³/h 可配单台或双台</li>
          <li>脱重烃、脱硫、脱水后进重整器</li>
          <li>孤岛运行，余热供值班室与生活区</li>
          <li>可结合碳资产开发核算减排</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">典型场景 · 园区能源站</span>
        <h3>城市天然气分布式冷热电联产</h3>
        <p>门站或园区天然气，经重整制氢进入燃料电池，电供楼宇，热水供生活与供暖，必要时配吸收制冷。</p>
        <ul class="checklist" style="margin-top:14px">
          <li>100–150 kW 模块化，按负荷分期投运</li>
          <li>低噪声，可布置在园区能源站或楼顶</li>
          <li>并网不上网 / 隔墙售电 / 自发自用</li>
          <li>与光伏、储能组成微能网</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">合作场景 · 东南亚棕榈油厂</span>
        <h3>POME 沼气发电、提纯与 BHP</h3>
        <p>棕榈油厂 POME 沼气气量大、连续性好，适合“发电 + 提纯 + 沼气空调”组合。合作制造体系在马来西亚已有 30 台机组、合计 16.4 MW 的运行业绩。</p>
        <ul class="checklist" style="margin-top:14px">
          <li>沼气发电 300 kW–2 MW</li>
          <li>提纯至 97% 供锅炉或 Bio-CNG</li>
          <li>BHP 解决厂区空调，不依赖电网</li>
          <li>余热回用厌氧池增温</li>
        </ul>
      </article>
    </div>
    <p class="table-note" style="margin-top:18px">“合作场景”中的机组业绩来自合作制造体系，非华森自有项目；具体项目边界与数据以合同及验收报告为准。</p>
  </div>
</section>
'''
    return page("zh", "cases.html", "案例与场景", "华森氢能案例：黑龙江宝泉岭寒区猪场沼气重整制氢 CHP 示范，油田伴生气、园区天然气与东南亚棕榈油厂 POME 沼气典型场景。", body)


def zh_about():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 关于华森</div>
    <span class="eyebrow">分布式氢能 · 装备成套 · 系统集成</span>
    <h1>关于安徽华森氢能源科技</h1>
    <p class="lead">把氢能从实验室和示范园区，带到有真实废弃物、有真实用能需求的乡镇与厂区。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">公司定位</span>
        <h2 style="font-size:32px;margin:12px 0 14px">一条主线，三件事</h2>
        <p class="lead">围绕“生物质 / 沼气 → 制氢 → 燃料电池发电 + 余热利用”，做装备成套、系统工程与投资运营。</p>
        <ul class="checklist">
          <li><b>装备成套：</b>重整制氢、PSA 提纯、燃料电池、余热回收集成为可搬运、可快速安装的撬装装置</li>
          <li><b>系统工程：</b>为养殖场、村镇、工业园区做“电、热、肥、气”多能互补微能网，含可研、申报、施工、调试</li>
          <li><b>投资运营：</b>以 EMC / EaaS 模式参与项目投资，与业主分享节能与能源收益</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/huasen/assembly-skid.jpg" alt="华森撬装式热电联产装置"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">技术与生态</span><h2>联合研发，国内制造</h2><p class="lead">核心工艺包与装备均为联合研发、国内制造，不依赖进口整机。</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>伙伴</th><th>合作内容</th></tr></thead>
        <tbody>
          <tr><td><b>中石化大连石油化工研究院</b></td><td>沼气 / 甲烷重整制氢工艺包、催化剂与系统设计</td></tr>
          <tr><td><b>西安热工院</b></td><td>超级碱性电解制氢、低温低压合成氨技术</td></tr>
          <tr><td><b>合肥远景常现</b></td><td>智慧微能网 AI 边缘计算与管控平台</td></tr>
          <tr><td><b>安徽海普克电气有限公司</b></td><td>燃料电池热电联供装置制造与成套</td></tr>
          <tr><td><b>黑龙江省农业科学院</b></td><td>寒区沼气 CHP 示范项目推荐与技术论证</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">技术团队由清华大学、天津大学、中科院大连化物所博士领衔，覆盖工艺包设计、装备集成、系统控制全链条。</p>
  </div>
</section>

<section class="section" id="base">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">生产基地</span>
      <h2>安徽海普克电气有限公司</h2>
      <p class="lead">燃料电池热电联供装置的制造与成套由海普克承担。海普克位于安徽省宣城市泾县琴溪路 18 号，由皖南电机与京能电力共同投资，2021 年 7 月投产。</p>
    </div>
    <div class="gallery">
      <figure class="wide"><img src="assets/img/hopco/workshop-01.jpg" alt="海普克钣金制造车间"><figcaption>钣金制造中心 · 德国通快高精度钣金加工设备</figcaption></figure>
      <figure><img src="assets/img/hopco/laser.jpg" alt="数控激光切割设备"><figcaption>数控激光切割</figcaption></figure>
      <figure><img src="assets/img/hopco/cnc.jpg" alt="数控冲床"><figcaption>数控冲床</figcaption></figure>
      <figure><img src="assets/img/hopco/bending-robot.jpg" alt="自动化折弯机器人工作站"><figcaption>自动化折弯机器人工作站</figcaption></figure>
      <figure><img src="assets/img/hopco/powder-coating.jpg" alt="自动喷粉涂装线"><figcaption>瑞士金马自动喷粉线</figcaption></figure>
      <figure><img src="assets/img/hopco/harness.jpg" alt="成套线束加工"><figcaption>成套线束加工中心</figcaption></figure>
      <figure><img src="assets/img/hopco/workshop-02.jpg" alt="海普克生产车间"><figcaption>成套制造车间</figcaption></figure>
    </div>
    <div class="grid g3" style="margin-top:26px">
      <div class="card"><h3>资质体系</h3><p>西门子 ICP 合格集成商；ISO 9001 质量、ISO 14001 环境、ISO 45001 职业健康安全、IQNET 与 CE 认证。</p></div>
      <div class="card"><h3>制造装备</h3><p>德国通快激光切割、数控冲床与折弯机，瑞士金马自动喷粉系统，埃斯顿机器人折弯与自动化线束设备。</p></div>
      <div class="card"><h3>质量边界</h3><p>从产品设计、钣金、涂装、成套到出厂测试的完整质量管理体系，关键工序可追溯。</p></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">合作模式</span><h2>四种做法，按你的边界选</h2></div>
    <div class="grid g4">
      <div class="card"><span class="num">01</span><h3>设备成套 / EPC</h3><p>提供撬装装备与工程设计、施工、调试，适合有预算、想自建自营的业主。</p></div>
      <div class="card"><span class="num">02</span><h3>EMC 合同能源管理</h3><p>我方投资建设，按节能/能源收益分成，合同期满设备无偿移交。</p></div>
      <div class="card"><span class="num">03</span><h3>EaaS 能源即服务</h3><p>按电、热、冷、肥的实际用量计费，适合用能波动大、想零投资的用户。</p></div>
      <div class="card"><span class="num">04</span><h3>咨询与申报</h3><p>可研编制、试点申报、政策对接、碳资产开发，适合地方政府与平台公司。</p></div>
    </div>
  </div>
</section>
'''
    return page("zh", "about.html", "关于华森与生产基地", "安徽华森氢能源科技：分布式氢能装备成套、系统集成与投资运营；生产基地安徽海普克电气，西门子 ICP、ISO 三体系与 CE 认证。", body)


def zh_contact():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">首页</a> / 联系我们</div>
    <span class="eyebrow">项目咨询 · 方案测算</span>
    <h1>把气源数据发给我们</h1>
    <p class="lead">有气源类型、流量、甲烷与硫化氢含量、用能负荷，我们就能给出机型、投资区间与回收期。没有实测数据也没关系，先做区间测算。</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-card">
        <h3>商务与技术咨询</h3>
        <div class="contact-line"><span class="k">联系人</span><span class="v">刘洋</span></div>
        <div class="contact-line"><span class="k">电话</span><span class="v"><a href="tel:+8613252949897">132 5294 9897</a><small>项目咨询、方案与报价</small></span></div>
        <div class="contact-line"><span class="k">公司</span><span class="v">安徽华森氢能源科技有限公司</span></div>
        <div class="contact-line"><span class="k">生产基地</span><span class="v">安徽海普克电气有限公司<small>安徽省宣城市泾县琴溪路 18 号</small></span></div>
        <div class="contact-line"><span class="k">基地电话</span><span class="v"><a href="tel:+8619565726668">195-6572-6668</a></span></div>
        <div class="contact-line"><span class="k">邮箱</span><span class="v"><a href="mailto:Hopco@hpkdq.com">Hopco@hpkdq.com</a></span></div>
        <p class="note" style="margin-top:16px">如需现场踏勘，请提前提供地址、气源类型与大致流量，我们安排工艺与电气工程师一同到场。</p>
      </div>
      <div class="contact-card">
        <h3>第一次沟通，准备这六项就够</h3>
        <ul class="checklist">
          <li>气源类型：沼气 / 煤层气 / 油田伴生气 / 天然气 / 生物天然气</li>
          <li>气量与气质：流量 Nm³/h、CH₄%、CO₂%、H₂S ppm</li>
          <li>用能需求：电负荷 kW、热水或蒸汽量、是否需要制冷</li>
          <li>运行方式：并网 / 孤岛 / 是否允许余电上网</li>
          <li>场地条件：可用面积、层高、与居民区距离</li>
          <li>项目阶段：可研、立项、招标或已具备场地</li>
        </ul>
        <div class="callout" style="margin-top:18px"><b>不确定气量？</b>把最近 1–2 周的流量计读数或沼气柜运行记录发来，我们可以先做区间估算。</div>
      </div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">合作方式</span><h2>从一次测算开始</h2></div>
    <div class="grid g4">
      <div class="card"><h3>预可研</h3><p>气量平衡、机型建议、投资与运维区间、回收期区间。基础资料齐全时免费。</p></div>
      <div class="card"><h3>技术方案</h3><p>P&amp;ID、总图、设备选型、电气与控制方案、正式报价。</p></div>
      <div class="card"><h3>工程交付</h3><p>供货、安装指导、调试、培训、并网配合与验收。</p></div>
      <div class="card"><h3>投资运营</h3><p>EMC / EaaS / BOO，按项目边界设计收益结构。</p></div>
    </div>
    <div class="cta-band" style="margin-top:36px">
      <div><h2>先算一遍，再决定怎么建</h2><p>我们的 CHP 与沼气计算器公开全部公式与假设，可以直接用来交叉核对供应商的数字。</p></div>
      <div class="actions"><a class="btn light" href="tools/">打开工程工具</a></div>
    </div>
  </div>
</section>
'''
    return page("zh", "contact.html", "联系我们", "安徽华森氢能源科技联系方式：商务咨询刘洋 132 5294 9897；生产基地安徽海普克电气，安徽省宣城市泾县琴溪路18号，195-6572-6668。", body)


# =====================================================================
# English pages
# =====================================================================

def en_home():
    body = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Distributed hydrogen · CCHP</span>
      <h1>Turn every cubic metre of gas<br>into <em>power, heat and cooling</em></h1>
      <p class="lead">Biogas, coal mine gas, oilfield associated gas and city natural gas are reformed on site into hydrogen for fuel-cell CHP. Biogas-driven heat-pump air conditioning completes the cooling side. One system, one party accountable from gas source to end use.</p>
      <div class="hero-actions">
        <a class="btn light" href="contact.html">Request a project study</a>
        <a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.3)" href="tools/">Open engineering tools</a>
      </div>
      <div class="hero-stats">
        <div><b>100–150 kW</b><span>per skid, factory-integrated</span></div>
        <div><b>≥40%</b><span>electrical efficiency (H₂ LHV)</span></div>
        <div><b>≥85%</b><span>combined heat and power efficiency</span></div>
        <div><b>≥8,000 h</b><span>design operating hours per year</span></div>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-card">
        <img src="assets/img/huasen/assembly-skid.jpg" alt="Skid-mounted methane reforming fuel-cell CHP unit">
        <div class="cap"><span>Reforming + fuel-cell CHP skid</span><span>100–150 kW</span></div>
      </div>
      <div class="hero-badge"><b>CHP ≥85%</b>power and heat in one pass</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Four gas sources, one route</span>
      <h2>Whatever gas you have, we build around it</h2>
      <p class="lead">We are not picky about the source — only about gas quality. First clean the gas to what the reformer accepts, then size hydrogen generation, power and heat recovery to your load.</p>
    </div>
    <div class="grid g4">
      <article class="card gas-card"><div class="ico">B</div><h3>Biogas</h3>
        <p>Livestock manure, food-processing wastewater, straw, landfill and palm oil mill POME.</p>
        <ul><li>CH₄ 50–65%</li><li>Desulphurisation, drying, pressure control</li><li>On-site use or grid parallel</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">C</div><h3>Coal mine gas / CBM</h3>
        <p>Underground extraction gas, gas pumping stations and mine gas power plants.</p>
        <ul><li>CH₄ 30–80%</li><li>Concentration or blending, fine desulphurisation</li><li>Power-led, heat for mine buildings</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">O</div><h3>Oilfield associated gas</h3>
        <p>Remote wells, gathering stations, vented and flared gas.</p>
        <ul><li>CH₄ 60–90%</li><li>Heavy hydrocarbon removal, drying</li><li>Replaces diesel gensets and flaring</li></ul>
      </article>
      <article class="card gas-card"><div class="ico">N</div><h3>City natural gas</h3>
        <p>City gate stations, industrial parks, hotels, hospitals and data centres.</p>
        <ul><li>CH₄ 90–99%</li><li>Pressure regulation, fine desulphurisation</li><li>Cooling, heating and power</li></ul>
      </article>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How the system works</span>
      <h2>Five steps from gas to cooling, heat and power</h2>
      <p class="lead">The core equipment is skid-mounted. On site you connect gas, power and water, then commission. Hydrogen is generated on demand and consumed inside the unit — no high-pressure hydrogen storage.</p>
    </div>
    <div class="flow">
      <div class="step"><b>Clean &amp; regulate</b><span>H₂S down to ≤20 ppm, drying, filtration and stable pressure.</span></div>
      <div class="step"><b>Reform</b><span>Steam methane reforming at 700–850℃: CH₄ + H₂O → H₂ + CO.</span></div>
      <div class="step"><b>Shift &amp; purify</b><span>Water-gas shift + PSA; product hydrogen ≥70%, CO &lt;10 ppm.</span></div>
      <div class="step"><b>Fuel cell</b><span>PEMFC electrochemical generation — no open flame, low noise.</span></div>
      <div class="step"><b>Heat recovery</b><span>40–50℃ hot water for digesters, space heating or domestic use.</span></div>
    </div>
    <div class="split" style="margin-top:46px">
      <div class="visual"><img src="assets/img/huasen/principle-system-en.png" alt="Methane reforming fuel-cell CHP process diagram"></div>
      <div>
        <h2 style="font-size:28px;margin-bottom:14px">Power and heat should be counted together</h2>
        <p class="lead">Electrical efficiency is ≥40%; most of the remainder is recovered as useful heat, giving ≥85% overall efficiency. For farms, oilfield stations and industrial parks, heat is often worth more than electricity.</p>
        <ul class="checklist">
          <li>Digester heating first — solves winter gas-output collapse in cold regions</li>
          <li>Hot water, steam and absorption cooling used in load order</li>
          <li>Grid parallel, island mode and black start available</li>
          <li>Modular parallel units, expand as gas volume grows</li>
        </ul>
        <a class="btn ghost" href="solutions/hydrogen-chp.html">See the technical detail</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Products</span><h2>Four product lines from gas to CCHP</h2></div>
    <div class="grid g4">
      <article class="card prod-card"><img src="assets/img/huasen/assembly-skid.jpg" alt="Reforming fuel-cell CHP unit"><div class="body">
        <span class="tag">CHP</span><h3>Reforming hydrogen CHP</h3><p>100–150 kW skid, power plus hot water, for biogas, mine gas, associated gas and natural gas.</p><a class="mini-link" href="solutions/hydrogen-chp.html">Models</a></div></article>
      <article class="card prod-card"><img src="assets/img/bhp/bhp-unit.svg" alt="Biogas heat-pump air conditioner" style="object-fit:contain;background:#f2f7f5;padding:14px"><div class="body">
        <span class="tag">BHP</span><h3>Biogas heat-pump air-con</h3><p>30–480 kW; gas engine drives the compressor directly, no grid power for cooling, with optional hot water.</p><a class="mini-link" href="solutions/bhp.html">Models</a></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-01.jpg" alt="Biogas power plant"><div class="body">
        <span class="tag">POWER</span><h3>Biogas gensets</h3><p>300 kW–2 MW, containerised or skid-mounted, island or grid parallel, with gas treatment and heat recovery.</p><a class="mini-link" href="solutions/biogas.html">Scope</a></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-02.jpg" alt="Biomethane upgrading unit"><div class="body">
        <span class="tag">UPGRADING</span><h3>Biomethane upgrading</h3><p>PSA, water scrubber or membrane; CH₄ ≥97% for boilers, vehicles or bio-CNG.</p><a class="mini-link" href="solutions/biogas.html">Process</a></div></article>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Why Huasen</span>
      <h2>Process package, equipment and site — one chain of responsibility</h2>
      <p class="lead">Reforming CHP is not a box of parts. Gas quality, catalyst, fuel cell, heat recovery and grid interface need one party accountable for the whole chain.</p>
    </div>
    <div class="grid g4">
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)"><h3 style="color:#fff">Process package</h3><p style="color:#b8ccc4">Reforming process, catalyst and system design developed with SINOPEC Dalian Research Institute of Petroleum and Petrochemicals.</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)"><h3 style="color:#fff">Manufacturing</h3><p style="color:#b8ccc4">Skid integration and packaging by Anhui Hopco Electric — Siemens ICP, ISO 9001/14001/45001 and CE.</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)"><h3 style="color:#fff">Engineering team</h3><p style="color:#b8ccc4">PhD-led team from Tsinghua, Tianjin and Dalian Institute of Chemical Physics, CAS across process, equipment and controls.</p></div>
      <div class="card" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)"><h3 style="color:#fff">Business models</h3><p style="color:#b8ccc4">Equipment / EPC, EMC shared savings, or EaaS — chosen to fit the owner’s balance sheet.</p></div>
    </div>
    <div class="stat-band" style="margin-top:30px;background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)">
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">1</b><span>system accountable for CCHP</span></div>
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">2</b><span>research institutes in co-development</span></div>
      <div style="border-color:rgba(255,255,255,.14)"><b style="color:#8fe0b8">3</b><span>universities in the core team</span></div>
      <div><b style="color:#8fe0b8">4</b><span>gas sources covered</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Reference &amp; scenarios</span>
        <h2 style="font-size:32px;margin:12px 0 14px">A cold-region pig farm, heated by its own CHP</h2>
        <p class="lead">Baiquanling, Heilongjiang: a pig farm with more than 9,000 head. Manure is digested to biogas and fed to a 120–150 kW reforming fuel-cell CHP unit.</p>
        <ul class="checklist">
          <li>About 1.05–1.31 million kWh generated per year; 150–250 kW of recoverable heat</li>
          <li>Heat returned to the digester; coldest-month demand 80–120 kW</li>
          <li>Solves the 70–90% winter gas-output drop typical of cold-region digesters</li>
          <li>Recommended by the Heilongjiang Academy of Agricultural Sciences</li>
        </ul>
        <a class="btn ghost" href="cases.html">More cases and scenarios</a>
      </div>
      <div class="visual"><img src="assets/img/biogas/plant-03.jpg" alt="Biogas plant site"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Send us your gas data</h2><p>Gas source, flow, methane and H₂S content, and load profile — with those we can size the unit and give an investment range and payback.</p></div>
      <div class="actions"><a class="btn light" href="contact.html">Contact Huasen</a><a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="tools/">Run the numbers first</a></div>
    </div>
  </div>
</section>
'''
    return page("en", "", "Anhui Huasen Hydrogen Energy — Distributed CCHP", "Anhui Huasen Hydrogen Energy: methane reforming hydrogen CHP for biogas, coal mine gas, oilfield associated gas and city natural gas; biogas-driven heat-pump air conditioning (BHP); distributed CCHP solutions.", body)


def en_chp():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Solutions / H₂ CHP</div>
    <span class="eyebrow">100–150 kW · skid-mounted</span>
    <h1>Methane reforming · fuel-cell CHP</h1>
    <p class="lead">Turn biogas, coal mine gas, associated gas or city natural gas into power and hot water on site. ≥40% electrical efficiency, ≥85% overall, ≥8,000 operating hours a year.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split img-right">
      <div>
        <span class="eyebrow">Process</span>
        <h2 style="font-size:30px;margin:12px 0 14px">No hydrogen storage — made and used on demand</h2>
        <p class="lead">Clean gas enters the reformer to produce hydrogen-rich syngas, then shift and PSA bring it to fuel-cell quality. Hydrogen is not bottled or stored at pressure; it is consumed inside the unit as it is made.</p>
        <ul class="checklist">
          <li>Inlet limits: H₂S ≤20 ppm, CO₂ ≤20% (higher CO₂ needs front-end removal)</li>
          <li>Product hydrogen ≥70%, CO &lt;10 ppm</li>
          <li>PEMFC generation with 40–50℃ hot-water recovery</li>
          <li>Grid parallel, island mode and black start available</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/huasen/principle-fuelcell-en.png" alt="Fuel-cell CHP principle"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Gas compatibility</span><h2>Four sources, four pre-treatment priorities</h2><p class="lead">One reformer and fuel-cell platform; the front end changes with the gas. Gas analysis is the first step of selection — and the boundary of the warranty.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Gas source</th><th>Typical CH₄</th><th>Front-end treatment</th><th>Typical use</th></tr></thead>
        <tbody>
          <tr><td><b>Biogas</b></td><td>50–65%</td><td>H₂S to ≤20 ppm, drying, filtration; CO₂ removal if high</td><td>Livestock, food wastewater, straw, landfill, POME</td></tr>
          <tr><td><b>Coal mine gas</b></td><td>30–80%</td><td>Concentration or blending, fine desulphurisation, drying, pressure control</td><td>Mine extraction gas, pumping stations, gas power plants</td></tr>
          <tr><td><b>Associated gas</b></td><td>60–90%</td><td>Heavy hydrocarbon removal, desulphurisation, drying</td><td>Remote wells, gathering stations, vented/flared gas</td></tr>
          <tr><td><b>City natural gas</b></td><td>90–99%</td><td>Pressure regulation, fine desulphurisation (incl. odorant), filtration</td><td>City gates, parks, hotels, hospitals, data centres</td></tr>
          <tr><td><b>Biomethane / CNG (extended)</b></td><td>96–99%</td><td>Let-down, regulation, filtration</td><td>Sites without pipeline, bottled or trucked gas</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">Below 30% CH₄, coal mine gas needs concentration or blending with natural gas. The exact boundary is confirmed case by case from gas analysis and flow.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Models</span><h2>Three standard units, sized by gas and load</h2><p class="lead">Electrical efficiency ≥40% on hydrogen LHV; recoverable heat estimated at about 45% of fuel input. Multiple units parallel to several hundred kW.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Model</th><th class="num">Power</th><th class="num">Fuel input</th><th class="num">Pure CH₄</th><th class="num">60% biogas</th><th class="num">Recoverable heat</th></tr></thead>
        <tbody>
          <tr><td><b>HS-CHP-100</b></td><td class="num">100 kW</td><td class="num">250 kW</td><td class="num">25.2 Nm³/h</td><td class="num">41.9 Nm³/h</td><td class="num">≈112 kW</td></tr>
          <tr class="hl"><td><b>HS-CHP-120</b></td><td class="num">120 kW</td><td class="num">300 kW</td><td class="num">30.2 Nm³/h</td><td class="num">50.3 Nm³/h</td><td class="num">≈135 kW</td></tr>
          <tr><td><b>HS-CHP-150</b></td><td class="num">150 kW</td><td class="num">375 kW</td><td class="num">37.7 Nm³/h</td><td class="num">62.9 Nm³/h</td><td class="num">≈169 kW</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">Basis: methane LHV 9.94 kWh/Nm³, 40% electrical efficiency, 45% heat recovery. Actual values depend on gas analysis, ambient conditions and the manufacturer’s guarantee. Hot water 40–50℃, upgradeable or used for absorption cooling.</p>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Operation</span><h2>No engine, no open flame</h2><p class="lead">A fuel cell generates electrochemically rather than by combustion. For residential areas, farms, oilfield stations and industrial parks that means lower noise and simpler emission control.</p></div>
    <div class="grid g3">
      <div class="card"><h3>Low noise</h3><p>The main moving parts are fans and pumps; about 55 dB(A) at 1 m, so the unit can sit next to a site office or dormitory.</p></div>
      <div class="card"><h3>Low emissions</h3><p>No high-temperature flame; NOx, SOx and particulate emissions are very low. Gas is desulphurised upstream, so sulphur does not enter the process.</p></div>
      <div class="card"><h3>Process water</h3><p>The fuel-cell reaction produces water that can be recovered for washing or irrigation. No waste oil and no black smoke.</p></div>
      <div class="card"><h3>Load following</h3><p>Output tracks the electrical load; when gas is short the unit reduces power instead of cycling on and off.</p></div>
      <div class="card"><h3>Unattended</h3><p>PLC plus remote monitoring, alarms on key parameters, optional remote diagnostics and O&amp;M.</p></div>
      <div class="card"><h3>Modular growth</h3><p>100–150 kW per unit, parallel operation. Start with one and add as gas volume increases.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Scope</span>
        <h2 style="font-size:30px;margin:12px 0 14px">What we supply — and what we do not</h2>
        <p class="lead">A clear boundary is the cheapest risk control in a gas project.</p>
        <ul class="checklist">
          <li>Supply: gas treatment skid, reformer, PSA, fuel cell, heat recovery, control cabinet and interconnecting piping</li>
          <li>Services: gas analysis, process design, installation supervision, commissioning, training, O&amp;M</li>
          <li>Excluded: civil works, external gas pipeline, grid connection approval, owner-side electrical works</li>
          <li>Optional: grid interface panel, black start, absorption cooling, remote monitoring</li>
        </ul>
        <a class="btn" href="contact.html">Request technical agreement and quotation</a>
      </div>
      <div class="visual"><img src="assets/img/huasen/inside-01.jpg" alt="Inside the CHP unit"></div>
    </div>
  </div>
</section>
'''
    return page("en", "solutions/hydrogen-chp.html", "Reforming hydrogen CHP, 100–150 kW", "Methane reforming hydrogen fuel-cell CHP for biogas, coal mine gas, oilfield associated gas and city natural gas. ≥40% electrical, ≥85% overall, 100–150 kW skid-mounted.", body)


def en_bhp():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Solutions / BHP air-con</div>
    <span class="eyebrow">30–480 kW · engine-driven</span>
    <h1>Biogas heat-pump air conditioning (BHP)</h1>
    <p class="lead">When the boiler stops, the air conditioning keeps running. A small gas engine drives the compressor directly; the fuel is biogas or biomethane, and there is no electric motor in the drive train.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split img-right">
      <div>
        <span class="eyebrow">Why it matters</span>
        <h2 style="font-size:30px;margin:12px 0 14px">Break the boiler–turbine–grid dependency</h2>
        <p class="lead">On farms, biogas plants, food factories and industrial parks, cooling often hangs on one chain: boiler stops, turbine stops, site power gets tight, and offices and dormitories lose cooling first. BHP cuts that chain.</p>
        <ul class="checklist">
          <li>Gas engine drives an open compressor — no generator, no electric motor</li>
          <li>30–480 kW per unit, up to 8 units in parallel to MW scale</li>
          <li>97% methane at 5–20 kPa; H₂S &lt;10 ppm</li>
          <li>Optional engine heat recovery to 60–90℃ hot water</li>
          <li>Skid-mounted outdoor unit, ground or roof, no plant room</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/bhp/bhp-unit.svg" alt="BHP outdoor unit" style="background:#f2f7f5;padding:18px"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Principle</span><h2>Gas in, cooling out — and hot water too</h2><p class="lead">This is not an absorption chiller. The engine does mechanical work on the compressor, so one cubic metre of methane yields about 10 kWh of cooling — roughly 50% more than a single-effect absorption unit on the same gas.</p></div>
    <div class="split">
      <div class="visual"><img src="assets/img/bhp/bhp-principle-en.svg" alt="BHP working principle" style="background:#fff;padding:14px"></div>
      <div>
        <div class="flow" style="grid-template-columns:1fr 1fr">
          <div class="step"><b>Gas inlet</b><span>97% methane at 5–20 kPa, filtered and regulated.</span></div>
          <div class="step"><b>Engine</b><span>Spark-ignition gas engine, shaft output via coupling or belt.</span></div>
          <div class="step"><b>Compression</b><span>Open reciprocating or scroll compressor; speed and unloading control capacity.</span></div>
          <div class="step"><b>Heat recovery</b><span>Jacket water and exhaust heat to 60–90℃ hot water.</span></div>
        </div>
        <div class="callout" style="margin-top:20px"><b>COP basis:</b> about 1.0 on gas LHV. On an electricity-equivalent basis the compressor itself is about COP 3.0 — what changes is where the shaft power comes from, not the cooling efficiency.</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Models</span><h2>Five nominal sizes, 30 to 480 kW</h2><p class="lead">Fuel input at rated cooling and gas COP 1.0; recoverable heat is engine heat in cooling mode, with 50 K hot-water rise.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Model</th><th class="num">Cooling</th><th class="num">Gas input</th><th class="num">97% CH₄</th><th class="num">Recoverable heat</th><th class="num">Hot water, 50 K</th></tr></thead>
        <tbody>
          <tr><td><b>BHP-30</b></td><td class="num">30 kW</td><td class="num">30.0 kW</td><td class="num">3.0 Nm³/h</td><td class="num">7.5 kW</td><td class="num">129 L/h</td></tr>
          <tr><td><b>BHP-60</b></td><td class="num">60 kW</td><td class="num">60.0 kW</td><td class="num">6.0 Nm³/h</td><td class="num">15.0 kW</td><td class="num">258 L/h</td></tr>
          <tr class="hl"><td><b>BHP-120</b></td><td class="num">120 kW</td><td class="num">120.0 kW</td><td class="num">12.1 Nm³/h</td><td class="num">30.0 kW</td><td class="num">517 L/h</td></tr>
          <tr><td><b>BHP-240</b></td><td class="num">240 kW</td><td class="num">240.0 kW</td><td class="num">24.1 Nm³/h</td><td class="num">60.0 kW</td><td class="num">1,034 L/h</td></tr>
          <tr><td><b>BHP-480</b></td><td class="num">480 kW</td><td class="num">480.0 kW</td><td class="num">48.3 Nm³/h</td><td class="num">120.0 kW</td><td class="num">2,069 L/h</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">Larger loads use multiple units in parallel. Performance figures are indicative and confirmed by the manufacturer’s guarantee and site gas analysis. Raw biogas must first be upgraded to 97% methane or treated by a front-end module.</p>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Applications</span><h2>Where BHP fits best</h2></div>
    <div class="grid g3">
      <div class="card"><h3>Farms and biogas plants</h3><p>Cool offices, dormitories and laboratories with own biogas; recover heat for the digester or domestic hot water.</p></div>
      <div class="card"><h3>Food processing</h3><p>Slaughterhouses, breweries and produce plants with steady biogas and cooling demand; replaces electric air-con and diesel sets.</p></div>
      <div class="card"><h3>Parks and off-grid sites</h3><p>Weak grids or expensive capacity upgrades; gas cooling solves summer demand without adding electrical load.</p></div>
      <div class="card"><h3>Oil and gas stations</h3><p>Associated or natural gas drives cooling and heating for control rooms, offices and living quarters.</p></div>
      <div class="card"><h3>Data and telecom sites</h3><p>High reliability requirement; BHP does not use grid capacity and can serve as backup cooling.</p></div>
      <div class="card"><h3>Hotels and commercial</h3><p>With the right gas price, BHP provides cooling and hot water and cuts summer electricity peaks.</p></div>
    </div>
  </div>
</section>
'''
    return page("en", "solutions/bhp.html", "Biogas heat-pump air conditioning, 30–480 kW", "BHP biogas-driven heat-pump air conditioning: gas engine drives the compressor, 30–480 kW, no grid power for cooling, optional 60–90℃ hot water.", body)


def en_biogas():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Solutions / Biogas power</div>
    <span class="eyebrow">300 kW–2 MW · CH₄ ≥97%</span>
    <h1>Biogas power and biomethane upgrading</h1>
    <p class="lead">From pond to busbar, from raw biogas to boiler-grade gas. A biogas plant is a chain, not a machine; inlet gas quality decides whether you get 8,000 hours or 4,000 hours between overhauls.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Process chain</span><h2>Six steps, one gas specification</h2></div>
    <div class="flow">
      <div class="step"><b>Collection</b><span>Covered pond or CSTR, cover membrane, condensate collection, gas header.</span></div>
      <div class="step"><b>Buffer</b><span>Gas holder absorbs production and demand swings.</span></div>
      <div class="step"><b>Desulphurisation</b><span>Biological tower plus iron-oxide polishing.</span></div>
      <div class="step"><b>Conditioning</b><span>Cooling, water and oil removal, boost to engine pressure.</span></div>
      <div class="step"><b>Power</b><span>Gas engine and generator, island or grid parallel, heat recovery.</span></div>
      <div class="step"><b>Upgrading</b><span>PSA, water scrubber or membrane to CH₄ ≥97%.</span></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Sizing</span><h2>Gas volume and engine capacity</h2><p class="lead">At 60% methane and 38–40% electrical efficiency, one cubic metre of biogas yields about 2.2 kWh. Running below 70% load for long periods causes carbon build-up; choose a smaller unit or split into two.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Power</th><th class="num">Gas at 60% CH₄</th><th class="num">Gas at 55% CH₄</th><th class="num">Recoverable heat</th></tr></thead>
        <tbody>
          <tr><td>300 kW</td><td class="num">132–140 Nm³/h</td><td class="num">144–153 Nm³/h</td><td class="num">330–390 kW</td></tr>
          <tr><td>500 kW</td><td class="num">220–234 Nm³/h</td><td class="num">240–255 Nm³/h</td><td class="num">550–650 kW</td></tr>
          <tr class="hl"><td>600 kW</td><td class="num">265–280 Nm³/h</td><td class="num">289–306 Nm³/h</td><td class="num">660–780 kW</td></tr>
          <tr><td>800 kW</td><td class="num">353–373 Nm³/h</td><td class="num">385–407 Nm³/h</td><td class="num">880–1,040 kW</td></tr>
          <tr><td>1,000 kW</td><td class="num">441–466 Nm³/h</td><td class="num">481–509 Nm³/h</td><td class="num">1,100–1,300 kW</td></tr>
          <tr><td>1,500 kW</td><td class="num">662–699 Nm³/h</td><td class="num">722–763 Nm³/h</td><td class="num">1,650–1,950 kW</td></tr>
          <tr><td>2,000 kW</td><td class="num">883–932 Nm³/h</td><td class="num">963–1,017 Nm³/h</td><td class="num">2,200–2,600 kW</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">Full-load reference values. Engine inlet: CH₄ ≥50% (design 55–65%), H₂S ≤200 ppm (target ≤100), pressure 5–15 kPa, temperature ≤40℃.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Upgrading routes</span><h2>PSA, water scrubber or membrane?</h2><p class="lead">No universal answer — it depends on gas volume, purity, electricity price and footprint.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Route</th><th>CH₄ purity</th><th>CH₄ recovery</th><th>Power</th><th>Best fit</th></tr></thead>
        <tbody>
          <tr><td><b>PSA</b></td><td>96–98%</td><td>95–98%</td><td>0.25–0.30 kWh/Nm³</td><td>200–1,500 Nm³/h, large plants</td></tr>
          <tr><td><b>Water scrubber</b></td><td>97–99%</td><td>98–99%</td><td>0.20–0.30 kWh/Nm³</td><td>Medium-large, continuous gas</td></tr>
          <tr class="hl"><td><b>Membrane</b></td><td>96–98%</td><td>96–99%</td><td>0.20–0.28 kWh/Nm³</td><td>Small-medium, skid-mounted, fast deployment</td></tr>
        </tbody>
      </table>
    </div>
    <div class="split" style="margin-top:40px">
      <div>
        <h2 style="font-size:28px;margin-bottom:12px">What 500 Nm³/h of raw gas yields</h2>
        <ul class="checklist">
          <li>Raw biogas 500 Nm³/h at 60% CH₄</li>
          <li>Methane input 300 Nm³/h, 97% recovery</li>
          <li>97% methane product ≈300 Nm³/h</li>
          <li>Product heat ≈2,890 kW (LHV); upgrading power ≈125–150 kW</li>
        </ul>
        <p class="note">Guaranteed gas: CH₄ ≥97% (adjustable 96–99%), CO₂ ≤2–3%, H₂S ≤5 ppm, pressurised dew point ≤−40℃, O₂ ≤0.5%.</p>
      </div>
      <div class="visual"><img src="assets/img/biogas/plant-02.jpg" alt="Biomethane upgrading unit"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Power-only is rarely the best answer</h2><p>If the site also needs steam, hot water or vehicle fuel, upgrading, CHP and BHP combined often pay back faster than power alone.</p></div>
      <div class="actions"><a class="btn light" href="contact.html">Run a gas and economics study</a></div>
    </div>
  </div>
</section>
'''
    return page("en", "solutions/biogas.html", "Biogas power and biomethane upgrading", "Biogas power 300 kW–2 MW and biomethane upgrading to CH₄≥97% by PSA, water scrubber or membrane, with gas specification, sizing tables and a 500 Nm³/h example.", body)


def en_equipment():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Equipment</div>
    <span class="eyebrow">Skid integration · factory tested</span>
    <h1>Core equipment and supply scope</h1>
    <p class="lead">Reformer, gas treatment, PSA, fuel cell, heat recovery and controls are integrated and run-tested in the factory. On site you connect gas, power and water, then commission.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g3">
      <article class="card prod-card"><img src="assets/img/huasen/assembly-skid.jpg" alt="Reforming fuel-cell CHP unit"><div class="body"><span class="tag">CHP SKID</span><h3>Reforming CHP skid</h3><p>100–150 kW, including reformer, shift, PSA, PEMFC, heat recovery and controls.</p></div></article>
      <article class="card prod-card"><img src="assets/img/huasen/unit-compact.jpg" alt="Compact unit"><div class="body"><span class="tag">COMPACT</span><h3>Compact unit</h3><p>Small footprint for constrained farms, stations and park plant rooms.</p></div></article>
      <article class="card prod-card"><img src="assets/img/huasen/inside-01.jpg" alt="Skid internals"><div class="body"><span class="tag">INTEGRATION</span><h3>Skid integration</h3><p>Piping, valves, control cabinet, fire and alarm pre-built in the factory to cut site welding.</p></div></article>
      <article class="card prod-card"><img src="assets/img/bhp/bhp-unit.svg" alt="BHP outdoor unit" style="object-fit:contain;background:#f2f7f5;padding:14px"><div class="body"><span class="tag">BHP</span><h3>Biogas heat-pump air-con</h3><p>30–480 kW outdoor skid with engine, compressor, condenser and controls in one frame.</p></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-01.jpg" alt="Biogas genset"><div class="body"><span class="tag">GAS ENGINE</span><h3>Biogas gensets</h3><p>300 kW–2 MW, containerised or skid-mounted, island or grid parallel, heat recovery.</p></div></article>
      <article class="card prod-card"><img src="assets/img/biogas/plant-02.jpg" alt="Upgrading skid"><div class="body"><span class="tag">UPGRADING</span><h3>Treatment and upgrading skids</h3><p>Desulphurisation, drying, CO₂ removal and boosting, combined to gas volume and quality.</p></div></article>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Scope</span><h2>Put “who does what” in the contract</h2></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Scope</th><th>Huasen / manufacturing base</th><th>Owner / third party</th></tr></thead>
        <tbody>
          <tr><td>Process design and gas balance</td><td>Responsible</td><td>Provide gas sample and operating data</td></tr>
          <tr><td>Core equipment manufacturing and integration</td><td>Responsible</td><td>—</td></tr>
          <tr><td>Transport, installation supervision, commissioning</td><td>Responsible</td><td>Site support and lifting</td></tr>
          <tr><td>Civil foundation and plant room</td><td>Provide loads and drawings</td><td>Responsible</td></tr>
          <tr><td>External gas pipeline and grid approval</td><td>Technical support</td><td>Responsible</td></tr>
          <tr><td>O&amp;M</td><td>Optional</td><td>Per contract</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout" style="margin-top:22px"><b>Before dispatch:</b> pressure test, gas tightness, insulation, control logic and interlocks are completed in the factory. On site the main work is connecting gas, power and water, then commissioning and grid synchronisation.</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div><span class="eyebrow">Manufacturing base</span><h2 style="font-size:30px;margin:12px 0 14px">Anhui Hopco Electric Co., Ltd.</h2>
        <p class="lead">No. 18 Qinxi Road, Jing County, Xuancheng, Anhui, jointly invested by Wannan Motor and Jingneng Power. Siemens ICP qualified integrator; ISO 9001 / 14001 / 45001, IQNET and CE; TRUMPF, GEMA and ESTUN equipment on key processes.</p>
        <a class="btn ghost" href="about.html#base">See the production base</a></div>
      <div class="visual"><img src="assets/img/hopco/workshop-01.jpg" alt="Hopco workshop"></div>
    </div>
  </div>
</section>
'''
    return page("en", "equipment.html", "Core equipment and supply scope", "Reforming CHP skids, BHP biogas heat-pump air conditioning, biogas gensets and upgrading skids, manufactured at Anhui Hopco Electric with Siemens ICP, ISO and CE certification.", body)


def en_cases():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Cases</div>
    <span class="eyebrow">Demonstration · replicable scenarios</span>
    <h1>Cases and scenarios</h1>
    <p class="lead">We separate what is already running from what is replicable, so you can judge which numbers apply to your project.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g2">
      <article class="card">
        <span class="num">DEMONSTRATION · RECOMMENDED</span>
        <h3>Cold-region pig farm biogas reforming CHP, Baiquanling</h3>
        <p>A pig farm with more than 9,000 head in Heilongjiang. Manure is digested to biogas and fed to a 120–150 kW CHP unit.</p>
        <ul class="checklist" style="margin-top:14px">
          <li>About 1.05–1.31 million kWh per year; 150–250 kW recoverable heat</li>
          <li>Heat returned to the digester; 80–120 kW needed in the coldest month</li>
          <li>Solves the 70–90% winter gas-output drop in cold-region digesters</li>
          <li>Recommended by the Heilongjiang Academy of Agricultural Sciences</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">SCENARIO · REPLICABLE</span>
        <h3>Oilfield associated gas utilisation</h3>
        <p>Remote wells, gathering stations and flare gas that were vented or burned. After treatment the gas feeds reforming CHP for site power and heat, replacing diesel gensets.</p>
        <ul class="checklist" style="margin-top:14px">
          <li>30–200 Nm³/h, one or two units</li>
          <li>Heavy hydrocarbon, sulphur and water removal before the reformer</li>
          <li>Island operation; heat for control rooms and living quarters</li>
          <li>Can be combined with carbon-asset accounting</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">SCENARIO · PARK ENERGY STATION</span>
        <h3>City natural gas distributed CCHP</h3>
        <p>City gate or park natural gas is reformed to hydrogen for the fuel cell. Power serves buildings, hot water serves domestic and heating loads, with absorption cooling where needed.</p>
        <ul class="checklist" style="margin-top:14px">
          <li>100–150 kW modular, staged with load growth</li>
          <li>Low noise; suitable for park energy stations or rooftops</li>
          <li>Grid parallel without export, behind-the-meter or self-consumption</li>
          <li>Can form a microgrid with PV and storage</li>
        </ul>
      </article>
      <article class="card">
        <span class="num">PARTNER SCENARIO · SOUTHEAST ASIA</span>
        <h3>POME biogas power, upgrading and BHP</h3>
        <p>Palm oil mill POME offers large, continuous biogas volume — a good fit for power, upgrading and biogas air conditioning together. The partner manufacturing system has 30 units / 16.4 MW operating in Malaysia.</p>
        <ul class="checklist" style="margin-top:14px">
          <li>Biogas power 300 kW–2 MW</li>
          <li>Upgrading to 97% for boilers or bio-CNG</li>
          <li>BHP for site cooling without grid demand</li>
          <li>Heat returned to the anaerobic pond</li>
        </ul>
      </article>
    </div>
    <p class="table-note" style="margin-top:18px">Unit references in the partner scenario come from the partner manufacturing system, not from Huasen-owned projects. Project boundaries and figures are subject to contract and acceptance reports.</p>
  </div>
</section>
'''
    return page("en", "cases.html", "Cases and scenarios", "Huasen Hydrogen cases: cold-region pig farm biogas reforming CHP demonstration in Heilongjiang, plus oilfield associated gas, park natural gas and Southeast Asian POME biogas scenarios.", body)


def en_about():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / About</div>
    <span class="eyebrow">Distributed hydrogen · equipment · integration</span>
    <h1>About Anhui Huasen Hydrogen Energy</h1>
    <p class="lead">Taking hydrogen out of laboratories and demonstration parks, into towns and factories that have real waste and real energy demand.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow">Positioning</span>
        <h2 style="font-size:32px;margin:12px 0 14px">One thread, three businesses</h2>
        <p class="lead">Around “biomass / biogas → hydrogen → fuel-cell power + heat recovery”, we do equipment packaging, system engineering and project investment.</p>
        <ul class="checklist">
          <li><b>Equipment:</b> reforming, PSA, fuel cell and heat recovery integrated into movable, fast-install skids</li>
          <li><b>System engineering:</b> multi-energy microgrids for farms, villages and industrial parks — feasibility, applications, construction and commissioning</li>
          <li><b>Investment:</b> EMC / EaaS participation, sharing energy savings and revenue with the owner</li>
        </ul>
      </div>
      <div class="visual"><img src="assets/img/huasen/assembly-skid.jpg" alt="Huasen skid-mounted CHP unit"></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Technology and partners</span><h2>Co-developed, made in China</h2><p class="lead">Core process packages and equipment are co-developed and manufactured domestically, without reliance on imported complete units.</p></div>
    <div class="table-wrap">
      <table class="data">
        <thead><tr><th>Partner</th><th>Scope</th></tr></thead>
        <tbody>
          <tr><td><b>SINOPEC Dalian Research Institute of Petroleum and Petrochemicals</b></td><td>Biogas / methane reforming process package, catalyst and system design</td></tr>
          <tr><td><b>Xi’an Thermal Power Research Institute</b></td><td>Advanced alkaline electrolysis and low-pressure ammonia synthesis</td></tr>
          <tr><td><b>Hefei Yuanjing Changxian</b></td><td>AI edge computing and control platform for smart microgrids</td></tr>
          <tr><td><b>Anhui Hopco Electric Co., Ltd.</b></td><td>Manufacturing and packaging of fuel-cell CHP units</td></tr>
          <tr><td><b>Heilongjiang Academy of Agricultural Sciences</b></td><td>Recommendation and technical review for cold-region biogas CHP demonstration</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">The technical team is led by PhDs from Tsinghua University, Tianjin University and Dalian Institute of Chemical Physics, CAS, covering process design, equipment integration and control.</p>
  </div>
</section>

<section class="section" id="base">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Manufacturing base</span>
      <h2>Anhui Hopco Electric Co., Ltd.</h2>
      <p class="lead">Fuel-cell CHP units are manufactured and packaged by Hopco at No. 18 Qinxi Road, Jing County, Xuancheng, Anhui. Jointly invested by Wannan Motor and Jingneng Power, in production since July 2021.</p>
    </div>
    <div class="gallery">
      <figure class="wide"><img src="assets/img/hopco/workshop-01.jpg" alt="Hopco sheet-metal workshop"><figcaption>Sheet-metal centre · TRUMPF high-precision equipment</figcaption></figure>
      <figure><img src="assets/img/hopco/laser.jpg" alt="CNC laser cutting"><figcaption>CNC laser cutting</figcaption></figure>
      <figure><img src="assets/img/hopco/cnc.jpg" alt="CNC punch"><figcaption>CNC punch</figcaption></figure>
      <figure><img src="assets/img/hopco/bending-robot.jpg" alt="Robotic bending cell"><figcaption>Robotic bending cell</figcaption></figure>
      <figure><img src="assets/img/hopco/powder-coating.jpg" alt="Automatic powder coating line"><figcaption>GEMA automatic powder line</figcaption></figure>
      <figure><img src="assets/img/hopco/harness.jpg" alt="Wire harness workshop"><figcaption>Wire harness centre</figcaption></figure>
      <figure><img src="assets/img/hopco/workshop-02.jpg" alt="Hopco assembly workshop"><figcaption>Assembly workshop</figcaption></figure>
    </div>
    <div class="grid g3" style="margin-top:26px">
      <div class="card"><h3>Certification</h3><p>Siemens ICP qualified integrator; ISO 9001 quality, ISO 14001 environment, ISO 45001 occupational health and safety, IQNET and CE.</p></div>
      <div class="card"><h3>Equipment</h3><p>TRUMPF laser cutting, CNC punching and bending, GEMA automatic powder coating, ESTUN robotic bending and automated harness machines.</p></div>
      <div class="card"><h3>Quality boundary</h3><p>A complete quality system from design, sheet metal and coating to assembly and factory testing, with traceability on key processes.</p></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Business models</span><h2>Four ways to work with us</h2></div>
    <div class="grid g4">
      <div class="card"><span class="num">01</span><h3>Equipment / EPC</h3><p>Skid supply plus engineering, construction and commissioning for owners who want to build and operate themselves.</p></div>
      <div class="card"><span class="num">02</span><h3>EMC shared savings</h3><p>We invest and build, share the energy savings, and transfer the equipment at the end of the contract.</p></div>
      <div class="card"><span class="num">03</span><h3>EaaS</h3><p>Pay per kWh of power, heat, cooling or fertiliser — for users with fluctuating demand and no capex appetite.</p></div>
      <div class="card"><span class="num">04</span><h3>Consulting</h3><p>Feasibility studies, pilot applications, policy alignment and carbon-asset development for governments and platforms.</p></div>
    </div>
  </div>
</section>
'''
    return page("en", "about.html", "About Huasen and the manufacturing base", "Anhui Huasen Hydrogen Energy: distributed hydrogen equipment, system integration and investment; manufacturing base Anhui Hopco Electric with Siemens ICP, ISO and CE certification.", body)


def en_contact():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="index.html" style="color:#9fc0b4">Home</a> / Contact</div>
    <span class="eyebrow">Project enquiry · feasibility</span>
    <h1>Send us your gas data</h1>
    <p class="lead">With gas source, flow, methane and H₂S content and load profile, we can size the unit and give an investment range and payback. No measured data yet? We can start with a range.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-card">
        <h3>Sales and technical enquiry</h3>
        <div class="contact-line"><span class="k">Contact</span><span class="v">Liu Yang</span></div>
        <div class="contact-line"><span class="k">Phone</span><span class="v"><a href="tel:+8613252949897">+86 132 5294 9897</a><small>Project enquiry, scheme and quotation</small></span></div>
        <div class="contact-line"><span class="k">Company</span><span class="v">Anhui Huasen Hydrogen Energy Technology Co., Ltd.</span></div>
        <div class="contact-line"><span class="k">Base</span><span class="v">Anhui Hopco Electric Co., Ltd.<small>No. 18 Qinxi Road, Jing County, Xuancheng, Anhui, China</small></span></div>
        <div class="contact-line"><span class="k">Base phone</span><span class="v"><a href="tel:+8619565726668">+86 195-6572-6668</a></span></div>
        <div class="contact-line"><span class="k">Email</span><span class="v"><a href="mailto:Hopco@hpkdq.com">Hopco@hpkdq.com</a></span></div>
        <p class="note" style="margin-top:16px">For a site visit, please send the address, gas source and approximate flow in advance; we will bring both process and electrical engineers.</p>
      </div>
      <div class="contact-card">
        <h3>Six things for the first conversation</h3>
        <ul class="checklist">
          <li>Gas source: biogas / coal mine gas / associated gas / natural gas / biomethane</li>
          <li>Gas data: flow Nm³/h, CH₄%, CO₂%, H₂S ppm</li>
          <li>Load: electrical kW, hot water or steam, cooling required?</li>
          <li>Operation: grid parallel, island, export allowed?</li>
          <li>Site: available area, height, distance to residents</li>
          <li>Stage: feasibility, approval, tender or site ready</li>
        </ul>
        <div class="callout" style="margin-top:18px"><b>Not sure about gas volume?</b> Send one to two weeks of flow-meter readings or gas-holder records and we can start with a range estimate.</div>
      </div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">How we work</span><h2>Start with a calculation</h2></div>
    <div class="grid g4">
      <div class="card"><h3>Pre-feasibility</h3><p>Gas balance, model selection, investment and O&amp;M range, payback range. Free when basic data is complete.</p></div>
      <div class="card"><h3>Technical scheme</h3><p>P&amp;ID, general layout, equipment selection, electrical and control scheme, formal quotation.</p></div>
      <div class="card"><h3>Delivery</h3><p>Supply, installation supervision, commissioning, training, grid connection support and acceptance.</p></div>
      <div class="card"><h3>Investment</h3><p>EMC / EaaS / BOO, with the revenue structure designed around the project boundary.</p></div>
    </div>
    <div class="cta-band" style="margin-top:36px">
      <div><h2>Run the numbers before you decide how to build</h2><p>Our CHP and biogas calculators publish every formula and assumption, so you can cross-check any supplier’s figures — including ours.</p></div>
      <div class="actions"><a class="btn light" href="tools/">Open engineering tools</a></div>
    </div>
  </div>
</section>
'''
    return page("en", "contact.html", "Contact", "Contact Anhui Huasen Hydrogen Energy: sales Liu Yang +86 132 5294 9897; production base Anhui Hopco Electric, No. 18 Qinxi Road, Jing County, Xuancheng, Anhui; +86 195-6572-6668.", body)


# =====================================================================
# tools landing (shared, Chinese UI, English note via /en/ link)
# =====================================================================

def tools_index(lang="zh", slug="tools/", depth=1):
    en = lang == "en"
    r = rel(depth)
    title = "工程测算工具" if not en else "Engineering calculators"
    desc = ("华森 CHP 工业版与民用版测算工具，以及沼气发电、提纯、BHP 与项目经济性计算器。纯前端离线可用。"
            if not en else "Huasen CHP calculators (industrial and residential) plus biogas power, upgrading, BHP and project economics calculators. Pure front-end, offline.")
    body = f'''
<section class="page-head">
  <div class="wrap">
    <div class="breadcrumb" style="color:#9fc0b4"><a href="{r}index.html" style="color:#9fc0b4">{'首页' if not en else 'Home'}</a> / {'工程工具' if not en else 'Tools'}</div>
    <span class="eyebrow">{'公开公式 · 不用注册' if not en else 'Open formulas · no sign-up'}</span>
    <h1>{title}</h1>
    <p class="lead">{'这些公式与我们的预可研一致，所有假设都摊开、可改。用它去质疑供应商的数字——包括我们的。' if not en else 'These formulas match our pre-feasibility work. Every assumption is visible and editable — use them to challenge any supplier’s numbers, including ours.'}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="tool-grid">
      <article class="tool-card">
        <span class="num" style="font-size:12px;font-weight:700;color:var(--brand);letter-spacing:.1em">CHP · INDUSTRIAL</span>
        <h3>{'工业版：重整制氢热电联产' if not en else 'Industrial: reforming hydrogen CHP'}</h3>
        <p>{'百千瓦级、协议口径。输入机组参数，自动算氢耗、甲烷耗、产水量、余热热水、碳排放与单位成本。' if not en else 'Hundred-kW class, technical-agreement basis. Enter unit parameters to get hydrogen and methane consumption, water production, recoverable heat, carbon and unit cost.'}</p>
        <div class="meta">{'适用：沼气 / 煤层气 / 伴生气 / 天然气' if not en else 'For biogas, mine gas, associated gas and natural gas'}</div>
        <a class="btn" href="{r}tools/chp-industrial.html">{'打开工业版' if not en else 'Open industrial'}</a>
      </article>
      <article class="tool-card">
        <span class="num" style="font-size:12px;font-weight:700;color:var(--brand);letter-spacing:.1em">CHP · RESIDENTIAL</span>
        <h3>{'民用版：别墅 / 自建房' if not en else 'Residential: villa / house'}</h3>
        <p>{'按家庭电、热负荷反算机组规模与年运行成本，适合分布式户用场景的初步选型。' if not en else 'Back-calculate unit size and annual running cost from household power and heat load — for early-stage residential selection.'}</p>
        <div class="meta">{'适用：户用 / 小型商业' if not en else 'For households and small commercial'}</div>
        <a class="btn" href="{r}tools/chp-residential.html">{'打开民用版' if not en else 'Open residential'}</a>
      </article>
      <article class="tool-card">
        <span class="num" style="font-size:12px;font-weight:700;color:var(--brand);letter-spacing:.1em">BIOGAS · 7 TOOLS</span>
        <h3>{'沼气工程计算器（7 个）' if not en else 'Biogas calculators (7 tools)'}</h3>
        <p>{'沼气发电与余热、容量选型、压榨量产气、提纯收率、项目经济性、氢燃料电池 CHP、沼气热泵空调 BHP。' if not en else 'Biogas power and heat, capacity sizing, mill throughput, upgrading yield, project economics, hydrogen fuel-cell CHP and BHP air conditioning.'}</p>
        <div class="meta">{'界面为中文，公式通用' if not en else 'Chinese interface, universal formulas'}</div>
        <a class="btn" href="{r}tools/biogas.html">{'打开沼气计算器' if not en else 'Open biogas tools'}</a>
      </article>
    </div>
    <div class="callout" style="margin-top:26px"><b>{'数据不上传：' if not en else 'Nothing is uploaded: '}</b>{'所有计算在浏览器本地完成，可离线使用。结果仅作参考，性能保证以气样分析、技术协议与厂家保证书为准。' if not en else 'All calculations run locally in the browser and work offline. Results are indicative; performance guarantees follow gas analysis, technical agreement and the manufacturer’s warranty.'}</div>
  </div>
</section>
'''
    return page(lang, slug, title, desc, body)


# =====================================================================
# main
# =====================================================================

def main():
    pages = {
        "index.html": zh_home,
        "solutions/hydrogen-chp.html": zh_chp,
        "solutions/bhp.html": zh_bhp,
        "solutions/biogas.html": zh_biogas,
        "equipment.html": zh_equipment,
        "cases.html": zh_cases,
        "about.html": zh_about,
        "contact.html": zh_contact,
        "tools/index.html": lambda: tools_index("zh"),
        "en/index.html": en_home,
        "en/solutions/hydrogen-chp.html": en_chp,
        "en/solutions/bhp.html": en_bhp,
        "en/solutions/biogas.html": en_biogas,
        "en/equipment.html": en_equipment,
        "en/cases.html": en_cases,
        "en/about.html": en_about,
        "en/contact.html": en_contact,
        "en/tools/index.html": lambda: tools_index("en", "tools/", 2),
        "404.html": lambda: page(
            "zh", "404.html", "页面未找到",
            "页面未找到。返回安徽华森氢能源科技官网首页，或查看重整制氢 CHP、BHP 沼气源热泵空调与工程测算工具。",
            f'''<section class="page-head"><div class="wrap"><span class="eyebrow">404</span><h1>这个页面不在了</h1>
<p class="lead">链接可能已更新。你可以返回首页，或直接查看解决方案与工程工具。</p>
<div class="hero-actions"><a class="btn light" href="index.html">返回首页</a><a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="tools/">工程测算工具</a></div>
</div></section>'''),
        "en/404.html": lambda: page(
            "en", "404.html", "Page not found",
            "Page not found. Return to Anhui Huasen Hydrogen Energy, or view reforming hydrogen CHP, BHP air conditioning and engineering calculators.",
            f'''<section class="page-head"><div class="wrap"><span class="eyebrow">404</span><h1>This page is gone</h1>
<p class="lead">The link may have changed. Return to the homepage, or go straight to solutions and engineering tools.</p>
<div class="hero-actions"><a class="btn light" href="index.html">Back to home</a><a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="tools/">Engineering tools</a></div>
</div></section>'''),
    }
    for path, fn in pages.items():
        write(path, fn())

    # sitemap + robots
    urls = [
        ("", ""),
        ("solutions/hydrogen-chp.html", "solutions/hydrogen-chp.html"),
        ("solutions/bhp.html", "solutions/bhp.html"),
        ("solutions/biogas.html", "solutions/biogas.html"),
        ("equipment.html", "equipment.html"),
        ("cases.html", "cases.html"),
        ("about.html", "about.html"),
        ("contact.html", "contact.html"),
        ("tools/", "tools/"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for zh, _ in urls:
        en = "en/" + zh
        for loc in (BASE + "/" + zh, BASE + "/" + en):
            lines.append("<url>")
            lines.append(f"<loc>{loc}</loc>")
            lines.append(f'<xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/{zh}"/>')
            lines.append(f'<xhtml:link rel="alternate" hreflang="en" href="{BASE}/{en}"/>')
            lines.append("</url>")
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


if __name__ == "__main__":
    main()
