#!/usr/bin/env python3
"""Validate openapi.json (parses, is OpenAPI 3.x, every operation has a response) and, with
--notes, write CLIENT-NOTES.md. `--check` fails when CLIENT-NOTES.md is stale."""
import json, pathlib, sys
from collections import defaultdict

root = pathlib.Path(__file__).resolve().parent.parent
METHODS = {"get", "put", "post", "delete", "patch", "head", "options"}


def load():
    doc = json.loads((root / "openapi.json").read_text())
    assert str(doc.get("openapi", "")).startswith("3."), "not an OpenAPI 3 document"
    assert doc.get("paths"), "no paths"
    for path, item in doc["paths"].items():
        for m, op in item.items():
            if m in METHODS:
                assert op.get("responses"), f"{m.upper()} {path} has no responses"
    return doc


def notes(doc):
    groups = defaultdict(list)
    for path, item in sorted(doc["paths"].items()):
        seg = path.split("/")
        group = seg[2] if len(seg) > 2 and seg[1] == "v1" else "meta"
        for m in sorted(item):
            if m in METHODS:
                groups[group].append(f"{m.upper()} `{path}`")
    out = [f"# {doc['info']['title']}: client usage notes", "",
           "Generated from `openapi.json` by `scripts/check.py --notes`; do not edit.", "",
           "## Conventions", "",
           "- Public API lives under `/v1`; send `Authorization: Bearer <token>`.",
           "- Lists use cursor pagination: `?limit=&cursor=` returns `{data, next_cursor}`; stop when `next_cursor` is null.",
           "- Errors are RFC 9457 `application/problem+json`. Inaccessible resources return 404, not 403.",
           "- Secrets are shown once at creation; store them immediately.",
           "- Generate a client with any OpenAPI 3.1 generator, e.g. `openapi-generator-cli generate -i openapi.json -g <lang>`.",
           "", "## Operations by resource", ""]
    for g in sorted(groups):
        out += [f"### {g} ({len(groups[g])})", ""] + [f"- {x}" for x in groups[g]] + [""]
    return "\n".join(out)


if __name__ == "__main__":
    text = notes(load())
    target = root / "CLIENT-NOTES.md"
    if "--notes" in sys.argv:
        target.write_text(text)
    elif "--check" in sys.argv and (not target.exists() or target.read_text() != text):
        sys.exit("CLIENT-NOTES.md is stale: run python scripts/check.py --notes")
