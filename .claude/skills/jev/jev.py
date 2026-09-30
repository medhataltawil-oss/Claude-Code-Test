#!/usr/bin/env python3
"""Call Jev (typesafe/jev-1.13) through OpenRouter's Decisions endpoint.

The API key is read only from the OPENROUTER_API_KEY environment variable.
It is never printed, logged, or written to disk.

Usage:
  jev.py request.json
  jev.py -            # read the request from stdin

request.json is either a single request:
  {"state": "<text or JSON>", "questions": {...}}
or a batch (one API call per item, run in parallel, same questions for all):
  {"questions": {...}, "items": [{"id": "a", "state": "..."}, ...]}

Prints JSON: {"results": [{"id", "ok", "answers"|"error", "latency_ms", "cost", ...}],
              "total_cost", "total_wall_ms"}
"""
import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = "typesafe/jev-1.13"
RETRY_STATUS = {429, 502, 503, 524, 529}


def call(key, state, questions, attempts=3):
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    last = None
    for i in range(attempts):
        req = urllib.request.Request(
            URL,
            data=body,
            method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            ms = round((time.perf_counter() - t0) * 1000)
            return {
                "ok": True,
                "answers": data.get("answers"),
                "latency_ms": ms,
                "cost": (data.get("usage") or {}).get("cost"),
                "usage": data.get("usage"),
                "model": data.get("model"),
                "id": data.get("id"),
            }
        except urllib.error.HTTPError as e:
            ms = round((time.perf_counter() - t0) * 1000)
            raw = e.read().decode("utf-8", "replace")
            last = {"ok": False, "status": e.code, "error": raw, "latency_ms": ms}
            if e.code not in RETRY_STATUS:
                return last
        except Exception as e:  # network, timeout, bad JSON
            ms = round((time.perf_counter() - t0) * 1000)
            last = {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}", "latency_ms": ms}
        time.sleep(2 ** (i + 1))
    return last


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set in the environment.")
    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    req = json.loads(src)
    questions = req["questions"]
    items = req.get("items") or [{"id": "0", "state": req["state"]}]

    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(call, key, it["state"], questions) for it in items]
        results = []
        for it, f in zip(items, futs):
            res = f.result()
            res["id"] = it.get("id", res.get("id"))
            results.append(res)
    out = {
        "results": results,
        "total_cost": sum(r.get("cost") or 0 for r in results),
        "total_wall_ms": round((time.perf_counter() - t0) * 1000),
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all(r["ok"] for r in results) else 1)


if __name__ == "__main__":
    main()
