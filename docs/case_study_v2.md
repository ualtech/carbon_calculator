# Case study recomputed with the calculator v2.0.0 (DB built 2026-09-24)

Region: España (0.258 kg CO2e/kWh). Students: 16. Model mix (central): 50 % GPT-5 minimal, 25 % Claude Sonnet 4.5 (proxy Claude 3.7 Sonnet), 25 % Gemini 2.5 Flash.

Blended coefficient (central mix): 1.106 kWh per million tokens

## Table I - Weekly emissions (central scenario)

| Wk | Dimension | Task type | Int./student | Tokens/int. | Tokens total (M) | kWh | CO2e total (kg) | CO2e/student (kg) | % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Prompt engineering | Medium | 50 | 2,500 | 2.00 | 2.21 | 0.57 | 0.036 | 20 % |
| 2 | Bias and hallucinations | Medium | 40 | 2,000 | 1.28 | 1.42 | 0.37 | 0.023 | 13 % |
| 3 | Teaching planning | Complex | 30 | 4,700 | 2.26 | 2.50 | 0.64 | 0.040 | 23 % |
| 4 | Diversity and inclusion | Medium-complex | 35 | 3,000 | 1.68 | 1.86 | 0.48 | 0.030 | 17 % |
| 5 | Assessment design | Complex | 30 | 4,200 | 2.02 | 2.23 | 0.58 | 0.036 | 20 % |
| 6 | Sustainability | Simple-medium | 25 | 1,600 | 0.64 | 0.71 | 0.18 | 0.011 | 6 % |
| **Total** | | | **210** | | **9.87** | **10.92** | **2.82** | **0.176** | 100 % |

## Worked example - Week 3

30 interactions/student x 16 students = 480 interactions x 4,700 tokens = 2.26 M tokens.
Energy = 2.26 M tokens x 1.106 kWh/M tokens = 2.50 kWh.
Emissions = 2.50 kWh x 0.258 kg CO2e/kWh = 0.64 kg CO2e.

## Sensitivity analysis (programme total, kg CO2e)

| Scenario | Assumption changed | Blended coeff. (kWh/M tok) | Total kg CO2e | Ratio to central |
|---|---|---|---|---|
| Central | observed mix, Spain grid | 1.106 | 2.82 | 1.00 |
| Light models | all interactions via GPT-4.1 nano (most efficient documented commercial model) | 0.288 | 0.73 | 0.26 |
| Equal mix | 1/3 each model | 1.087 | 2.77 | 0.98 |
| High reasoning | ChatGPT share routed to GPT-5 high-reasoning mode | 4.811 | 12.25 | 4.35 |
| EU grid | central mix, EU-27 average | 1.106 | 2.78 | 0.99 |
| US grid | central mix, United States | 1.106 | 4.19 | 1.49 |
| Global grid | central mix, world average | 1.106 | 5.17 | 1.83 |

Range across scenarios: 0.73 - 12.25 kg CO2e (central 2.82).
Light-model reduction vs central: 74 %.

## Conventional web search comparison

Assumption: 40 searches/student/week x 6 weeks x 16 students = 3,840 searches x 0.3 Wh/search = 1.15 kWh x 0.258 kg/kWh = 0.30 kg CO2e (server-side only; device energy excluded from both scenarios).
AI-assisted programme (central) / web search = 9.5x.

## Equivalences for the programme total (central)

- km en coche de gasolina medio: 11.538
- horas de streaming de video: 78.2727
- cargas completas de smartphone: 227.2388
- plantones de arbol creciendo 10 anos: 0.047
- per student: 0.176 kg CO2e = 0.7211 km by car
