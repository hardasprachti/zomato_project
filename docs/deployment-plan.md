# Deployment Plan
## AI-Powered Restaurant Recommendation System — Railway Deployment

---

## Table of Contents

1. [Overview & Architecture Decision](#1-overview--architecture-decision)
2. [Current State Audit](#2-current-state-audit)
3. [Phase D0 — Repository & Secrets Prep](#phase-d0--repository--secrets-prep)
4. [Phase D1 — Production Config Files](#phase-d1--production-config-files)
5. [Phase D2 — Railway Project Setup & Deploy](#phase-d2--railway-project-setup--deploy)
6. [Phase D3 — Environment Variables on Railway](#phase-d3--environment-variables-on-railway)
7. [Phase D4 — Post-Deploy Verification](#phase-d4--post-deploy-verification)
8. [Phase D5 — Domain, Monitoring & Ongoing Ops](#phase-d5--domain-monitoring--ongoing-ops)
9. [Why Not Vercel (and the future path if that changes)](#9-why-not-vercel-and-the-future-path-if-that-changes)
10. [Rollback & Redeploy](#10-rollback--redeploy)
11. [Deployment Checklist Summary](#11-deployment-checklist-summary)

---

## 1. Overview & Architecture Decision

This project is currently a **single Streamlit application** ([app/streamlit_app.py](../app/streamlit_app.py)) — the UI and the recommendation logic (`src/filter.py`, `src/prompt_builder.py`, `src/llm_client.py`) run in one Python process. There is no separate REST API and no standalone JS/React frontend.

**Decision: deploy the entire app to Railway as one service. Vercel is not used in this plan.**

Why: Streamlit needs a persistent, stateful server process (it holds a WebSocket connection per session for live interactivity). Vercel's hosting model is built for static sites and short-lived serverless functions — it cannot run a long-lived Streamlit server. Railway runs arbitrary containers/processes continuously, which is exactly what Streamlit needs. Splitting this into a separate frontend (Vercel) and backend (Railway) would require rebuilding the UI as a standalone web frontend calling a new REST API — that's a feature-build project, not a deployment task, and is explicitly out of scope here (see [§9](#9-why-not-vercel-and-the-future-path-if-that-changes) for that path if you want it later).

**End state:** one Railway service, serving the Streamlit app publicly over HTTPS on a Railway-provided (or custom) domain, with API keys stored as Railway environment variables.

---

## 2. Current State Audit

Checked directly against the repo as it stands today:

| Item | Status | Action needed |
|---|---|---|
| Git repository | **Not initialized** (`git status` → "not a git repository") | Init repo, first commit, push to GitHub |
| `.gitignore` | **Missing** | Create one before the first commit |
| `.env` | Contains a **real, active Groq API key** in plaintext | Must never be committed; rotate the key before/after going live (see D0) |
| `data/restaurants.csv` | Present, 4.0 MB, ~51k rows | Small enough to commit directly — no need to regenerate from Hugging Face at deploy time |
| `requirements.txt` | Includes `datasets` (pulls `pyarrow`, `huggingface-hub`, etc.) and `pytest` | Neither is needed at runtime — only for `src/ingest.py` and the test suite. Splitting these out shortens Railway build time |
| Streamlit entry point | `app/streamlit_app.py`, reads `data/restaurants.csv` via a relative path, imports `src.*` via `sys.path` injection | Works as-is as long as the process's working directory is the repo root (Railway's default) |
| Port handling | App has no `$PORT` awareness (relies on Streamlit's default `8501`) | Must pass `--server.port=$PORT --server.address=0.0.0.0` at start, since Railway assigns the port dynamically |

---

## Phase D0 — Repository & Secrets Prep

**Goal:** Get the project into a pushable, secret-free Git repository.

### Steps

#### D0.1 — Rotate the exposed Groq key
The current `GROQ_API_KEY` in `.env` has been used in plaintext during development. Before this repo goes anywhere near GitHub, generate a **new** key in the Groq console and use that going forward. Treat the old one as burned.

#### D0.2 — Create `.gitignore`
```gitignore
.env
.env.local
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
venv/
.venv/
```
Note: unlike the original [implementation-plan.md](implementation-plan.md) §7.3 suggestion, **do not** ignore `data/`. We're committing `restaurants.csv` directly (see D0.4).

#### D0.3 — Initialize git and push to GitHub
```bash
git init
git add .
git status   # verify .env is NOT listed
git commit -m "Initial commit"
gh repo create <repo-name> --private --source=. --push
```
Railway deploys from a GitHub repo (or via `railway up` from local — see D2), so this needs to exist first if you want auto-deploy-on-push.

#### D0.4 — Confirm `data/restaurants.csv` is tracked
```bash
git ls-files data/restaurants.csv
```
At 4 MB this is well within GitHub/Railway limits and avoids depending on Hugging Face being reachable at build time.

### ✅ Phase D0 Checklist
- [ ] Groq API key rotated
- [ ] `.gitignore` created and committed
- [ ] `.env` confirmed absent from `git status` / `git log`
- [ ] Repo pushed to GitHub
- [ ] `data/restaurants.csv` tracked in git

---

## Phase D1 — Production Config Files

**Goal:** Add the handful of files Railway needs to build and start the app correctly.

### Steps

#### D1.1 — Split `requirements.txt`
Runtime-only `requirements.txt` (what Railway installs):
```txt
pandas>=2.0.0
google-generativeai>=0.7.0
openai>=1.30.0
anthropic>=0.28.0
groq>=0.5.0
python-dotenv>=1.0.0
streamlit>=1.35.0
```
New `requirements-dev.txt` (local only — ingestion + tests):
```txt
-r requirements.txt
datasets>=2.19.0
pytest>=8.0.0
```
This keeps the Railway build from pulling in `pyarrow`/`huggingface-hub`/etc., which it never uses at runtime since `restaurants.csv` is already committed.

#### D1.2 — Pin the Python version
Create `.python-version` at the repo root:
```
3.11
```
Nixpacks (Railway's default builder) reads this to select the interpreter. Without it, a future Nixpacks default bump could break compatibility silently.

#### D1.3 — Add `.streamlit/config.toml`
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```
`enableCORS`/`enableXsrfProtection` set to `false` avoids a common gotcha where Streamlit's own CORS/XSRF checks conflict with Railway's reverse proxy and silently break the WebSocket connection (symptom: page loads but never updates after interaction). Port is deliberately **not** set here — it's injected dynamically at start (D1.4).

#### D1.4 — Add `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/_stcore/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```
`/_stcore/health` is Streamlit's built-in health endpoint — it returns `ok` with no app logic involved, so Railway can tell "process up" apart from "app actually works."

### ✅ Phase D1 Checklist
- [ ] `requirements.txt` trimmed to runtime deps; `requirements-dev.txt` added
- [ ] `.python-version` added
- [ ] `.streamlit/config.toml` added
- [ ] `railway.json` added
- [ ] Local smoke test: `pip install -r requirements.txt && streamlit run app/streamlit_app.py` still works with the trimmed deps

---

## Phase D2 — Railway Project Setup & Deploy

**Goal:** Stand up the Railway service and get a first successful deploy.

### Steps

#### D2.1 — Create the Railway project
Via dashboard (railway.app → New Project → Deploy from GitHub repo → select this repo), **or** via CLI:
```bash
npm install -g @railway/cli
railway login
railway init
railway link      # if the project already exists
```

#### D2.2 — First deploy
GitHub-connected projects auto-deploy on push to the tracked branch. For a manual/CLI deploy instead:
```bash
railway up
```

#### D2.3 — Watch the build
```bash
railway logs
```
Confirm: Nixpacks detects Python via `.python-version`, installs `requirements.txt`, then runs the `startCommand` from `railway.json` with no import errors.

### ✅ Phase D2 Checklist
- [ ] Railway project created and linked to the GitHub repo
- [ ] First deploy triggered
- [ ] Build logs show a clean `pip install` (no `datasets`/`pyarrow` build errors)
- [ ] Process starts and stays up (not crash-looping)

---

## Phase D3 — Environment Variables on Railway

**Goal:** Move every secret out of `.env` and into Railway's env var store.

### Steps

#### D3.1 — Set variables
In Railway dashboard → project → Variables (or via CLI: `railway variables set KEY=value`):
```
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=<the rotated key from D0.1>
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
TOP_N_RESULTS=10
```
Only set the API key for whichever `LLM_PROVIDER` you're actually using — no need to fill in the others (matches the existing `.env.example` convention).

#### D3.2 — Confirm `python-dotenv` doesn't shadow these
`src/llm_client.py` calls `load_dotenv()` on import. In production there's no `.env` file (it's gitignored), so `load_dotenv()` is a harmless no-op and `os.getenv()` reads straight from Railway's injected environment. No code change needed — just confirming no `.env` gets accidentally bundled (D0.2 already prevents this).

### ✅ Phase D3 Checklist
- [ ] All required env vars set in Railway (not committed anywhere)
- [ ] Redeployed after setting variables (Railway restarts automatically on var change)
- [ ] No `.env` file present in the deployed container

---

## Phase D4 — Post-Deploy Verification

**Goal:** Confirm the live Railway URL behaves the same as the locally-verified Phase 5 build.

Mirror the checks already validated locally in [implementation-plan.md](implementation-plan.md) Phase 5, against the live URL instead of `localhost`:

- [ ] `https://<your-app>.up.railway.app` loads without a Railway "Application failed to respond" error
- [ ] `/_stcore/health` returns `ok`
- [ ] Sidebar filters (location, cuisine, budget, rating, extras) all render and respond
- [ ] Submitting a query with a known-good input (e.g. location `jp nagar`, cuisine `north indian`) returns results and a real LLM response
- [ ] Loading state appears and disappears cleanly (this was a real bug fixed in Phase 5 — worth re-confirming in production)
- [ ] An impossible filter combo shows the "No matches found" state, not a crash
- [ ] Check `railway logs` for any stack traces during the above

---

## Phase D5 — Domain, Monitoring & Ongoing Ops

### Steps

#### D5.1 — Custom domain (optional)
Railway → project → Settings → Domains → add a custom domain, or keep the free `*.up.railway.app` subdomain.

#### D5.2 — Cost awareness
Two variable costs to watch:
- **Railway usage-based billing** — scales with uptime/compute; a single always-on Streamlit service is typically low-cost but not free indefinitely.
- **LLM API calls** — every search submission calls the Groq (or configured provider) API. There's currently no rate limiting or per-user quota in the app, so a spike in public traffic directly spikes LLM spend. Not a blocker for this deployment, but worth flagging if this URL gets shared publicly.

#### D5.3 — Logs & restarts
`railway logs --follow` for live tailing. The `restartPolicyType: ON_FAILURE` in `railway.json` (D1.4) auto-restarts on crash, capped at 3 retries, so a bad deploy fails loud rather than silently looping forever.

### ✅ Phase D5 Checklist
- [ ] Domain decision made (default subdomain or custom)
- [ ] Team aware of the uncapped LLM-cost-per-request risk
- [ ] Confirmed restart policy behaves as expected (e.g. by checking logs after a deliberate bad deploy, if desired)

---

## 9. Why Not Vercel (and the future path if that changes)

Vercel isn't part of this deployment because there's currently nothing in this repo shaped like a Vercel deployment — no Next.js/React/static frontend, no serverless API routes. The `Google_sticth_design/` folder contains a static Tailwind-CDN HTML mockup used as the *visual reference* for the Streamlit app's current theme (compare its Material-color CSS tokens to `DESIGN_CSS` in [streamlit_app.py](../app/streamlit_app.py)) — it has no real data wiring (hardcoded placeholder values, no fetch calls) and isn't a deployable product surface on its own.

If you later want an actual split — a polished static/React frontend on Vercel talking to a real backend on Railway — that's a build, not a deploy step, and would mean:
1. Wrapping `src/filter.py`, `src/prompt_builder.py`, `src/llm_client.py` in a FastAPI (or similar) app exposing JSON endpoints, deployed to Railway.
2. Building an actual frontend (e.g. from the Stitch mockup, wired to real state and fetch calls) deployed to Vercel, calling that API.

Flag this separately when you're ready — it's a meaningfully different scope than this plan.

---

## 10. Rollback & Redeploy

- Railway keeps deployment history per service — dashboard → Deployments → pick a previous successful build → **Redeploy**. This is the fastest rollback path and doesn't require a git revert.
- For a git-driven rollback: `git revert <bad-commit>` and push — the GitHub-connected service redeploys automatically.
- Because `railway.json` sets `restartPolicyType: ON_FAILURE` with a retry cap, a broken deploy fails visibly in the dashboard rather than serving a half-broken app indefinitely.

---

## 11. Deployment Checklist Summary

| Phase | Goal | Blocking risk if skipped |
|---|---|---|
| **D0** | Clean, secret-free git repo | Committing a live API key to a public/shared repo |
| **D1** | Config files Railway needs | Build fails, or app can't bind to Railway's dynamic port |
| **D2** | First deploy | N/A — this is the deploy itself |
| **D3** | Secrets in Railway, not in git | App runs but every LLM call fails with an auth error |
| **D4** | Verify live behavior | Silent regressions vs. the locally-tested Phase 5 build |
| **D5** | Domain + ongoing ops awareness | Unbounded LLM spend if traffic spikes unexpectedly |

---

**Total estimated time:** ~2–3 hours for a first deploy (most of it in D0/D1 one-time setup); subsequent deploys are a `git push` and a few minutes of Railway build time.
