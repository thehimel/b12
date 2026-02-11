#!/usr/bin/env python3
"""
Submit application via POST to the configured submission URL.
"""

import hashlib
import hmac
import json
import sys
from datetime import datetime, timezone

import httpx

from constants import (
    REQUEST_TIMEOUT,
    REQUIRED_ENV_VARS,
    SIGNING_SECRET,
    SUBMISSION_URL,
    EMAIL,
    NAME,
    RESUME_LINK,
    get_action_run_link,
    get_repository_link,
)


def get_iso8601_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def build_payload() -> dict:
    return {
        "action_run_link": get_action_run_link(),
        "email": EMAIL,
        "name": NAME,
        "repository_link": get_repository_link(),
        "resume_link": RESUME_LINK,
        "timestamp": get_iso8601_timestamp(),
    }


def main() -> None:
    for var, value in REQUIRED_ENV_VARS:
        if not value:
            print(f"Error: environment variable {var} is required.", file=sys.stderr)
            sys.exit(1)

    payload = build_payload()
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(
        SIGNING_SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Signature-256": f"sha256={signature}",
    }

    try:
        resp = httpx.post(
            SUBMISSION_URL,
            content=body,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and "receipt" in data:
            print(data["receipt"])
        else:
            print("Response missing success/receipt.", file=sys.stderr)
            sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} {e.response.reason_phrase}", file=sys.stderr)
        print(e.response.text, file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Request failed: {e!s}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
