# PulseCast backend integration

Imported from the user-supplied `pulsecast_codebase.zip`, excluding Python caches. The existing FastAPI `/agent` endpoint is connected to the frontend assistant. Databricks credentials stay on the server.

## Local setup

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# Configure Databricks authentication and artifact paths in the environment.
uvicorn pulsecast.service.api:app --host 127.0.0.1 --port 8000
```

Run `npm run dev` from the repository root in another terminal. Vite proxies `/api/agent` to the Python service. The agent requires `risk.parquet`, `subject_summary.parquet`, and `feature_comparison.parquet` under `PULSECAST_ARTIFACT_ROOT`, along with access to the configured Databricks LLM endpoint. The uploaded package contains processing/training scripts to produce artifacts; no production credentials or trained artifacts are included.

## Hosted frontend

GitHub Pages serves static files and cannot run Python. Deploy the backend separately and set `VITE_API_URL` at frontend build time to its HTTPS URL. Configure CORS or serve the API through a trusted same-origin reverse proxy. No live backend is currently deployed; the public assistant reports that state rather than returning fabricated LLM responses.

For direct browser access, set `PULSECAST_ALLOWED_ORIGINS=https://davidvalenta-dev.github.io` on the backend. Keep Databricks tokens in server environment variables, never in `VITE_` variables.

## Audience scope

Doctor mode can browse the public research cohort. Patient demo mode is fixed to participant 004 and removes cohort selection/export. Agent tools force the requested participant ID, and patient requests omit cohort comparison. This is a public-data demo, not an access-control system: a client-supplied audience is not trusted authentication. Real deployment requires server-verified identity, an assigned-patient mapping, clinician permissions, and endpoint authorization before adding private records.

## Verification

Run `pytest` from this directory. Live Databricks queries need credentials and artifacts and cannot be verified offline.
