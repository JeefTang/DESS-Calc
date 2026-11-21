/**
 * selfcheck_res.js — 民用模块口径自测
 * 用法: node selfcheck_res.js
 * 做法: 从 residential.html 抽取 CALC-RES 代码块执行（测的就是页面里跑的逻辑）。
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'residential.html'), 'utf8');
const m = html.match(/\/\* ==CALC-RES-START== \*\/([\s\S]*?)\/\* ==CALC-RES-END== \*\//);
if (!m) { console.error('✗ 未找到 CALC-RES 代码块'); process.exit(1); }
const core = new Function(m[1] + '\nreturn { RC: RC, tierCost: tierCost, calcRes: calcRes };')();
const { calcRes, tierCost } = core;

const APPLIANCES = [
  {n:'电视',p:0.20,q:2},{n:'冰箱',p:0.15,q:1},{n:'空调',p:2.50,q:2},{n:'洗衣机',p:0.50,q:1},
  {n:'干衣机',p:2.00,q:0},{n:'电饭煲',p:1.00,q:1},{n:'电磁炉',p:2.20,q:1},{n:'微波炉',p:1.20,q:0},
  {n:'洗碗机',p:1.50,q:0},{n:'电脑',p:0.30,q:2},{n:'照明',p:0.30,q:1},{n:'抽油烟机',p:0.25,q:1},
  {n:'新风',p:0.10,q:1},{n:'其他',p:0.50,q:1}
];

const base = {
  Area:300, K:1.2, Tib:20, Tob:-10, heatDays:150, loadF:0.55, dTloop:10, vSys:15, lossRate:0.01,
  nPeople:4, Vper:50, Tshower:42, Tcw:10, freqDay:1, dhwDays:365, peakF:0.5, flowHead:300,
  appliances: APPLIANCES, demandF:1.0, eYear:6000, hEq:1200, hasEV:false, evYear:3000, evPrice:0.72,
  gasType:'ng',
  gasTiers:[{upTo:30,price:2.80},{upTo:50,price:3.10},{upTo:Infinity,price:3.90}],
  elecTiers:[{upTo:240,price:0.5583},{upTo:400,price:0.6083},{upTo:Infinity,price:0.8583}],
  pGrid:0.40, pWater:4.00,
  pvOn:false, pvArea:60, pvDensity:150, pvHours:1200, pvSelf:0.7, pvCost:3.00,
  modP:12.5, unitCost:1.0, etaE:0.40, etaH:0.45, heatDelivery:0.95, etaWH:0.88,
  strategy:'heat', hRun:2000, hCap:8000,
  opexRate:0.02, life:15, disc:0.06, subsidy:0
};

const R = calcRes(base);

console.log('=== 民用模块校验（默认：别墅300m², K=1.2, 20/-10℃, 4人洗浴50L, 电器11kW, 12.5kW/模块, η_e40/η_h45）===');
let fail = 0;
function chk(name, got, want, tol){
  const ok = Math.abs(got - want) <= tol;
  if (!ok) fail++;
  console.log(`${ok?'✓':'✗'} ${name.padEnd(26)} 计算=${(isFinite(got)?got.toFixed(4):'∞').padStart(12)}  期望≈${String(want).padStart(9)}  容差±${tol}`);
}

// ① 供暖
chk('室内外温差 K',        R.dTh,        30,     0.001);
chk('供暖设计热负荷 kW',   R.Qheat,      10.8,   0.001);
chk('等效热指标 W/m²',     R.qIndex,     36,     0.001);
chk('供暖季耗热 kWh',      R.heatYear,   21384,  0.5);
chk('等效满负荷小时 h',    R.eqHours,    1980,   0.001);
chk('供暖循环流量 m³/h',   R.Vloop,      0.93014, 0.001);
chk('系统水容量 L',        R.Vsys,       162,    0.001);
chk('供暖补水 m³/年',      R.makeHeatYear, 0.243, 0.001);
// ② 生活热水
chk('单人次耗热 kWh',      R.perUse,     1.8578, 0.001);
chk('日热水用量 L',        R.dhwVolDay,  200,    0.001);
chk('日热水耗热 kWh',      R.dhwDay,     7.4311, 0.001);
chk('年热水耗热 kWh',      R.dhwYear,    2712.36, 0.5);
chk('年热水用量 m³',       R.dhwVolYear, 73,     0.001);
chk('峰值热水负荷 kW',     R.QdhwPeak,   22.2933, 0.001);
// ③ 用电
chk('电器装机 kW',         R.Papp,       11.0,   0.001);
chk('计算负荷 kW',         R.Pload,      11.0,   0.001);
chk('模块数',              R.Nmod,       1,      0.001);
chk('装机功率 kW',         R.Pinst,      12.5,   0.001);
// ④ 装置
chk('年运行小时 h',        R.hRun,       1803.70, 0.5);
chk('年发电量 kWh',        R.Egen,       22546.3, 5);
chk('年耗气 Nm³',          R.FgasQty,    5652.4,  1);
chk('年可回收热 kWh',      R.Qrec,       25364.6, 10);
chk('装置年供热 kWh',      R.heatSup,    24096.36, 2);
chk('供热覆盖率',          R.covHeat,    1.0,    0.001);
chk('余电上网 kWh',        R.Esur,       16546.3, 5);
// ⑤ 费用
chk('装置年气费 元',       R.costGasDev, 21456.5, 30);
chk('年水费 元',           R.costWater,  292.97, 0.5);
chk('装置年支出 元',       R.costDevTotal, 17631, 60);
chk('基准年支出 元',       R.costBaseTotal, 14380, 40);
chk('年节省 元',           R.saveAnnual, -3251, 60);
chk('总投资 元',           R.invTotal,   125000, 1);
console.log(`  → 静态回收期 = ${isFinite(R.payback)?R.payback.toFixed(2):'∞'}（默认外购居民阶梯气价下为负 → 不划算，符合预期）`);
chk('综合效率',            R.etaAll,     0.85,   0.001);

// 运行策略：按用电需求
const Re = calcRes(Object.assign({}, base, {strategy:'elec'}));
chk('「按电」年运行小时 h', Re.hRun,      480,    0.001);
chk('「按电」年发电 kWh',   Re.Egen,      6000,   0.001);
const okEL = Re.Esur === 0 && Math.abs(Re.Rd) < 1e-9;
if (!okEL) fail++;
console.log(`${okEL?'✓':'✗'} 「按电」策略：余电 ${Re.Esur}，剩余需求 ${Re.Rd}（期望 0/0）`);

// 阶梯计价
chk('阶梯气价 5652 Nm³ 年费', tierCost(5652.42, base.gasTiers), 21456.5, 30);
chk('阶梯电价 6000 kWh 年费', tierCost(6000, base.elecTiers), 3805.8, 5);

// 免费气（自产气）→ 应转正
const Rz = calcRes(Object.assign({}, base, {
  gasTiers:[{upTo:30,price:0},{upTo:50,price:0},{upTo:Infinity,price:0}]}));
const okZ = Rz.saveAnnual > 0;
if (!okZ) fail++;
console.log(`${okZ?'✓':'✗'} 气价=0（自产气）→ 年节省 ${(Rz.saveAnnual/10000).toFixed(2)} 万元，静态回收期 ${Rz.payback.toFixed(1)} 年（期望 >0）`);

// 加装光伏 → 回收期改善
const Rp = calcRes(Object.assign({}, base, {pvOn:true}));
chk('光伏装机 kW', Rp.Ppv, 9, 0.001);
chk('光伏年发电 kWh', Rp.Epv, 10800, 0.001);
chk('光伏投资 元', Rp.PpvCost, 27000, 1);
const okPV = Rp.costDevTotal < R.costDevTotal;
if (!okPV) fail++;
console.log(`${okPV?'✓':'✗'} 加装光伏：装置年支出 ${(R.costDevTotal/10000).toFixed(2)} 万 → ${(Rp.costDevTotal/10000).toFixed(2)} 万元（下降）`);

// 液化气口径
const Rl = calcRes(Object.assign({}, base, {gasType:'lpg',
  gasTiers:[{upTo:30,price:8},{upTo:60,price:8},{upTo:Infinity,price:8}]}));
chk('液化气：年耗气 kg', Rl.FgasQty, 56365.75/12.56, 1);
const okLPG = Rl.gasUnit === 'kg' && Math.abs(Rl.LHV - 12.56) < 1e-9;
if (!okLPG) fail++;
console.log(`${okLPG?'✓':'✗'} 液化气口径：单位 ${Rl.gasUnit}，LHV ${Rl.LHV} kWh/kg`);

// 补水倍数
const ratio = R.dhwVolYear / R.makeHeatYear;
const okW = ratio > 100;
if (!okW) fail++;
console.log(`${okW?'✓':'✗'} 补水倍数（洗浴÷供暖）= ${ratio.toFixed(0)} 倍（期望 >>1：洗浴直排补水远大于供暖闭式补水）`);

console.log(`\n${fail === 0 ? '✅ 全部通过' : '❌ 失败 ' + fail + ' 项'}`);
process.exit(fail === 0 ? 0 : 1);
