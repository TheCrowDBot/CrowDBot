import json
import numpy as np
from pathlib import Path


def to_json_serializable(obj):
    if isinstance(obj, dict):
        return {str(key): to_json_serializable(value) for key, value in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [to_json_serializable(value) for value in obj]

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, np.generic):
        return obj.item()

    return obj


def save_json(
    data: dict,
    path,
):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    serializable = to_json_serializable(data)

    json.dumps(serializable)

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            serializable,
            f,
            indent=4,
            ensure_ascii=False,
        )
