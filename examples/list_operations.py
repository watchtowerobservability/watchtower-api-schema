"""Print every operation id-less route in openapi.json. Run: python examples/list_operations.py"""
import json
import pathlib

doc = json.loads((pathlib.Path(__file__).resolve().parent.parent / "openapi.json").read_text())
for path, item in sorted(doc["paths"].items()):
    for method in item:
        if method in {"get", "put", "post", "delete", "patch"}:
            print(method.upper(), path)
