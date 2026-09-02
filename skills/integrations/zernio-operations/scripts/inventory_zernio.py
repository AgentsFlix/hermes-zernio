#!/usr/bin/env python3
"""Read-only, sanitized Zernio inventory. Never prints the API key or webhook URLs."""
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get("ZERNIO_API_URL", "https://zernio.com/api/v1").rstrip("/")


def request(path):
    key = os.environ.get("ZERNIO_API_KEY")
    if not key:
        raise RuntimeError("ZERNIO_API_KEY is not set")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def list_value(data, key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        value = data.get(key, data.get("data", []))
        return value if isinstance(value, list) else []
    return []


def main():
    output = {"ok": False, "base_url": BASE_URL, "profiles": [], "accounts": [], "posts": [], "webhooks": []}
    endpoints = {
        "profiles": ("/profiles", "profiles"),
        "accounts": ("/accounts", "accounts"),
        "posts": ("/posts?limit=10", "posts"),
        "webhooks": ("/webhooks/settings", "webhooks"),
    }
    errors = {}
    for name, (path, key) in endpoints.items():
        try:
            raw = list_value(request(path), key)
            if name == "profiles":
                output[name] = [{"name": x.get("name"), "isDefault": x.get("isDefault", False)} for x in raw]
            elif name == "accounts":
                output[name] = [{"platform": x.get("platform"), "status": x.get("status"), "profileId": bool(x.get("profileId"))} for x in raw]
            elif name == "posts":
                output[name] = [{"status": x.get("status"), "platformCount": len(x.get("platforms", []))} for x in raw]
            else:
                output[name] = [{"name": x.get("name"), "isActive": x.get("isActive"), "eventCount": len(x.get("events", [])), "failureCount": x.get("failureCount")} for x in raw]
        except urllib.error.HTTPError as exc:
            errors[name] = {"http_status": exc.code}
        except Exception as exc:
            errors[name] = {"error": str(exc)}
    output["ok"] = bool(output["profiles"] or output["accounts"]) and not ("profiles" in errors and "accounts" in errors)
    if errors:
        output["errors"] = errors
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
