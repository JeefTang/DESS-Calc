/* KSTS bioenergy calculators — transparent formulas, no dependencies */
(function () {
  "use strict";

  var CH4_KWH_PER_NM3 = 9.94;     // LHV of methane, kWh/Nm3 (35.8 MJ/Nm3)
  var DIESEL_KWH_PER_L = 9.94;    // LHV, kWh/L
  var DIESEL_CO2_KG_PER_L = 2.68;

  function $(id) { return document.getElementById(id); }
  function val(id, dflt) {
    var v = parseFloat($(id) && $(id).value);
    return isFinite(v) ? v : (dflt || 0);
  }
  function nf(x, d) {
    if (!isFinite(x)) return "—";
    d = d === undefined ? 0 : d;
    return x.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function cny(x, d) {
    if (!isFinite(x)) return "—";
    d = d === undefined ? 1 : d;
    return Math.abs(x) >= 10000 ? "¥ " + nf(x / 10000, d) + " 万" : "¥ " + nf(x, 0);
  }
  function usd(x) {
    if (!isFinite(x)) return "—";
    return "US$ " + nf(Math.round(x / 100) * 100, 0);
  }
  function set(id, text) { var el = $(id); if (el) el.textContent = text; }
  function warn(id, text) {
    var el = $(id);
    if (!el) return;
    if (text) { el.textContent = text; el.classList.add("show"); }
    else { el.textContent = ""; el.classList.remove("show"); }
  }

  /* ---------------------------------------------------------- tool 1 */
  function tool1() {
    var flow = val("t1_flow"), ch4 = val("t1_ch4"), eff = val("t1_eff"),
        heat = val("t1_heat"), hours = val("t1_hours"), load = val("t1_load");

    var fuelKW = flow * (ch4 / 100) * CH4_KWH_PER_NM3;
    var kW = fuelKW * eff / 100;
    var heatKW = fuelKW * heat / 100;
    var total = eff + heat;
    var gasPerKWh = kW > 0 ? flow / kW : 0;
    var yearKWh = kW * hours * load / 100;
    var yearHeat = heatKW * hours * load / 100;
    var dieselL = yearKWh / (DIESEL_KWH_PER_L * 0.35);
    var co2t = dieselL * DIESEL_CO2_KG_PER_L / 1000;

    set("t1_kw", nf(kW, 0) + " kW");
    set("t1_heatkw", nf(heatKW, 0) + " kW");
    set("t1_energy", nf(fuelKW, 0) + " kW");
    set("t1_total", nf(total, 0) + "%");
    set("t1_gas_kwh", nf(gasPerKWh, 2) + " Nm³/kWh");
    set("t1_year_kwh", nf(yearKWh / 1000, 0) + " MWh");
    set("t1_year_heat", nf(yearHeat / 1000, 0) + " MWh");
    set("t1_diesel", nf(dieselL, 0) + " L/yr · " + nf(co2t, 0) + " t CO₂");

    var msgs = [];
    if (ch4 < 45) msgs.push("Methane below 45%: outside the engine fuel specification — output is derated per the manufacturer's curve, and combustion becomes unstable.");
    if (load < 70) msgs.push("Average load below 70%: expect carbon build-up and a shorter overhaul interval. Consider a smaller unit or two units.");
    if (heat + eff > 92) msgs.push("Combined efficiency above 92% is not achievable — check the heat recovery assumption.");
    warn("t1_warn", msgs.join(" "));
  }

  /* --------------------------------------------- tool 2 · engine sizing + economics */
  /* Engine models — export list price, USD per unit (FOB, standard scope). */
  var ICE_MODELS = [
    { kw: 500, usd: 216667 },
    { kw: 600, usd: 234722 },
    { kw: 700, usd: 252778 },
    { kw: 800, usd: 288889 },
    { kw: 1000, usd: 379167 }
  ];

  function tool2() {
    var kW = val("t2_kw"), ch4 = val("t2_ch4"), eff = val("t2_eff"), load = val("t2_load");
    var hours = val("t2_hours", 8000);
    var tariff = val("t2_tariff"), use = val("t2_use", 100);
    var fx = val("t2_fx") || 1, om = val("t2_om"), omfix = val("t2_omfix"), disc = val("t2_disc") / 100;

    var modelSel = $("t2_model");
    var modelKW = modelSel && modelSel.value !== "" ? parseFloat(modelSel.value) : NaN;
    var enginePerKW = val("t2_engine", 391);
    var bopPerKW = val("t2_bop", 0);
    var engineModel = null;
    for (var mi = 0; isFinite(modelKW) && mi < ICE_MODELS.length; mi++) {
      if (ICE_MODELS[mi].kw === modelKW) engineModel = ICE_MODELS[mi];
    }
    if (engineModel) {
      enginePerKW = engineModel.usd / engineModel.kw;
      var engineEl = $("t2_engine");
      if (engineEl) engineEl.value = Math.round(enginePerKW);
    }
    var engineCost = kW * enginePerKW;
    var bopCost = kW * bopPerKW;

    var fuelKW = kW / (eff / 100);
    var flow = ch4 > 0 ? fuelKW / (ch4 / 100) / CH4_KWH_PER_NM3 : 0;
    var flowDay = flow * 24;
    var avg = flow * load / 100;
    var ch4flow = flow * ch4 / 100;
    var year = avg * hours;

    var gen = kW * hours * load / 100;
    var capex = engineCost + bopCost;
    var tariffUSD = tariff / fx;
    var revUSD = gen * (use / 100) * tariffUSD;
    var opexUSD = gen * om + omfix;
    var netUSD = revUSD - opexUSD;
    var payback = netUSD > 0 ? capex / netUSD : Infinity;

    var npv = -capex;
    for (var t = 1; t <= 10; t++) npv += netUSD / Math.pow(1 + disc, t);
    var cum10 = netUSD * 10 - capex;
    var r = irr(capex, netUSD, 10);
    var crf = disc > 0 ? (disc * Math.pow(1 + disc, 10)) / (Math.pow(1 + disc, 10) - 1) : 0.1;
    var lcoe = gen > 0 ? (capex * crf + opexUSD) / gen : 0;

    set("t2_flow", nf(flow, 0) + " Nm³/h");
    set("t2_day", nf(flowDay, 0) + " Nm³/day");
    set("t2_avg", nf(avg, 0) + " Nm³/h");
    set("t2_ch4flow", nf(ch4flow, 0) + " Nm³/h");
    set("t2_energy", nf(fuelKW, 0) + " kW");
    set("t2_year", nf(year / 1000000, 2) + " million Nm³/yr");

    set("t2_engine_cost", usd(engineCost) + "（" + cny(engineCost * fx, 1) + "）");
    set("t2_bop_cost", usd(bopCost) + "（" + cny(bopCost * fx, 1) + "）");
    set("t2_total_capex", usd(capex) + "（" + cny(capex * fx, 1) + "）");
    set("t2_gen", nf(gen / 1000, 0) + " MWh/yr");
    set("t2_rev", cny(revUSD * fx, 1) + "/年");
    set("t2_opex", cny(opexUSD * fx, 1) + "/年");
    set("t2_net", cny(netUSD * fx, 1) + "/年");
    set("t2_payback", isFinite(payback) ? nf(payback, 2) + " 年" : "无法回收");
    set("t2_cum10", cny(cum10 * fx, 1));
    set("t2_npv", cny(npv * fx, 1));
    set("t2_irr", isFinite(r) ? nf(r * 100, 1) + "%" : "n/a");
    set("t2_lcoe", "¥ " + nf(lcoe * fx, 3) + "/kWh");

    var msgs = [];
    if (ch4 < 45) msgs.push("At this methane content the engine is outside its fuel specification: check the manufacturer's derating curve.");
    if (eff > 42) msgs.push("Efficiency above 42% is at the top of the range for gas engines — verify it is not a lower-heating-value claim.");
    if (netUSD <= 0) msgs.push("Negative annual net cash flow at these prices and capex — the payback never closes. Check the displaced power price, self-use share and capex scope.");
    if (use > 90) msgs.push("Assuming almost all output displaces bought power is optimistic unless the mill runs a steady 24-hour load.");
    if (isFinite(modelKW) && kW > 0 && Math.abs(kW - modelKW) / modelKW > 0.01) msgs.push("目标功率与所选机型不一致：机组价按所选的 " + modelKW + " kW 机型单价折算，建议直接改选对应机型。");
    if (enginePerKW < 250) msgs.push("机组价低于 250 美元/kW，明显低于当前机型报价——核对是否选错机型。");
    if (bopPerKW === 0) msgs.push("配套与安装为 0：这是机组 FOB 口径，不含沼气预处理、余热回收、并网、土建与安装。");
    else if (enginePerKW + bopPerKW < 900) msgs.push("全站投资低于 900 美元/kW 偏紧——核查是否漏了气柜、脱硫脱水、余热与并网。");
    if (payback < 2) msgs.push("Payback under 2 years is unusual for a complete plant — check that capex includes pond cover, gas treatment, civils and grid connection.");
    warn("t2_warn", msgs.join(" "));
  }

  /* ---------------------------------------------------------- tool 3 */
  function tool3() {
    var ffb = val("t3_ffb"), pome = val("t3_pome"), yield_ = val("t3_yield"),
        ch4 = val("t3_ch4"), cap = val("t3_capture"), eff = val("t3_eff");

    var pomeDay = ffb * 24 * pome;
    var gasDay = pomeDay * yield_ * cap / 100;
    var gasH = gasDay / 24;
    var ch4H = gasH * ch4 / 100;
    var fuelKW = gasH * (ch4 / 100) * CH4_KWH_PER_NM3;
    var kW = fuelKW * eff / 100;
    var mwh = kW * 8000 / 1000;

    set("t3_pome_day", nf(pomeDay, 0) + " m³/day");
    set("t3_gas_day", nf(gasDay, 0) + " Nm³/day");
    set("t3_gas_h", nf(gasH, 0) + " Nm³/h");
    set("t3_ch4_h", nf(ch4H, 0) + " Nm³/h");
    set("t3_kw", nf(kW, 0) + " kW");
    set("t3_mwh", nf(mwh, 0) + " MWh/yr");

    var msgs = [];
    if (yield_ > 30) msgs.push("Yield above 30 Nm³/m³ POME is optimistic for a covered lagoon — it assumes a well-mixed, heated digester.");
    if (cap > 90) msgs.push("Capture efficiency above 90% requires a well-sealed cover and active pressure management.");
    warn("t3_warn", msgs.join(" "));
  }

  /* ---------------------------------------------------------- tool 4 */
  function tool4() {
    var flow = val("t4_flow"), ch4 = val("t4_ch4"), rec = val("t4_rec"),
        purity = val("t4_purity"), power = val("t4_power");

    var ch4in = flow * ch4 / 100;
    var ch4out = ch4in * rec / 100;
    var product = purity > 0 ? ch4out / (purity / 100) : 0;
    var loss = ch4in - ch4out;
    var co2 = flow * (1 - ch4 / 100);
    var mw = product * CH4_KWH_PER_NM3 / 1000;
    var kW = flow * power;
    var diesel = product; // Nm3 CH4 at 9.94 kWh/Nm3 vs diesel 9.94 kWh/L

    set("t4_ch4in", nf(ch4in, 0) + " Nm³/h");
    set("t4_product", nf(product, 0) + " Nm³/h");
    set("t4_ch4out", nf(ch4out, 0) + " Nm³/h");
    set("t4_loss", nf(loss, 0) + " Nm³/h (" + nf(100 - rec, 1) + "%)");
    set("t4_co2", nf(co2, 0) + " Nm³/h");
    set("t4_mw", nf(mw, 2) + " MW (LHV)");
    set("t4_kw", nf(kW, 0) + " kW");
    set("t4_diesel", nf(diesel, 0) + " L/h equivalent");
  }

  /* ---------------------------------------------------------- finance helpers */
  function irr(capex, annual, years) {
    function npv(r) {
      var s = -capex;
      for (var t = 1; t <= years; t++) s += annual / Math.pow(1 + r, t);
      return s;
    }
    var lo = -0.99, hi = 5;
    if (npv(lo) * npv(hi) > 0) return NaN;
    for (var i = 0; i < 200; i++) {
      var mid = (lo + hi) / 2;
      if (npv(lo) * npv(mid) <= 0) hi = mid; else lo = mid;
    }
    return (lo + hi) / 2;
  }

  /* ---------------------------------------------------------- tool 6 · H2 fuel-cell CHP */
  var H2_MODELS = [7.5, 10, 15, 20, 30, 50, 75, 100];

  function tool6() {
    var kw = val("t6_kw"), ch4pct = val("t6_ch4pct", 97), eff = val("t6_eff", 42),
        heat = val("t6_heat", 43), load = val("t6_load", 85), hours = val("t6_hours", 8000),
        capexKW = val("t6_capex", 10000), gasP = val("t6_gas"), tariff = val("t6_tariff"),
        heatP = val("t6_heatp"), omPct = val("t6_om", 3);

    var pick = H2_MODELS[H2_MODELS.length - 1];
    for (var i = 0; i < H2_MODELS.length; i++) {
      if (H2_MODELS[i] >= kw) { pick = H2_MODELS[i]; break; }
    }
    var share = kw > 0 ? pick / kw : 0;

    var fuel = eff > 0 ? pick / (eff / 100) : 0;
    var ch4 = fuel / CH4_KWH_PER_NM3;
    var raw = ch4pct > 0 ? ch4 / (ch4pct / 100) : 0;
    var heatKW = fuel * heat / 100;
    var hot = heatKW * 3600 / (4.18 * 50);
    var gen = pick * hours * load / 100;
    var heatYr = heatKW * hours * load / 100;
    var ch4yr = ch4 * hours * load / 100;

    var capex = pick * capexKW;
    var gasCost = ch4yr * gasP;
    var omCost = capex * omPct / 100;
    var revE = gen * tariff;
    var revH = heatYr * heatP;
    var net = revE + revH - gasCost - omCost;
    var payback = net > 0 ? capex / net : Infinity;
    var disc = 0.08;
    var npv = -capex;
    for (var t = 1; t <= 10; t++) npv += net / Math.pow(1 + disc, t);
    var r = net > 0 ? irr(capex, net, 10) : NaN;
    var crf = (disc * Math.pow(1 + disc, 10)) / (Math.pow(1 + disc, 10) - 1);
    var costKWh = gen > 0 ? (capex * crf + omCost + gasCost) / gen : 0;
    var co2 = gen / 1000 * 0.60;

    set("t6_model", (pick === 7.5 ? "7.5" : nf(pick, 0)) + " kW" + (share > 1.05 ? " × " + Math.ceil(share) + " units" : ""));
    set("t6_fuel", nf(fuel, 1) + " kW");
    set("t6_ch4", nf(ch4, 2) + " Nm³/h");
    set("t6_raw", nf(raw, 1) + " Nm³/h");
    set("t6_cyl", nf(ch4 * 24 / 10, 1) + " /day");
    set("t6_heatkw", nf(heatKW, 1) + " kW");
    set("t6_hot", nf(hot, 0) + " L/h");
    set("t6_total", nf(eff + heat, 0) + "%");
    set("t6_gen", nf(gen / 1000, 0) + " MWh/yr");
    set("t6_heatyr", nf(heatYr / 1000, 0) + " MWh/yr");
    set("t6_capexout", cny(capex, 1));
    set("t6_gascost", cny(gasCost, 1) + "/年");
    set("t6_omcost", cny(omCost, 1) + "/年");
    set("t6_rev", cny(revE + revH, 1) + "/年");
    set("t6_net", cny(net, 1) + "/年");
    set("t6_payback", isFinite(payback) ? nf(payback, 1) + " 年" : "无法回收");
    set("t6_npv", cny(npv, 1));
    set("t6_irr", isFinite(r) ? nf(r * 100, 1) + "%" : "n/a");
    set("t6_lcoe", "¥ " + nf(costKWh, 3) + "/kWh");
    set("t6_co2", nf(co2, 0) + " t/yr");

    var msgs = [];
    if (eff + heat > 90) msgs.push("Combined efficiency above 90% is not achievable for a reformer + fuel cell: check both assumptions.");
    if (eff > 48) msgs.push("Electrical efficiency above 48% assumes a large SOFC; a reformer + PEM/PAFC unit is 40–45%.");
    if (kw > 100) msgs.push("Above 100 kW this range stops — " + Math.ceil(share) + " units in parallel, or a gas-engine CHP.");
    if (kw > 0 && kw < 7.5) msgs.push("Below 7.5 kW the fixed balance-of-plant dominates the price — one shared unit for several houses is usually cheaper.");
    if (ch4pct < 90) msgs.push("燃料气甲烷低于 90%：需要一体化净化前处理，造价约 3.3 万元/kW，不能套用 1.72 万元/kW 的含前处理口径。");
    if (net <= 0) msgs.push("Negative annual benefit: fuel plus O&M costs more than the power and heat it replaces. Change the fuel cost or the avoided cost — nothing else in the model fixes it.");
    if (heatP === 0 && heatKW > 0) msgs.push("Heat is valued at zero: the 43% heat output is being thrown away, which is half the reason to buy a CHP.");
    if (tariff < 0.55 && gasP >= 2.0) msgs.push("有便宜市电、又按外购天然气计价时，这套账很难算平。产品适用于离网、电价高或沼气自产成本低的场景。");
    warn("t6_warn", msgs.join(" "));
  }

  /* ---------------------------------------------------------- tool 7 · BHP air-conditioning */
  var BHP_MODELS = [30, 60, 120, 240, 480];

  function tool7() {
    var cool = val("t7_cool"), cop = val("t7_cop", 1.0), ch4pct = val("t7_ch4pct", 97),
        load = val("t7_load", 85), hours = val("t7_hours", 8000),
        capexKW = val("t7_capex", 2500), gasP = val("t7_gas"),
        altType = ($("t7_alt") || {}).value || "grid",
        tariff = val("t7_tariff"), eerCop = val("t7_eercop", 3.0),
        heatP = val("t7_heatp"), omPct = val("t7_om", 3);

    var pick = BHP_MODELS[BHP_MODELS.length - 1];
    for (var i = 0; i < BHP_MODELS.length; i++) {
      if (BHP_MODELS[i] >= cool) { pick = BHP_MODELS[i]; break; }
    }
    var units = cool > 0 ? Math.ceil(cool / 480) : 1;
    var label = "BHP-" + pick;
    if (cool > 480) label = "BHP-480 × " + units;

    var fuel = cop > 0 ? cool / cop : 0;
    var ch4 = fuel / CH4_KWH_PER_NM3;
    var raw = ch4pct > 0 ? ch4 / (ch4pct / 100) : 0;
    var heatKW = fuel * 0.25;
    var hot = heatKW * 3600 / (4.18 * 50);
    var coolYr = cool * hours * load / 100;
    var fuelYr = ch4 * hours * load / 100;
    var heatYr = heatKW * hours * load / 100;

    var capex = cool * capexKW;
    var gasCost = fuelYr * gasP;
    var omCost = capex * omPct / 100;
    var altKWh = eerCop > 0 ? coolYr / eerCop : 0;
    var altCost = altKWh * tariff;
    var revH = heatYr * heatP;
    var saving = altCost + revH - gasCost - omCost;
    var payback = saving > 0 ? capex / saving : Infinity;
    var costKWh = coolYr > 0 ? (gasCost + omCost) / coolYr : 0;
    var altUnit = coolYr > 0 ? altCost / coolYr : 0;
    var co2 = altKWh / 1000 * 0.60;

    set("t7_model", label);
    set("t7_fuel", nf(fuel, 1) + " kW");
    set("t7_ch4", nf(ch4, 2) + " Nm³/h");
    set("t7_raw", nf(raw, 1) + " Nm³/h");
    set("t7_heatkw", nf(heatKW, 1) + " kW");
    set("t7_hot", nf(hot, 0) + " L/h");
    set("t7_coolyr", nf(coolYr / 1000, 0) + " MWh/yr");
    set("t7_fuelyr", nf(fuelYr, 0) + " Nm³/yr CH₄");
    set("t7_capexout", cny(capex, 1));
    set("t7_gascost", cny(gasCost, 1) + "/年");
    set("t7_omcost", cny(omCost, 1) + "/年");
    set("t7_altkwh", nf(altKWh, 0) + " kWh/yr");
    set("t7_altcost", cny(altCost, 1) + "/年");
    set("t7_saving", cny(saving, 1) + "/年");
    set("t7_payback", isFinite(payback) ? nf(payback, 1) + " 年" : "无法回收");
    set("t7_cost", "¥ " + nf(costKWh, 3) + "/kWh");
    set("t7_altunit", "¥ " + nf(altUnit, 3) + "/kWh");
    set("t7_co2", nf(co2, 0) + " t/yr");

    var msgs = [];
    if (cop > 1.2) msgs.push("Cooling COP above 1.2 on fuel LHV is optimistic for an engine-driven unit — check the guarantee sheet before quoting it.");
    if (altType === "grid" && tariff < 0.35) msgs.push("可靠市电低于 0.35 元/kWh 时，电空调买得便宜、用得也便宜，BHP 只有在无电、供电不稳或余热锅炉停机时才划算。");
    if (altType === "grid" && tariff <= 0.50) msgs.push("市电 0.35–0.50 元/kWh 属于临界区间：账要靠停机时仍能供冷来支撑，单靠省燃料费撑不住。");
    if (ch4pct < 90) msgs.push("Fuel gas below 90% methane: the engine must be derated and service intervals shorten. Price that in before comparing with a 97% biomethane case.");
    if (saving <= 0) msgs.push("No annual saving: at this fuel price the heat-pump cooling costs more to run than the system it replaces. Only availability (cooling with the grid down) justifies it.");
    warn("t7_warn", msgs.join(" "));
  }

  /* ---------------------------------------------------------- quick selector */
  var MODELS = [
    { kw: 500, ch4: 142 },
    { kw: 600, ch4: 172 },
    { kw: 700, ch4: 200 },
    { kw: 800, ch4: 228.6 },
    { kw: 1000, ch4: 286 }
  ];

  function quick() {
    var flow = val("q_flow"), ch4 = val("q_ch4", 60), load = val("q_load", 90);
    var eff = 0.352, heatFrac = 0.42;
    var availCH4 = flow * ch4 / 100;
    var pick = null;
    for (var i = 0; i < MODELS.length; i++) {
      if (MODELS[i].ch4 <= availCH4) pick = MODELS[i];
    }

    if (pick) {
      var needRaw = ch4 > 0 ? pick.ch4 / (ch4 / 100) : 0;
      var util = flow > 0 ? needRaw / flow * 100 : 0;
      var fuelKW = pick.ch4 * CH4_KWH_PER_NM3;
      set("q_model", pick.kw.toLocaleString("en-US") + " kW");
      set("q_need", nf(needRaw, 0) + " Nm³/h");
      set("q_util", nf(util, 0) + "%");
      set("q_out", nf(pick.kw, 0) + " kW");
      set("q_ann", nf(pick.kw * 8000 * load / 100 / 1000, 0) + " MWh/yr");
      set("q_heat", nf(fuelKW * heatFrac, 0) + " kW");
      set("q_ch4need", nf(pick.ch4, 0) + " Nm³/h");
    } else {
      var kW = availCH4 * CH4_KWH_PER_NM3 * eff;
      set("q_model", "< 500 kW");
      set("q_need", nf(flow, 0) + " Nm³/h (all gas)");
      set("q_util", "100%");
      set("q_out", nf(kW, 0) + " kW");
      set("q_ann", nf(kW * 8000 * load / 100 / 1000, 0) + " MWh/yr");
      set("q_heat", nf(availCH4 * CH4_KWH_PER_NM3 * heatFrac, 0) + " kW");
      set("q_ch4need", nf(availCH4, 0) + " Nm³/h");
    }

    var msgs = [];
    if (ch4 < 45) msgs.push("Methane below 45%: outside the engine fuel specification — the engine is derated and may not hold load.");
    if (pick && flow > 0 && pick.ch4 / (ch4 / 100) / flow < 0.75) msgs.push("Less than 75% of the available gas is used. A smaller unit, or a second unit later, will run more efficiently than one oversized engine.");
    warn("q_warn", msgs.join(" "));
  }

  /* ---------------------------------------------------------- wiring */
  var CALCS = { quick: quick, tool1: tool1, tool2: tool2, tool3: tool3, tool4: tool4, tool6: tool6, tool7: tool7 };

  function runAll() { Object.keys(CALCS).forEach(function (k) { CALCS[k](); }); }

  function bind() {
    document.querySelectorAll(".calc-form input, .calc-form select").forEach(function (el) {
      el.addEventListener("input", runAll);
      el.addEventListener("change", runAll);
    });

    var altSel = $("t7_alt");
    if (altSel) altSel.addEventListener("change", function () {
      var t = $("t7_tariff");
      if (t) t.value = altSel.value === "diesel" ? "2.20" : "0.65";
      runAll();
    });

    var modelSel = $("t2_model");
    if (modelSel) modelSel.addEventListener("change", function () {
      var kw = parseFloat(modelSel.value);
      var kwIn = $("t2_kw"), engineIn = $("t2_engine");
      if (isFinite(kw)) {
        if (kwIn) kwIn.value = kw;
        if (engineIn) engineIn.readOnly = true;
      } else if (engineIn) {
        engineIn.readOnly = false;
      }
      runAll();
    });

    document.querySelectorAll(".tab-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".tab-btn").forEach(function (b) { b.classList.remove("active"); });
        document.querySelectorAll(".tab-panel").forEach(function (p) { p.classList.remove("active"); });
        btn.classList.add("active");
        var panel = $(btn.dataset.tab);
        if (panel) panel.classList.add("active");
        if (history.replaceState) history.replaceState(null, "", "#" + btn.dataset.tab);
      });
    });
  }

  window.copySummary = function (which) {
    var panel = $(which);
    if (!panel) return;
    var lines = [];
    panel.querySelectorAll(".calc-form .field").forEach(function (f) {
      var label = f.querySelector("label");
      var input = f.querySelector("input, select");
      if (label && input) lines.push(label.textContent.trim() + ": " + input.value);
    });
    lines.push("—");
    panel.querySelectorAll(".calc-out .kv").forEach(function (kv) {
      var s = kv.querySelector("span"), b = kv.querySelector("b");
      if (s && b) lines.push(s.textContent.trim() + ": " + b.textContent.trim());
    });
    lines.push("");
    lines.push("KSTS K. S. Technical Services — indicative calculation, subject to measured site data.");
    var text = lines.join("\n");
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { alert("Summary copied to clipboard."); },
        function () { window.prompt("Copy the summary:", text); });
    } else {
      window.prompt("Copy the summary:", text);
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    bind();
    var h = (location.hash || "").replace("#", "");
    if (h && $(h) && $(h).classList.contains("tab-panel")) {
      var btn = document.querySelector('.tab-btn[data-tab="' + h + '"]');
      if (btn) btn.click();
    }
    runAll();
  });
})();
