import os
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import yaml

BASE = Path(__file__).resolve().parent
DEFAULTS = {"port": 8000, "workers": 1, "debug": False, "log_level": "info", "api_key": "default-secret-000"}
KEYS = {"port", "workers", "debug", "log_level", "api_key"}
ALIASES = {"NUM_WORKERS": "workers"}

def normalize_key(key):
    if key in ALIASES:
        return ALIASES[key]
    if key.startswith("APP_"):
        key = key[4:]
    return key.lower()

def cast(key, value):
    if key in {"port", "workers"}:
        return int(value)
    if key == "debug":
        return str(value).strip().lower() in {"true", "1", "yes", "on"}
    return str(value)

def apply_layer(config, layer):
    for raw_key, value in layer.items():
        key = normalize_key(str(raw_key))
        if key in KEYS and value is not None:
            config[key] = cast(key, value)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    config = DEFAULTS.copy()
    environment = os.environ.get("APP_ENV", "development")
    yaml_path = BASE / f"config.{environment}.yaml"
    if yaml_path.is_file():
        with yaml_path.open(encoding="utf-8") as f:
            apply_layer(config, yaml.safe_load(f) or {})
    apply_layer(config, dotenv_values(BASE / ".env"))
    apply_layer(config, {k: v for k, v in os.environ.items() if k.startswith("APP_") and k != "APP_ENV"})
    for item in set:
        if "=" in item:
            key, value = item.split("=", 1)
            apply_layer(config, {key: value})
    config["api_key"] = "****"
    return config
