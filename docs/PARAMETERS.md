# Parameter database - AI Carbon Footprint Calculator v2.0.0

All parameters used by the calculator, with their source and reference date. This file is generated from the SQLite database (`carbon_calculator.db`), which in turn is built from the CSV files in `data/`. It corresponds to Table II of the paper.

Calculation model: `CO2e (kg) = N_tokens x (E_Mtoken / 1e6) x CI_grid`, where N_tokens = input + output tokens, E_Mtoken = model energy in kWh per million tokens, CI_grid = grid carbon intensity in kg CO2e/kWh.

## A. Model energy coefficients (kWh per million tokens)

Coefficients derived from per-query energy measurements in Jegham et al. (2025) for the *medium* prompt configuration (1,000 input + 1,000 output tokens): E_Mtoken = Wh_medium / 2,000 tokens x 1,000. This configuration matches the typical interaction size observed in the case study (1,600-4,700 tokens). Models marked with * were used in the case study.

| id | Model | Provider | Version / identifier | kWh per M tokens | Source | Ref. date | Notes |
|---|---|---|---|---|---|---|---|
| 1 | GPT-5 (razonamiento minimo)* | OpenAI | gpt-5, modo minimal (routing por defecto en ChatGPT) | 1.165 | Jegham et al. 2025 (arXiv:2505.09598v5), Sec. 7, prompt medio 2.33 Wh / 2000 tokens | 2025-11 | Modelo por defecto de ChatGPT (nivel gratuito) entre dic-2025 y feb-2026 |
| 2 | GPT-5 (razonamiento alto) | OpenAI | gpt-5, modo high | 8.575 | Jegham et al. 2025 (arXiv:2505.09598v5), Sec. 7, prompt medio 17.15 Wh / 2000 tokens | 2025-11 | Escenario alto: consultas enrutadas al modo de razonamiento |
| 3 | GPT-4o | OpenAI | gpt-4o (mar-2025) | 0.608 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 1.215 Wh / 2000 tokens | 2025-11 |  |
| 4 | GPT-4.1 | OpenAI | gpt-4.1 | 1.581 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 3.161 Wh / 2000 tokens | 2025-11 |  |
| 5 | GPT-4.1 mini | OpenAI | gpt-4.1-mini | 0.773 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 1.545 Wh / 2000 tokens | 2025-11 |  |
| 6 | GPT-4.1 nano | OpenAI | gpt-4.1-nano | 0.288 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 0.575 Wh / 2000 tokens | 2025-11 | Modelo comercial mas eficiente documentado |
| 7 | o3 | OpenAI | o3 | 2.577 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 5.153 Wh / 2000 tokens | 2025-11 | Modelo de razonamiento |
| 8 | Claude Sonnet 4.5* | Anthropic | claude-sonnet-4-5 (proxy: Claude 3.7 Sonnet) | 1.495 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, Claude 3.7 Sonnet, prompt medio 2.989 Wh / 2000 tokens | 2025-11 | Proxy documentado: misma clase de tamano (Large) y misma infraestructura (AWS) que Claude 3.7 Sonnet. Modelo gratuito de Claude entre dic-2025 y feb-2026 |
| 9 | Claude 3.7 Sonnet | Anthropic | claude-3-7-sonnet | 1.495 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 2.989 Wh / 2000 tokens | 2025-11 |  |
| 10 | Claude 3.5 Haiku | Anthropic | claude-3-5-haiku | 2.232 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 4.464 Wh / 2000 tokens | 2025-11 |  |
| 11 | Gemini 2.5 Flash* | Google | gemini-2.5-flash (Gemini Apps) | 0.600 | Google 2025 (arXiv:2508.15734): 0.24 Wh por prompt mediano de texto |  hipotesis de los autores: 400 tokens por prompt mediano (config. corta de Jegham et al.) | 1 |
| 12 | DeepSeek-V3 (Azure) | DeepSeek | deepseek-v3 alojado en Microsoft Azure | 1.083 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 2.165 Wh / 2000 tokens | 2025-11 |  |
| 13 | DeepSeek-R1 (Azure) | DeepSeek | deepseek-r1 alojado en Microsoft Azure | 2.166 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 4.331 Wh / 2000 tokens | 2025-11 | Modelo de razonamiento |
| 14 | LLaMA-3.3 70B | Meta | llama-3.3-70b (AWS) | 0.380 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 0.760 Wh / 2000 tokens | 2025-11 | Modelo abierto |
| 15 | LLaMA-3.1 8B | Meta | llama-3.1-8b (AWS) | 0.086 | Jegham et al. 2025 (arXiv:2505.09598v5), Tabla 4, prompt medio 0.172 Wh / 2000 tokens | 2025-11 | Modelo abierto mas eficiente del benchmark |

## B. Grid carbon intensity (kg CO2e/kWh)

| id | Region | kg CO2e/kWh | Data year | Source |
|---|---|---|---|---|
| 1 | España | 0.258 | 2025 | CNMC, Etiquetado de la electricidad: energia producida en 2025 (mix nacional 258 gCO2eq/kWh), Madrid, 2026 |
| 2 | Europa | 0.255 | 2022 | Ember, European Electricity Review 2023 (UE-27, 255 gCO2/kWh en 2022) |
| 3 | USA | 0.384 | 2024 | Ember, Global Electricity Review 2025 (Estados Unidos, 384 gCO2/kWh en 2024) |
| 4 | Global | 0.473 | 2024 | Ember, Global Electricity Review 2025 (media mundial, 473 gCO2/kWh en 2024) |

The region selected by the user is used as a proxy for the electricity mix of the data centre serving the request, because providers do not disclose the location of the infrastructure handling individual queries.

## C. Token budgets by task type

| Type | Label | Input tokens | Output tokens | Total | Description | Source |
|---|---|---|---|---|---|---|
| simple | Simple (pregunta directa) | 300 | 700 | 1000 | Consulta breve con respuesta corta: definicion, aclaracion, pregunta factual | Calibrado por los autores sobre los portafolios del programa (dic-2025 a feb-2026): ~1000 tokens por interaccion |
| medium | Media (diseno de actividad) | 700 | 1550 | 2250 | Peticion con contexto y respuesta elaborada: diseno de una actividad, resumen, comparacion, revision de un texto | Calibrado por los autores sobre los portafolios del programa: 2000-2500 tokens por interaccion |
| complex | Compleja (unidad o planificacion completa) | 1300 | 3200 | 4500 | Prompt largo con instrucciones en varias fases y salida extensa: planificacion completa, rubricas, secuencias de unidad | Calibrado por los autores sobre los portafolios del programa: 4200-4700 tokens por interaccion |

## D. Equivalences (units per kg CO2e)

| Equivalence | Factor | Unit | Source |
|---|---|---|---|
| km en coche de gasolina medio | 4.095 | km | US EPA, Greenhouse Gas Equivalencies Calculator (3.93e-4 t CO2e por milla = 0.244 kg CO2e/km) |
| horas de streaming de video | 27.78 | horas | IEA 2020, The carbon footprint of streaming video: fact-checking the headlines (36 gCO2 por hora, media mundial 2019) |
| cargas completas de smartphone | 80.65 | cargas | US EPA, Greenhouse Gas Equivalencies Calculator (1.24e-5 t CO2 por carga) |
| plantones de arbol creciendo 10 anos | 0.01667 | plantones | US EPA, Greenhouse Gas Equivalencies Calculator (0.060 t CO2 secuestradas por planton en 10 anos) |

## E. References

- N. Jegham, M. Abdelatti, C. Y. Koh, L. Elmoubarki, and A. Hendawi, "How hungry is AI? Benchmarking energy, water, and carbon footprint of LLM inference," arXiv:2505.09598v5, Nov. 2025.
- C. Elsworth et al. (Google), "Measuring the environmental impact of delivering AI at Google scale," arXiv:2508.15734, Aug. 2025.
- Comision Nacional de los Mercados y la Competencia (CNMC), "Etiquetado de la electricidad: energia producida en 2025," Madrid, Spain, 2026.
- Ember, "European Electricity Review 2023," London, U.K., 2023.
- Ember, "Global Electricity Review 2025," London, U.K., 2025.
- U.S. Environmental Protection Agency, "Greenhouse Gas Equivalencies Calculator - Calculations and References," 2025.
- International Energy Agency, "The carbon footprint of streaming video: fact-checking the headlines," IEA, Paris, 2020.
