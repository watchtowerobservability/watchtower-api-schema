# watchtower-api-schema

The Watchtower control-plane OpenAPI 3.1 document (`openapi.json`, copied from the monorepo's
`apps/web/openapi.json`) plus generated client usage notes ([`CLIENT-NOTES.md`](CLIENT-NOTES.md)).

Status: 0.x, early. The schema is generated from server code and may change between minor versions.

## Install

Schema repository, not a package. Download `openapi.json` from the latest release.

## Quick start

```sh
curl -LO https://github.com/watchtowerobservability/watchtower-api-schema/releases/latest/download/openapi.json
npx @openapitools/openapi-generator-cli generate -i openapi.json -g python -o client
```

```python
import json
print(len(json.load(open("openapi.json"))["paths"]), "paths")
```

## Contents

| File | What |
|---|---|
| `openapi.json` | The API description |
| `CLIENT-NOTES.md` | Auth, pagination, errors and the operation list per resource (generated) |
| `scripts/check.py` | Validates the schema; `--notes` regenerates the notes |

## Configuration

| Name | Meaning |
|---|---|
| `Authorization: Bearer <token>` | Every `/v1` call; keys are never logged or put in URLs |

## Provenance

Every release artifact carries a GitHub build attestation. Verify one with
`gh attestation verify <file> --repo watchtowerobservability/watchtower-api-schema`.

## License

Apache-2.0. Source of truth is the Watchtower monorepo; this repository is a published mirror.
