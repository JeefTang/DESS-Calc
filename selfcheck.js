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
const econ = [
  ['年发电收益 万元',  R.revElec/10000,   56.00,  0.01],
  ['年供热收益 万元',  R.revHeat/10000,   12.96,  0.01],
  ['年运维费 万元',    R.opex/10000,       3.4514, 0.01],
  ['年净收益 万元',    R.netAnnual/10000, 14.31,  0.02],
  ['静态回收期 年',    R.payback,         12.06,  0.05],
  ['ROI %/年',        R.roi*100,          8.29,  0.02],
  ['NPV 万元',        R.npv/10000,      -67.26,  0.50],
  ['寿命期累计 万元',  R.cumProfit/10000, 143.09,  0.10],
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

console.log(`\n${fail === 0 ? '✅ 全部通过' : '❌ 失败 ' + fail + ' 项'}`);
process.exit(fail === 0 ? 0 : 1);
