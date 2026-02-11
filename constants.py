"""Application constants and environment configuration."""

from decouple import config

# Required from environment (no defaults; set in .env or CI secrets)
SIGNING_SECRET = config("SIGNING_SECRET")
SUBMISSION_URL = config("SUBMISSION_URL")
REQUEST_TIMEOUT = 30.0

# Environment variables
NAME = config("NAME", default="")
EMAIL = config("EMAIL", default="")
RESUME_LINK = config("RESUME_LINK", default="")
REPOSITORY_LINK = config("REPOSITORY_LINK", default="")
ACTION_RUN_LINK = config("ACTION_RUN_LINK", default="")
GITHUB_SERVER_URL = config("GITHUB_SERVER_URL", default="")
GITHUB_REPOSITORY = config("GITHUB_REPOSITORY", default="")
GITHUB_RUN_ID = config("GITHUB_RUN_ID", default="")

# Required env var names and values (for validation)
REQUIRED_ENV_VARS = (
    ("NAME", NAME),
    ("EMAIL", EMAIL),
    ("RESUME_LINK", RESUME_LINK),
)


def get_repository_link() -> str:
    if REPOSITORY_LINK:
        return REPOSITORY_LINK
    if GITHUB_SERVER_URL and GITHUB_REPOSITORY:
        return f"{GITHUB_SERVER_URL.rstrip('/')}/{GITHUB_REPOSITORY}"
    raise SystemExit(
        "Set REPOSITORY_LINK or run in GitHub Actions (GITHUB_SERVER_URL, GITHUB_REPOSITORY)."
    )


def get_action_run_link() -> str:
    if ACTION_RUN_LINK:
        return ACTION_RUN_LINK
    if GITHUB_SERVER_URL and GITHUB_REPOSITORY and GITHUB_RUN_ID:
        return f"{GITHUB_SERVER_URL.rstrip('/')}/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"
    raise SystemExit(
        "Set ACTION_RUN_LINK or run in GitHub Actions (GITHUB_RUN_ID, etc.)."
    )
