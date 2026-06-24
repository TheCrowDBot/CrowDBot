import json
from pathlib import Path

REGISTRY_PATH = Path("workspace/state/models_registry.json")


def load_registry():
    if not REGISTRY_PATH.exists():
        return {"obb": [], "ocr": []}

    return json.loads(REGISTRY_PATH.read_text())


def save_registry(data):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, indent=2))
