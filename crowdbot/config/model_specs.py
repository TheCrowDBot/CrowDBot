from typing import Any


MODEL_SPECS: dict[str, dict[str, Any]] = {
    "obb": {
        "title": "OBB Detection Model",
        "file_type": ["pt"],
        "folder": "obb",
        "url_label": "Download OBB model from URL",
    },
    "ocr": {
        "title": "OCR Model",
        "file_type": ["keras"],
        "folder": "ocr",
        "url_label": "Download OCR model from URL",
        "extra_files": [
            {
                "key": "vocab_path",
                "label": "Vocabulary file",
                "file_type": ["json"],
                "required": True,
            }
        ],
    },
}
