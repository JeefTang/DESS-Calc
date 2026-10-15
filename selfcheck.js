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
  recov: 0.80, sc: 5,
  qmode: 'Q', Q: 100, steamT: 1, steamTemp: 600,
  Tin: 15, Tout: 50, etaHex: 0.75,
  pCH4: 3.20, pElec: 0.64, pWater: 4.00, pHeat: 60,
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

console.log('=== 对照任务说明 §5 校验表（P=100kW, η=50%, r=5, 回收0.8, Q=100kW, η_hex=0.75, 15→50℃）===');
let fail = 0;
for (const [name, got, want, tol] of cases) {
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${name.padEnd(18)} 计算=${got.toFixed(4).padStart(10)}  期望≈${String(want).padStart(7)}  容差±${tol}`);
}

// 蒸汽 1 t/h（600℃→50℃）→ ≈18 m³/h
const Rs = calcCore(Object.assign({}, i, { qmode: 'S', steamT: 1 }));
const okSteam = Math.abs(Rs.Vhot - 18) <= 0.1;
if (!okSteam) fail++;
console.log(`${okSteam ? '✓' : '✗'} 蒸汽1t/h→热水m³/h  计算=${Rs.Vhot.toFixed(4).padStart(10)}  期望≈     18  容差±0.1`);

// 附加：警示触发 / 水账方向
console.log('\n=== 附加一致性检查 ===');
console.log(`${R.etaAll > 0.5 ? '✓' : '✗'} 全链路效率 50.3% 触发 >50% 警示`);
console.log(`${R.steamNeed > R.mH2ORecov ? '✓' : '✗'} 净耗水：配汽 ${R.steamNeed.toFixed(2)} kg/h > 回收产水 ${R.mH2ORecov.toFixed(2)} L/h`);
console.log(`  净补水 = ${R.netMakeup.toFixed(2)} kg/h`);
const okUnit = Math.abs(R.unitCost - 0.64) <= 0.02; if (!okUnit) fail++;
console.log(`${okUnit ? '✓' : '✗'} 单位电成本 = ${R.unitCost.toFixed(4)} 元/kWh (期望≈0.64 = 气价3.2÷气电比5；气 ${(R.costCH4/10000).toFixed(2)}万 + 水 ${(R.costWater/10000).toFixed(4)}万 / ${(R.yMWh*1000).toFixed(0)} kWh)`);
console.log(`  理论反推甲烷 = ${R.VCH4Theory.toFixed(2)} Nm³/h`);

// 反算抽查
const rv = core.calcReverse(Object.assign({}, i, { rmode: 'V', tgtV: 5 }));
console.log(`  反算 5 m³/h 热水 → 需 Q=${rv.reqQ.toFixed(1)} kW, 600℃蒸汽 ${rv.reqSteam.toFixed(3)} t/h`);

console.log(`\n${fail === 0 ? '✅ 全部通过' : '❌ 失败 ' + fail + ' 项'}`);
process.exit(fail === 0 ? 0 : 1);
