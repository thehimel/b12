# Application Submission

A Python project that submits an application by POSTing a signed JSON payload to a configurable endpoint. It is
intended to run from **GitHub Actions** (manual trigger); it can also be run locally with the right environment
variables.

A test server is deployed on **Vercel** for trying the client with a live endpoint.

| Link       | URL                                                                                      |
|------------|------------------------------------------------------------------------------------------|
| Repository | [github.com/thehimel/b12-server](https://github.com/thehimel/b12-server)                 |
| Live       | [b12-server.vercel.app](https://b12-server.vercel.app/)                                  |
| OpenAPI    | [b12-server.vercel.app/docs](https://b12-server.vercel.app/docs)                         |
| API        | [b12-server.vercel.app/apply/submission](https://b12-server.vercel.app/apply/submission) |

## Prerequisites

- Python 3.12+
- Signing secret and submission URL (from application provider; do not commit).

## Environment variables

| Variable          | Required | Description                                                                  |
|-------------------|----------|------------------------------------------------------------------------------|
| `SIGNING_SECRET`  | Yes      | HMAC-SHA256 secret (do not commit).                                          |
| `SUBMISSION_URL`  | Yes      | Submission endpoint URL.                                                     |
| `NAME`            | Yes      | Full name.                                                                   |
| `EMAIL`           | Yes      | Email address.                                                               |
| `RESUME_LINK`     | Yes      | URL to resume (PDF, HTML, or LinkedIn).                                      |
| `REPOSITORY_LINK` | No       | Repo URL; derived from `GITHUB_SERVER_URL` + `GITHUB_REPOSITORY` in Actions. |
| `ACTION_RUN_LINK` | No       | CI run URL; derived from `GITHUB_*` in Actions.                              |

For local runs, set `REPOSITORY_LINK` and `ACTION_RUN_LINK` in `.env` (or set `GITHUB_*`) so the payload is complete.

## Getting started

```bash
git clone <repo-url>
cd b12
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env
# Edit .env with the required variables (see Environment variables)
python submit_application.py
```

## GitHub Actions

1. **Secrets:** Settings → Secrets and variables → Actions → **New repository secret**. Add the five required
   variables (see Environment variables). Secrets cannot be viewed or edited after creation.
2. **Run:** Actions → **Submit application** → **Run workflow** → **Run workflow**.
3. Copy the **receipt** from the job log to confirm the submission.

`REPOSITORY_LINK` and `ACTION_RUN_LINK` are not needed in secrets; the workflow uses GitHub’s `GITHUB_*` variables.
