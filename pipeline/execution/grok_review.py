"""Optional xAI review client. Refuses to run unless XAI_API_KEY is set.

The value is never printed, logged, or written. This module does not invent a review.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SECRET_NAME = "XAI_API_KEY"
ROUTE = "https://api.x.ai/v1/chat/completions"
ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "docs" / "automation" / "grok_reviews"


def secret_present() -> bool:
    value = os.environ.get(SECRET_NAME)
    return isinstance(value, str) and bool(value.strip())


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "grok_invoked": False,
        "secret_name": SECRET_NAME,
        "secret_present": secret_present(),
        "secret_value_read": False,
        "route": ROUTE,
        "model_id": None,
        "request_id": None,
        "http_status": None,
        "timestamp_utc": stamp,
        "sanitized_request": None,
        "sanitized_response": None,
    }
    if not record["secret_present"]:
        record["reason"] = f"{SECRET_NAME} is not set. No request was sent."
        _write(record, stamp)
        print(f"grok_review: NOT_RUN {SECRET_NAME} unset")
        return 2
    if "--send" not in argv:
        record["reason"] = "Secret is set, but --send was not passed. No request was sent."
        _write(record, stamp)
        print("grok_review: NOT_RUN --send not passed")
        return 2
    prompt_path = Path(argv[argv.index("--prompt") + 1]) if "--prompt" in argv else None
    if prompt_path is None or not prompt_path.is_file():
        print("grok_review: NOT_RUN missing --prompt file")
        return 2
    model = "grok-4"
    if "--model" in argv:
        model = argv[argv.index("--model") + 1]
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt_path.read_text()[:120000]}],
    }
    token = os.environ[SECRET_NAME].strip()
    request = urllib.request.Request(
        ROUTE, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    record["secret_value_read"] = True
    record["model_id"] = model
    record["sanitized_request"] = {"model": model, "route": ROUTE, "prompt_path": str(prompt_path), "prompt_chars": len(body["messages"][0]["content"])}
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = response.read().decode()
            record["http_status"] = getattr(response, "status", None)
            record["request_id"] = response.headers.get("x-request-id")
    except Exception as exc:  # noqa: BLE001 — record the failure class, never the token
        record["reason"] = f"request failed: {type(exc).__name__}"
        _write(record, stamp)
        print(f"grok_review: FAILED {type(exc).__name__}")
        return 1
    payload = json.loads(raw)
    text = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
    record["grok_invoked"] = bool(text.strip())
    record["sanitized_response"] = {"chars": len(text), "text": text}
    record["reason"] = "response received" if record["grok_invoked"] else "empty response"
    _write(record, stamp)
    print(f"grok_review: {'OK' if record['grok_invoked'] else 'EMPTY'} model={model}")
    return 0 if record["grok_invoked"] else 1


def _write(record: dict, stamp: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe = stamp.replace(":", "")
    (OUT_DIR / f"{safe}_attempt.json").write_text(json.dumps(record, indent=1) + "\n")


if __name__ == "__main__":
    sys.exit(main())
