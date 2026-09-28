"""
scripts/case_study.py

Recalcula el caso de estudio del articulo (programa de 6 semanas, 16 estudiantes,
dic-2025 a feb-2026) con el propio codigo de la calculadora (backend.calculations),
de modo que cualquier lector puede reproducir la Tabla I, el ejemplo trabajado y
el analisis de sensibilidad ejecutando:

    python -m scripts.case_study

Datos de entrada (derivados de los portafolios del programa):
  - interacciones por estudiante y semana
  - tokens por interaccion segun la categoria de la tarea
  - mezcla de modelos: 50 % ChatGPT (GPT-5), 25 % Claude (Sonnet 4.5), 25 % Gemini (2.5 Flash)
"""
from backend.calculations import calculate_co2, get_equivalences
from backend.database import get_model_by_id, get_region_factor, get_metadata

N_STUDENTS = 16
REGION = "España"

# id_modelo en la BD v2.0
GPT5_MIN, GPT5_HIGH, GPT41_NANO, CLAUDE_45, GEMINI_25F = 1, 2, 6, 8, 11

MIX_CENTRAL = {GPT5_MIN: 0.50, CLAUDE_45: 0.25, GEMINI_25F: 0.25}
MIX_EQUAL   = {GPT5_MIN: 1/3, CLAUDE_45: 1/3, GEMINI_25F: 1/3}
MIX_HIGH    = {GPT5_HIGH: 0.50, CLAUDE_45: 0.25, GEMINI_25F: 0.25}
MIX_LIGHT   = {GPT41_NANO: 1.0}

# semana, dimension, categoria, interacciones/estudiante, tokens/interaccion
WEEKS = [
    (1, "Prompt engineering",        "Medium",         50, 2500),
    (2, "Bias and hallucinations",   "Medium",         40, 2000),
    (3, "Teaching planning",         "Complex",        30, 4700),
    (4, "Diversity and inclusion",   "Medium-complex", 35, 3000),
    (5, "Assessment design",         "Complex",        30, 4200),
    (6, "Sustainability",            "Simple-medium",  25, 1600),
]

def week_tokens(w):
    _, _, _, inter, tok = w
    return inter * N_STUDENTS * tok

def co2_for(tokens, mix, region=REGION):
    """CO2 (kg) de un volumen de tokens repartido entre modelos segun mix."""
    total = 0.0
    for mid, share in mix.items():
        r = calculate_co2(tokens_input=int(round(tokens * share)), tokens_output=0,
                          model_id=mid, region=region)
        total += r["co2_kg"]
    return total

def blended_coefficient(mix):
    return sum(get_model_by_id(m)["kwh_por_millon_tokens"] * s for m, s in mix.items())

def fmt(x, d=2):
    return f"{x:.{d}f}"

def main():
    meta = get_metadata()
    ci = get_region_factor(REGION)
    lines = []
    P = lines.append
    P(f"# Case study recomputed with the calculator v{meta['tool_version']} (DB built {meta['db_build_date']})\n")
    P(f"Region: {REGION} ({ci} kg CO2e/kWh). Students: {N_STUDENTS}. Model mix (central): "
      f"50 % GPT-5 minimal, 25 % Claude Sonnet 4.5 (proxy Claude 3.7 Sonnet), 25 % Gemini 2.5 Flash.\n")
    P(f"Blended coefficient (central mix): {blended_coefficient(MIX_CENTRAL):.3f} kWh per million tokens\n")

    # ---------- Table I ----------
    P("## Table I - Weekly emissions (central scenario)\n")
    P("| Wk | Dimension | Task type | Int./student | Tokens/int. | Tokens total (M) | kWh | CO2e total (kg) | CO2e/student (kg) | % |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    tot_tok = tot_co2 = tot_kwh = 0.0
    rows = []
    for w in WEEKS:
        tk = week_tokens(w)
        co2 = co2_for(tk, MIX_CENTRAL)
        kwh = tk * blended_coefficient(MIX_CENTRAL) / 1e6
        rows.append((w, tk, kwh, co2))
        tot_tok += tk; tot_co2 += co2; tot_kwh += kwh
    for (w, tk, kwh, co2) in rows:
        P(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} | {w[4]:,} | {tk/1e6:.2f} | {kwh:.2f} | {co2:.2f} | {co2/N_STUDENTS:.3f} | {100*co2/tot_co2:.0f} % |")
    P(f"| **Total** | | | **{sum(w[3] for w in WEEKS)}** | | **{tot_tok/1e6:.2f}** | **{tot_kwh:.2f}** | **{tot_co2:.2f}** | **{tot_co2/N_STUDENTS:.3f}** | 100 % |\n")

    # ---------- Worked example ----------
    w3 = WEEKS[2]; tk3 = week_tokens(w3); co2_3 = co2_for(tk3, MIX_CENTRAL)
    P("## Worked example - Week 3\n")
    P(f"{w3[3]} interactions/student x {N_STUDENTS} students = {w3[3]*N_STUDENTS} interactions x {w3[4]:,} tokens = {tk3/1e6:.2f} M tokens.")
    P(f"Energy = {tk3/1e6:.2f} M tokens x {blended_coefficient(MIX_CENTRAL):.3f} kWh/M tokens = {tk3*blended_coefficient(MIX_CENTRAL)/1e6:.2f} kWh.")
    P(f"Emissions = {tk3*blended_coefficient(MIX_CENTRAL)/1e6:.2f} kWh x {ci} kg CO2e/kWh = {co2_3:.2f} kg CO2e.\n")

    # ---------- Sensitivity ----------
    P("## Sensitivity analysis (programme total, kg CO2e)\n")
    P("| Scenario | Assumption changed | Blended coeff. (kWh/M tok) | Total kg CO2e | Ratio to central |")
    P("|---|---|---|---|---|")
    scen = [
        ("Central", "observed mix, Spain grid", MIX_CENTRAL, REGION),
        ("Light models", "all interactions via GPT-4.1 nano (most efficient documented commercial model)", MIX_LIGHT, REGION),
        ("Equal mix", "1/3 each model", MIX_EQUAL, REGION),
        ("High reasoning", "ChatGPT share routed to GPT-5 high-reasoning mode", MIX_HIGH, REGION),
        ("EU grid", "central mix, EU-27 average", MIX_CENTRAL, "Europa"),
        ("US grid", "central mix, United States", MIX_CENTRAL, "USA"),
        ("Global grid", "central mix, world average", MIX_CENTRAL, "Global"),
    ]
    results = {}
    for name, desc, mix, reg in scen:
        t = sum(co2_for(week_tokens(w), mix, reg) for w in WEEKS)
        results[name] = t
        P(f"| {name} | {desc} | {blended_coefficient(mix):.3f} | {t:.2f} | {t/tot_co2:.2f} |")
    P("")
    P(f"Range across scenarios: {min(results.values()):.2f} - {max(results.values()):.2f} kg CO2e (central {tot_co2:.2f}).")
    P(f"Light-model reduction vs central: {100*(1-results['Light models']/tot_co2):.0f} %.\n")

    # ---------- Web search comparison ----------
    searches = 40 * 6 * N_STUDENTS
    wh_per_search = 0.30   # Wh, Google search, as cited in Jegham et al. 2025
    ws_kwh = searches * wh_per_search / 1000
    ws_co2 = ws_kwh * ci
    P("## Conventional web search comparison\n")
    P(f"Assumption: 40 searches/student/week x 6 weeks x {N_STUDENTS} students = {searches:,} searches x {wh_per_search} Wh/search "
      f"= {ws_kwh:.2f} kWh x {ci} kg/kWh = {ws_co2:.2f} kg CO2e (server-side only; device energy excluded from both scenarios).")
    P(f"AI-assisted programme (central) / web search = {tot_co2/ws_co2:.1f}x.\n")

    # ---------- Equivalences ----------
    P("## Equivalences for the programme total (central)\n")
    for k, v in get_equivalences(tot_co2).items():
        P(f"- {k}: {v}")
    P(f"- per student: {tot_co2/N_STUDENTS:.3f} kg CO2e = "
      f"{get_equivalences(tot_co2/N_STUDENTS)['km en coche de gasolina medio']} km by car")
    out = "\n".join(lines)
    print(out)
    with open("docs/case_study_v2.md", "w", encoding="utf-8") as f:
        f.write(out + "\n")

if __name__ == "__main__":
    main()
