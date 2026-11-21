/**
 * selfcheck.js — 口径自测（对照任务说明 §5 校验表）
 * 用法: node selfcheck.js
 * 做法: 从 index.html 中抽取 CALC-CORE 代码块并执行，保证测的就是页面里跑的那份逻辑。
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const m = html.match(/\/\* ==CALC-CORE-START== \*\/([\s\S]*?)\/\* ==CALC-CORE-END== \*\//);
if (!m) { console.error('✗ 未找到 CALC-CORE 代码块'); process.exit(1); }
const core = new Function(m[1] + '\nreturn { CONST: CONST, calcCore: calcCore, calcReverse: calcReverse };')();
const { calcCore } = core;

const i = {
  P: 100, eta: 0.50, h: 8000, r: 5,
  psa: 0.80, refconv: 0.90,
  recov: 0.80, sc: 5, heatMode: 'auto', steamSelf: 1, heatSrc: 'burner', oxid: 'air', oc: 0.40, ch4f: 60,
  qmode: 'Q', Q: 100, steamT: 1, steamTemp: 600,
  Tin: 15, Tout: 50, etaHex: 0.75,
  pCH4: 3.20, pElec: 0.70, pWater: 4.00, pHeat: 60,
  inv: 172.57, opexRate: 0.02, life: 10, disc: 0.06, subsidy: 0,
  // 碳资产（默认=页面默认：养殖场沼气 · 直排放空 · 生物源 · GWP100 · 计入替代电网）
  gasType: 'biogas', baseMode: 'vent', flareEff: 0.98, gwp: 28, carbonType: 'biogenic',
  gridEF: 0.5568, countGrid: true, pCarbon: 70, creditYears: 10, includeCarbon: true,
  rmode: 'off', tgtP: 200, tgtV: 5
};
const R = calcCore(i);

const cases = [
  ['氢耗 kg/h',        R.mH2,         6.01,  0.01],
  ['氢耗 Nm³/h',       R.VH2,         67,    0.5],
  ['甲烷耗 Nm³/h',     R.VCH4,        20,    0.01],
  ['甲烷耗 kg/h',      R.mCH4,        14.34, 0.01],
  ['全链路效率 %',     R.etaAll*100,  50.3,  0.05],
  ['理论产水 kg/h',    R.mH2OTheory,  54.1,  0.05],
  ['回收产水 L/h',     R.mH2ORecov,   43,    0.5],
  ['产水率 kg/kWh',    R.waterRate,   0.54,  0.005],
  ['CO₂ kg/h',         R.mCO2,        39.3,  0.05],
  ['CO₂ 年 t',         R.yCO2,        314,   0.5],
  ['热水(实际) m³/h',  R.Vhot,        1.85,  0.01],
  ['热水(理论) m³/h',  R.VhotTheory,  2.46,  0.01],
];

// ⑧ 经济效益（老唐 2026-10-15 确认：投资按不含税 172.57 万；电价 0.70 元/kWh；
//    运维 2%/年；寿命 10 年；折现率 6%）
// ⚠ 2026-10-15 口径修正：重整改为「自热耦合」默认（不外供蒸汽，自产占比 100%）
//    → 净补水 0 → 年水费 0，故净收益/回收期较旧版（外供蒸汽口径）略有变化
// ⚠ 2026-10-15 新增：碳资产模块（默认计入）→ 年净收益/回收期含碳收益
const econ = [
  ['年发电收益 万元',  R.revElec/10000,   56.00,  0.01],
  ['年供热收益 万元',  R.revHeat/10000,   12.96,  0.01],
  ['年碳收益 万元',    R.revCarbon/10000, 25.60,  0.02],
  ['年运维费 万元',    R.opex/10000,       3.4514, 0.01],
  ['年收益合计 万元',  R.revTotal/10000,  94.56,  0.02],
  ['年净收益 万元',    R.netAnnual/10000, 39.91,  0.02],
  ['静态回收期 年',    R.payback,          4.32,  0.02],
  ['不含碳回收期 年',  R.paybackNoC,      12.06,  0.05],
  ['ROI %/年',        R.roi*100,         23.13,  0.05],
  ['NPV 万元',        R.npv/10000,      121.18,  0.50],
  ['动态回收期 年',    R.discPayback,       5.16,  0.05],
  ['碳收益占比 %',     R.carbonShare*100,  27.07,  0.05],
  ['寿命期累计 万元',  R.cumProfit/10000, 399.12,  0.10],
];

console.log('=== 对照任务说明 §5 校验表（P=100kW, η=50%, r=5, 回收0.8, Q=100kW, η_hex=0.75, 15→50℃）===');
let fail = 0;
for (const [name, got, want, tol] of cases) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(18)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(7)}  容差±${tol}`);
}

console.log('\n=== ⑧ 经济效益（投资 172.57 万不含税 / 电价 0.70 / 运维 2%/年 / 寿命 10 年 / 折现 6%）===');
for (const [name, got, want, tol] of econ) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(18)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(8)}  容差±${tol}`);
}
console.log(`  IRR = ${R.irr !== null ? (R.irr*100).toFixed(2)+' %' : '无解'}（负值=按外购气价不划算）`);
console.log(`  动态回收期 = ${R.discPayback !== null ? R.discPayback.toFixed(2)+' 年' : '>'+i.life+' 年'}`);
const rFree = calcCore(Object.assign({}, i, { pCH4: 0 }));
console.log(`  敏感性抽查：气价=0（自产沼气）→ 年净收益 ${(rFree.netAnnual/10000).toFixed(2)} 万元，回收期 ${rFree.payback.toFixed(2)} 年`);

// 蒸汽 1 t/h（600℃→50℃）→ ≈18 m³/h
const Rs = calcCore(Object.assign({}, i, { qmode: 'S', steamT: 1 }));
const okSteam = Math.abs(Rs.Vhot - 18) <= 0.1;
if (!okSteam) fail++;
console.log(`${okSteam ? '✓' : '✗'} 蒸汽1t/h→热水m³/h  计算=${Rs.Vhot.toFixed(4).padStart(10)}  期望≈     18  容差±0.1`);

// 附加：警示触发 / 水账方向（自热耦合口径）
console.log('\n=== 附加一致性检查（自热耦合 · 默认）===');
console.log(`${R.etaAll > 0.5 ? '✓' : '✗'} 全链路效率 50.3% 触发 >50% 警示`);
const okSelf = Math.abs(R.steamSelf - R.steamNeed) < 1e-9 && Math.abs(R.steamExt) < 1e-9;
if (!okSelf) fail++;
console.log(`${okSelf ? '✓' : '✗'} 自热耦合：自产蒸汽 ${R.steamSelf.toFixed(2)} kg/h = 蒸汽需求 ${R.steamNeed.toFixed(2)} kg/h，外供 ${R.steamExt.toFixed(2)} kg/h`);
console.log(`${R.netMakeup === 0 ? '✓' : '✗'} 净补水 = ${R.netMakeup.toFixed(2)} kg/h（不外供 → 系统水自平衡）`);

// 外供蒸汽（对比）口径：应回到老版数值
const Rext = calcCore(Object.assign({}, i, { heatMode: 'ext' }));
const okExt = Math.abs(Rext.netMakeup - 37.07) <= 0.05 && Math.abs(Rext.steamExt - Rext.steamNeed) < 1e-9;
if (!okExt) fail++;
console.log(`${okExt ? '✓' : '✗'} 外供蒸汽模式：外供 ${Rext.steamExt.toFixed(2)} kg/h，净补水 ${Rext.netMakeup.toFixed(2)} kg/h（期望≈ 37.07）`);

// 重整配气·氧化剂（催化部分氧化·配空气，O₂/C=0.40）
const Rox = calcCore(Object.assign({}, i, { heatSrc: 'cpo', oxid: 'air', oc: 0.40 }));
const ox = [
  ['O₂ 配入 Nm³/h',   Rox.vO2,  8.00,  0.01],
  ['空气配入 Nm³/h',   Rox.vAir, 38.10, 0.05],
  ['空气带入 N₂ Nm³/h', Rox.vN2, 30.10, 0.05],
];
console.log('\n=== 重整配气·氧化剂（催化部分氧化 · 空气 · O₂/C=0.40）===');
for (const [name, got, want, tol] of ox) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(20)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(7)}  容差±${tol}`);
}
const Rno = calcCore(Object.assign({}, i, { heatSrc: 'cpo', oxid: 'none' }));
const okNone = Rno.vO2 === 0 && Rno.vAir === 0 && Rno.vN2 === 0;
if (!okNone) fail++;
console.log(`${okNone ? '✓' : '✗'} 不配氧化剂 → O₂/空气/N₂ 均为 0`);
const okUnit = Math.abs(R.unitCost - 0.64) <= 0.02; if (!okUnit) fail++;
console.log(`${okUnit ? '✓' : '✗'} 单位电成本 = ${R.unitCost.toFixed(4)} 元/kWh (期望≈0.64 = 气价3.2÷气电比5；气 ${(R.costCH4/10000).toFixed(2)}万 + 水 ${(R.costWater/10000).toFixed(4)}万 / ${(R.yMWh*1000).toFixed(0)} kWh)`);
console.log(`  理论反推甲烷 = ${R.VCH4Theory.toFixed(2)} Nm³/h`);

// 进堆氢浓度（参考）：内置燃烧器（协议口径）· 变换气干基组成
const h2 = [
  ['化学计量氢 Nm³/h', R.cH2,        80.00,  0.05],
  ['氢质量 kg/h',      R.mH2Stoich,   7.19,  0.02],
  ['化学计量 CO₂ Nm³/h', R.cCO2,    33.33,  0.05],
  ['沼气量 Nm³/h',     R.vBiogas,    33.33,  0.05],
  ['纯化前干基 H₂ %',  R.yH2raw*100, 70.59,  0.05],
];
console.log('\n=== 进堆氢浓度（参考 · 内置燃烧器·协议口径 · 沼气 CH₄=60% · 全转化假设）===');
for (const [name, got, want, tol] of h2) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(20)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(7)}  容差±${tol}`);
}
const okBN2 = R.cN2 === 0 && Math.abs(R.yH2deN - R.yH2raw) < 1e-9;
if (!okBN2) fail++;
console.log(`${okBN2 ? '✓' : '✗'} 内置燃烧器：空气不进工艺气 → N₂=0，脱氮前后氢浓度相同 ${(R.yH2deN*100).toFixed(2)}%`);
const okSpec = R.yH2deN >= 0.695;
if (!okSpec) fail++;
console.log(`${okSpec ? '✓' : '✗'} 进堆氢浓度 ${(R.yH2deN*100).toFixed(2)}% ≥ 协议阈值 70%（±0.5pp 容差）`);

// 催化部分氧化（对比口径）：配空气 O₂/C=0.40 → N₂ 稀释
const Rcpo = calcCore(Object.assign({}, i, { heatSrc: 'cpo', oxid: 'air', oc: 0.40 }));
const cpo = [
  ['CPO·O₂ Nm³/h',     Rcpo.vO2,           8.00,  0.01],
  ['CPO·空气 Nm³/h',   Rcpo.vAir,         38.10,  0.05],
  ['CPO·N₂ Nm³/h',     Rcpo.vN2,          30.10,  0.05],
  ['CPO·化学计量氢',   Rcpo.cH2,          64.00,  0.05],
  ['CPO·纯化前干基 H₂ %', Rcpo.yH2raw*100, 50.22, 0.05],
  ['CPO·脱氮后干基 H₂ %', Rcpo.yH2deN*100, 65.75, 0.05],
];
console.log('\n=== 催化部分氧化（对比口径 · 空气 O₂/C=0.40）===');
for (const [name, got, want, tol] of cpo) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(22)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(7)}  容差±${tol}`);
}
// 沼气 CH₄ 低端 50% → 氢浓度下降
const Rlo = calcCore(Object.assign({}, i, { ch4f: 50 }));
const okLo = Math.abs(Rlo.yH2raw*100 - 66.67) <= 0.05;
if (!okLo) fail++;
console.log(`${okLo ? '✓' : '✗'} 沼气 CH₄=50% → 纯化前干基 H₂ ${(Rlo.yH2raw*100).toFixed(2)}%（期望 66.67%）`);

// 反算抽查
const rv = core.calcReverse(Object.assign({}, i, { rmode: 'V', tgtV: 5 }));
console.log(`  反算 5 m³/h 热水 → 需 Q=${rv.reqQ.toFixed(1)} kW, 600℃蒸汽 ${rv.reqSteam.toFixed(3)} t/h`);

console.log('\n=== ⑨ 碳资产（默认：养殖场沼气 · 直排放空 · 生物源 · GWP100=28 · 碳价 70 元/tCO₂e）===');
const carbon = [
  ['甲烷质量流量 t/h',  R.CH4_t,            0.01434, 0.00001],
  ['基准线(直排) t/年', R.beCH4*i.h,        3212.16, 0.5],
  ['替代电网 t/年',    R.gridAvoid*i.h,      445.44, 0.5],
  ['项目排放 t/年',    R.peCH4*i.h,           0.00, 0.001],
  ['净减排 tCO₂e/年',  R.erY,              3657.6,  1.0],
  ['减排强度 kg/kWh',  R.erIntensity,         4.572, 0.01],
  ['年碳收益 万元',    R.carbonRevY/10000,   25.60,  0.02],
  ['计入期累计 t',     R.carbonCum,        36576,   10],
  ['碳资产现值 万元',  R.carbonNPV/10000,   188.41, 0.5],
];
for (const [name, got, want, tol] of carbon) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(18)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(8)}  容差±${tol}`);
}

console.log('\n=== 气源预设差异（同一机组 P=100kW）===');
// 油田伴生气：火炬基准 + 化石源 → 减排量大幅低于沼气直排
const Rof = calcCore(Object.assign({}, i, { gasType:'oilfield', ch4f:85, baseMode:'flare', carbonType:'fossil' }));
const of = [
  ['伴生气·基准线 t/年', Rof.beCH4*8000, 372.20, 0.5],
  ['伴生气·项目排放 t/年', Rof.peCH4*8000, 314.24, 0.5],
  ['伴生气·净减排 t/年', Rof.erY,         503.40, 1.0],
  ['伴生气·年碳收益 万元', Rof.carbonRevY/10000, 3.52, 0.05],
];
for (const [name, got, want, tol] of of) {
  const ok = Math.abs(got - want) <= tol; if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(22)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(8)}  容差±${tol}`);
}
// 煤矿瓦斯（井下）：直排 + 化石源
const Rcmm = calcCore(Object.assign({}, i, { gasType:'cmm', ch4f:45, baseMode:'vent', carbonType:'fossil' }));
const okCmm = Math.abs(Rcmm.erY - 3343.36) <= 1;
if (!okCmm) fail++;
console.log(`${okCmm ? '✓' : '✗'} 煤矿瓦斯·净减排 t/年  计算=${Rcmm.erY.toFixed(2).padStart(10)}  期望≈  3343.36  容差±1（直排×GWP − 化石项目排放）`);
// 沼泽气 + GWP20（84）→ 减排量约×3
const Rg20 = calcCore(Object.assign({}, i, { gwp: 84 }));
const okG20 = Math.abs(Rg20.erY - 10081.9) <= 3;
if (!okG20) fail++;
console.log(`${okG20 ? '✓' : '✗'} GWP₂₀=84 → 净减排 t/年 计算=${Rg20.erY.toFixed(2).padStart(10)}  期望≈ 10081.9  容差±3`);
// 关闭「替代电网」→ 仅甲烷减排
const Rng = calcCore(Object.assign({}, i, { countGrid: false }));
const okNg = Math.abs(Rng.erY - 3212.16) <= 0.5 && Rng.gridAvoid === 0;
if (!okNg) fail++;
console.log(`${okNg ? '✓' : '✗'} 关闭替代电网 → 净减排 ${Rng.erY.toFixed(2)} t/年（=基准线 3212.16）`);
// 关闭「碳收益计入经济评价」→ 回到不含碳口径
const Rnc = calcCore(Object.assign({}, i, { includeCarbon: false }));
const okNc = Math.abs(Rnc.netAnnual - R.netAnnualNoC) < 1e-6 && Math.abs(Rnc.revCarbon) < 1e-9;
if (!okNc) fail++;
console.log(`${okNc ? '✓' : '✗'} 碳收益不计入 → 年净收益 ${(Rnc.netAnnual/10000).toFixed(2)} 万元（=不含碳口径，回收期 12.06 年）`);
// 碳价敏感性：碳价 0 → 碳收益 0 但减排量不变
const Rc0 = calcCore(Object.assign({}, i, { pCarbon: 0 }));
const okC0 = Rc0.carbonRevY === 0 && Math.abs(Rc0.erY - R.erY) < 1e-9;
if (!okC0) fail++;
console.log(`${okC0 ? '✓' : '✗'} 碳价=0 → 减排量不变 ${Rc0.erY.toFixed(1)} t/年，碳收益 0`);

console.log(`\n${fail === 0 ? '✅ 全部通过' : '❌ 失败 ' + fail + ' 项'}`);
process.exit(fail === 0 ? 0 : 1);
