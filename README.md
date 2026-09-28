# AI Carbon Footprint Calculator (v2.0.0)

Web tool to estimate and compare the carbon footprint of the educational use of generative AI.
Live instance: https://www.ualtech.es/projects/carbon_calculator/ · Universidad de Almería.

Three modes: **Calculator** (one interaction), **Comparator** (two scenarios side by side) and **Classroom Simulator** (a whole course: students × activities × weeks).

## Calculation model

    CO2e (kg) = N_tokens × (E_Mtoken / 10⁶) × CI_grid

- `N_tokens`: input + output tokens of the interaction (entered directly, or pre-filled from a task type).
- `E_Mtoken`: model energy coefficient in kWh per million tokens (table `modelos`).
- `CI_grid`: carbon intensity of the selected region in kg CO2e/kWh (table `factores_region`), used as a proxy for the data-centre mix.

Every parameter (model coefficients, regional factors, token budgets, equivalences) is stored with its source and reference date. See **`docs/PARAMETERS.md`**.

## Structure

- `backend/` — FastAPI API and pure calculation logic (`calculations.py`)
- `frontend/` — static HTML/JS pages (`index.html`, `calculate.html`, `compare.html`, `simulate.html`) and `i18n.js` (ES/EN switch)
- `data/` — CSV sources of the parameter database
- `docs/` — API description, parameter table with sources, case-study output
- `scripts/case_study.py` — reproduces the paper's case study with the calculator code

## Run locally

```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
python -m backend.setup_database                      # builds carbon_calculator.db from data/
uvicorn backend.app:app --reload                      # API at http://localhost:8000
```

Open `frontend/index.html` in a browser. The pages read the API base URL from `frontend/config.js` (`window.CC_API`, default `http://localhost:8000`): when deploying, set it to the public URL of the backend in that single file, and deploy `config.js` and `i18n.js` next to the HTML files. If the API cannot be reached, the calculation pages show the URL they tried in a red banner. The interface is available in Spanish and English (EN/ES button in the navigation bar).

## API

`GET /models` · `GET /regions` · `GET /task_types` · `GET /version` · `POST /calculate` · `POST /compare` · `POST /simulate` — see `docs/API.md`.

## Reproduce the case study

```bash
python -m scripts.case_study      # writes docs/case_study_v2.md
```

## Updating parameters

Edit the CSV files in `data/` (keep the `fuente` and date columns filled), then run `python -m backend.setup_database` and bump `TOOL_VERSION` in `backend/setup_database.py`.

## License and citation

GNU General Public License v3.0 or later (see `LICENSE`). Cite with `CITATION.cff`.
