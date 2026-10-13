# fastapi-config-service
Deploy a FastAPI service that merges four configuration layers — defaults, environment-specific YAML, .env file, and OS-level environment variables — then applies CLI overrides passed as query parameters. The grader sends fresh random overrides on every check.

Your assigned config layers
1. defaults (hardcoded)
port: 8000
workers: 1
debug: false
log_level: info
api_key: default-secret-000
2. config.development.yaml
port: 8141
workers: 6
debug: false
api_key: key-gsxi6bdx4r
3. .env file
NUM_WORKERS=3
APP_LOG_LEVEL=info
APP_API_KEY=key-jxccus7u2m
4. OS env vars (APP_* prefix)
APP_PORT=8852
APP_WORKERS=13
APP_LOG_LEVEL=debug
APP_API_KEY=key-2wtsv68q7q
Endpoint: GET /effective-config?set=key=value&set=…

Merge the four config layers from low to high precedence: defaults → config.<env>.yaml → .env → OS env (APP_* prefix).
Apply any ?set=key=value query parameters as the highest-precedence CLI overrides. Multiple set params are allowed.
Return JSON: {"port": 8000, "workers": 2, "debug": false, "log_level": "info", "api_key": "****"}
Type coercion rules:

port, workers → integer
debug → boolean (true/1/yes/on case-insensitive = true)
log_level and all other keys → string
Special cases:

Alias: NUM_WORKERS in the .env layer maps to the workers key.
Secret masking: api_key must always appear as "****" in the response — never expose the real value.
CORS: your service must allow cross-origin requests from this page so the browser can check it directly.
What the grader checks:

All five keys present with correct types (port as int, debug as bool, etc.).
Alias NUM_WORKERS → workers correctly resolved.
api_key masked as "****".
Fresh CLI overrides (e.g. ?set=port=9000&set=debug=true) applied correctly with highest precedence.
Deploy and paste your /effective-config endpoint URL below.
