/* i18n.js — conmutador ES/EN para las páginas del Carbon Calculator.
   Uso: elementos con data-i18n="clave" (texto), data-i18n-html="clave" (HTML),
   data-i18n-ph="clave" (placeholder). Las cadenas que llegan de la API
   (regiones, tipos de tarea, equivalencias, sufijos de modelo) se traducen
   con las funciones tRegion(), tTask(), tEquiv(), tModel(). */
(function () {
  const DICT = {
    es: {
      nav_calc: "Calcular", nav_cmp: "Comparar", nav_sim: "Simular",
      // index
      hero_badge: "🌿 HUELLA DE CARBONO · IA",
      hero_h1: 'Mide el impacto <span class="accent-green">ambiental</span> de la<br/><span class="accent-orange">inteligencia artificial</span>',
      card_calc_h: "Calculadora", card_calc_p: "Calcula el CO₂ de una consulta a cualquier modelo de IA según región y tokens.", card_calc_l: "CALCULAR →",
      card_cmp_h: "Comparador", card_cmp_p: "Compara dos escenarios distintos y descubre cuál tiene menor huella de carbono.", card_cmp_l: "COMPARAR →",
      card_sim_h: "Simulador de Aula", card_sim_p: "Simula el impacto colectivo de un grupo de estudiantes usando IA durante semanas.", card_sim_l: "SIMULAR →",
      stat_models: "MODELOS DE IA", stat_equiv: "EQUIVALENCIAS", stat_kg: "EN KG / CONSULTA", stat_sims: "POSIBLES SIMULACIONES",
      foot_params: "parámetros y fuentes",
      hero_sub: "Calcula, compara y simula el CO₂ generado por tus consultas a modelos de IA. Toma decisiones más sostenibles.",
      foot_github: "Ver código en GitHub",
      foot_group: "Grupo de Investigación TIC 221 Computación, Optimización y Sensorización en Ingeniería y Energía",
      // calculadora
      calc_badge: "⚡ CALCULADORA", calc_h1: "Calcula tu <span>huella</span>",
      calc_sub: "Introduce los parámetros de tu consulta y obtén el CO₂ generado al instante.",
      p_model: "// PARÁMETROS DEL MODELO", l_model: "MODELO DE IA", l_region: "REGIÓN", p_tokens: "// TOKENS",
      l_task: "TIPO DE TAREA (rellena los tokens; puedes editarlos)", opt_manual: "— Introducir tokens manualmente —",
      l_tin: "TOKENS DE ENTRADA", l_tout: "TOKENS DE SALIDA", ph_tin: "ej: 1000", ph_tout: "ej: 500",
      btn_calc: "CALCULAR CO₂", loading_calc: "⏳ Calculando...",
      r_result: "// RESULTADO", r_kg: "KG DE CO₂", r_kwh: "KWH CONSUMIDOS", r_tokens: "TOKENS TOTALES", r_equiv: "// EQUIVALENCIAS",
      // comparador
      cmp_badge: "⚖️ COMPARADOR", cmp_h1: "Compara dos <span>escenarios</span>",
      cmp_sub: "¿GPT-5 o Gemini? ¿España o Europa? Descubre qué combinación emite menos CO₂.",
      p_s1: "// ESCENARIO 1", p_s2: "// ESCENARIO 2", l_model_s: "MODELO", l_task_s: "TIPO DE TAREA", opt_manual_s: "— Tokens manuales —",
      l_tin_s: "TOKENS ENTRADA", l_tout_s: "TOKENS SALIDA", btn_cmp: "COMPARAR ESCENARIOS", loading_cmp: "⏳ Comparando...",
      d_co2: "DIFERENCIA CO₂", d_pct: "DIFERENCIA %", d_res: "RESULTADO", win1: "🏆 Escenario 1 gana", win2: "🏆 Escenario 2 gana", tie: "🤝 Empate",
      // simulador
      sim_badge: "🏫 SIMULADOR DE AULA", sim_h1: "Simula el impacto <span>colectivo</span>",
      sim_sub: "Define el número de estudiantes, las actividades con IA y la duración. Descubre el CO₂ total del aula.",
      p_general: "// CONFIGURACIÓN GENERAL", l_students: "Nº DE ESTUDIANTES", ph_students: "ej: 30",
      h_acts: "ACTIVIDADES", btn_add: "+ AÑADIR ACTIVIDAD", btn_sim: "SIMULAR IMPACTO DEL AULA", loading_sim: "⏳ Simulando...",
      act_prefix: "ACT", l_act_name: "NOMBRE ACTIVIDAD", ph_act_name: "ej: Redacción con IA", l_tokens_student: "TOKENS/ALUMNO",
      l_freq: "FRECUENCIA", f_daily: "Diaria", f_weekly: "Semanal", f_monthly: "Mensual", l_weeks: "SEMANAS", act_default: "Actividad",
      s_kg_total: "KG CO₂ TOTAL", s_kg_student: "KG CO₂ / ALUMNO", s_students: "ESTUDIANTES",
      s_equiv_total: "// EQUIVALENCIAS TOTALES", s_breakdown: "// DESGLOSE POR ACTIVIDAD", bk_co2: "CO₂ TOTAL", bk_tokens: "TOKENS",
      // datos de la API
      region: { "España": "España", "Europa": "Europa (UE-27)", "USA": "Estados Unidos", "Global": "Global" },
      task: { simple: "Simple (pregunta directa)", medium: "Media (diseño de actividad)", complex: "Compleja (unidad o planificación completa)" },
      equiv: {
        "km en coche de gasolina medio": "km en coche de gasolina medio",
        "horas de streaming de video": "horas de streaming de vídeo",
        "cargas completas de smartphone": "cargas completas de smartphone",
        "plantones de arbol creciendo 10 anos": "plantones de árbol creciendo 10 años"
      },
      model: { "(razonamiento minimo)": "(razonamiento mínimo)", "(razonamiento alto)": "(razonamiento alto)" },
      tokens_word: "tokens"
    },
    en: {
      nav_calc: "Calculate", nav_cmp: "Compare", nav_sim: "Simulate",
      hero_badge: "🌿 CARBON FOOTPRINT · AI",
      hero_h1: 'Measure the <span class="accent-green">environmental</span> impact of<br/><span class="accent-orange">artificial intelligence</span>',
      card_calc_h: "Calculator", card_calc_p: "Estimate the CO₂ of a single query to any AI model, by region and token count.", card_calc_l: "CALCULATE →",
      card_cmp_h: "Comparator", card_cmp_p: "Compare two scenarios side by side and find out which has the lower carbon footprint.", card_cmp_l: "COMPARE →",
      card_sim_h: "Classroom Simulator", card_sim_p: "Simulate the collective impact of a group of students using AI over several weeks.", card_sim_l: "SIMULATE →",
      stat_models: "AI MODELS", stat_equiv: "EQUIVALENCES", stat_kg: "IN KG / QUERY", stat_sims: "POSSIBLE SIMULATIONS",
      foot_params: "parameters and sources",
      hero_sub: "Calculate, compare and simulate the CO₂ generated by your queries to AI models. Make more sustainable decisions.",
      foot_github: "View source code on GitHub",
      foot_group: "TIC 221 Research Group — Computing, Optimisation and Sensing in Engineering and Energy",
      calc_badge: "⚡ CALCULATOR", calc_h1: "Calculate your <span>footprint</span>",
      calc_sub: "Enter the parameters of your query and get the CO₂ generated instantly.",
      p_model: "// MODEL PARAMETERS", l_model: "AI MODEL", l_region: "REGION", p_tokens: "// TOKENS",
      l_task: "TASK TYPE (pre-fills the tokens; you can edit them)", opt_manual: "— Enter tokens manually —",
      l_tin: "INPUT TOKENS", l_tout: "OUTPUT TOKENS", ph_tin: "e.g. 1000", ph_tout: "e.g. 500",
      btn_calc: "CALCULATE CO₂", loading_calc: "⏳ Calculating...",
      r_result: "// RESULT", r_kg: "KG OF CO₂", r_kwh: "KWH CONSUMED", r_tokens: "TOTAL TOKENS", r_equiv: "// EQUIVALENCES",
      cmp_badge: "⚖️ COMPARATOR", cmp_h1: "Compare two <span>scenarios</span>",
      cmp_sub: "GPT-5 or Gemini? Spain or the EU? Find out which combination emits less CO₂.",
      p_s1: "// SCENARIO 1", p_s2: "// SCENARIO 2", l_model_s: "MODEL", l_task_s: "TASK TYPE", opt_manual_s: "— Manual tokens —",
      l_tin_s: "INPUT TOKENS", l_tout_s: "OUTPUT TOKENS", btn_cmp: "COMPARE SCENARIOS", loading_cmp: "⏳ Comparing...",
      d_co2: "CO₂ DIFFERENCE", d_pct: "DIFFERENCE %", d_res: "RESULT", win1: "🏆 Scenario 1 wins", win2: "🏆 Scenario 2 wins", tie: "🤝 Tie",
      sim_badge: "🏫 CLASSROOM SIMULATOR", sim_h1: "Simulate the <span>collective</span> impact",
      sim_sub: "Set the number of students, the AI-supported activities and their duration. Discover the total CO₂ of the classroom.",
      p_general: "// GENERAL SETTINGS", l_students: "NUMBER OF STUDENTS", ph_students: "e.g. 30",
      h_acts: "ACTIVITIES", btn_add: "+ ADD ACTIVITY", btn_sim: "SIMULATE CLASSROOM IMPACT", loading_sim: "⏳ Simulating...",
      act_prefix: "ACT", l_act_name: "ACTIVITY NAME", ph_act_name: "e.g. Writing with AI", l_tokens_student: "TOKENS/STUDENT",
      l_freq: "FREQUENCY", f_daily: "Daily", f_weekly: "Weekly", f_monthly: "Monthly", l_weeks: "WEEKS", act_default: "Activity",
      s_kg_total: "KG CO₂ TOTAL", s_kg_student: "KG CO₂ / STUDENT", s_students: "STUDENTS",
      s_equiv_total: "// TOTAL EQUIVALENCES", s_breakdown: "// BREAKDOWN BY ACTIVITY", bk_co2: "CO₂ TOTAL", bk_tokens: "TOKENS",
      region: { "España": "Spain", "Europa": "EU-27 average", "USA": "United States", "Global": "World average" },
      task: { simple: "Simple (direct question)", medium: "Medium (activity design)", complex: "Complex (full unit or lesson plan)" },
      equiv: {
        "km en coche de gasolina medio": "km driven by an average gasoline car",
        "horas de streaming de video": "hours of video streaming",
        "cargas completas de smartphone": "full smartphone charges",
        "plantones de arbol creciendo 10 anos": "tree seedlings grown for 10 years"
      },
      model: { "(razonamiento minimo)": "(minimal reasoning)", "(razonamiento alto)": "(high reasoning)" },
      tokens_word: "tokens"
    }
  };

  let lang = localStorage.getItem("cc_lang") || "es";

  function t(key) { return (DICT[lang] && DICT[lang][key]) ?? DICT.es[key] ?? key; }
  function tRegion(name) { return DICT[lang].region[name] || name; }
  function tTask(tipo, fallback) { return DICT[lang].task[tipo] || fallback; }
  function tEquiv(name) { return DICT[lang].equiv[name] || name; }
  function tModel(name) {
    let out = name;
    for (const [k, v] of Object.entries(DICT[lang].model)) out = out.replace(k, v);
    return out;
  }

  function applyLang() {
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll("[data-i18n-html]").forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
    const btn = document.getElementById("langToggle");
    if (btn) btn.textContent = lang === "es" ? "EN" : "ES";
    if (typeof window.onLangChange === "function") window.onLangChange();
  }

  function toggleLang() {
    lang = lang === "es" ? "en" : "es";
    localStorage.setItem("cc_lang", lang);
    applyLang();
  }

  function injectToggle() {
    const ul = document.querySelector("nav ul");
    if (!ul || document.getElementById("langToggle")) return;
    const li = document.createElement("li");
    li.innerHTML = '<button id="langToggle" type="button" onclick="toggleLang()">EN</button>';
    ul.appendChild(li);
    const st = document.createElement("style");
    st.textContent = "#langToggle{background:transparent;border:1px solid currentColor;color:inherit;font:inherit;font-size:0.75rem;letter-spacing:0.1em;padding:0.25rem 0.6rem;border-radius:999px;cursor:pointer;opacity:0.85}#langToggle:hover{opacity:1}";
    document.head.appendChild(st);
  }

  window.t = t; window.tRegion = tRegion; window.tTask = tTask; window.tEquiv = tEquiv; window.tModel = tModel;
  window.toggleLang = toggleLang; window.applyLang = applyLang; window.getLang = () => lang;

  document.addEventListener("DOMContentLoaded", () => { injectToggle(); applyLang(); });
})();
