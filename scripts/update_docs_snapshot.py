#!/usr/bin/env python3
"""Download Zernio's documentation snapshot for review. It never changes operational files."""
import hashlib
import json
import pathlib
import urllib.request

URL = "https://docs.zernio.com/llms-full.txt"
OUT = pathlib.Path("docs/zernio-llms-full.txt")
META = pathlib.Path("docs/zernio-llms-full.metadata.json")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "hermes-zernio-docs-review/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        body = response.read()
        metadata = {"url": URL, "http_status": response.status, "content_type": response.headers.get("content-type")}
    OUT.write_bytes(body)
    metadata.update({"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
    META.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
