# Changelog

## 2.0.0 — 2026-09-24

### Parameter database rebuilt with documented sources
- `modelos`: 15 models with version/identifier, energy coefficient (kWh per million tokens), source, reference date and notes. Coefficients derived from Jegham et al. (2025, arXiv:2505.09598v5) medium-prompt measurements and from Google (2025, arXiv:2508.15734). The previous database (10 models, no recorded sources) is retired.
- `factores_region`: Spain (CNMC 2026, data 2025), EU-27 (Ember 2023, data 2022), United States and world average (Ember 2025, data 2024). Each row carries data year and source.
- `equivalencias`: car km (EPA), streaming hours (IEA), smartphone charges (EPA), tree seedlings grown 10 years (EPA). "E-bike km" and "short-flight km" removed (unsourced and physically implausible factors).
- New table `tipos_tarea`: token budgets for simple / medium / complex educational tasks, calibrated on the programme portfolios.
- New table `metadata`: tool version and database build date.
- Full parameter listing with sources in `docs/PARAMETERS.md`.

### API
- `GET /task_types`, `GET /version` added.
- `POST /calculate` and `POST /compare` accept `task_type` (`simple` | `medium` | `complex`) as an alternative to explicit token counts; explicit tokens still work and take precedence.
- Results now include the two parameters applied (`kwh_por_millon_tokens`, `intensidad_carbono_kg_kwh`) for traceability.

### Frontend
- API base URL moved to `frontend/config.js` (`window.CC_API`), the only place to edit when deploying. Pages show a visible error banner with the attempted URL if the API is unreachable, and still load models/regions when an older backend without `/task_types` is running.
- Calculator and Comparator: task-type selector that pre-fills (editable) input/output tokens.
- ES/EN language switch (button in the navigation bar) on all four pages, implemented in `frontend/i18n.js`; the choice is remembered in the browser. All interface strings, including model suffixes, region names, task types and equivalences returned by the API, are translated on the fly.

### Reproducibility
- `scripts/case_study.py` recomputes the paper's case study (Table I, worked example, sensitivity scenarios, web-search comparison, equivalences) with the same functions the API uses. Output in `docs/case_study_v2.md`.

### Housekeeping
- `requirements.txt` now lists the real dependencies (FastAPI, uvicorn, pydantic); Flask and tiktoken were never used.
- `LICENSE` (GPL-3.0-or-later), `CITATION.cff`, this changelog.
- `setup_database.py` regenerates the DB from `data/` and starts with an empty `consultas_log`.

## 1.0.0 — 2026-03-12
- Initial version (backend FastAPI, frontend HTML/JS, SQLite database).
