from pathlib import Path
import hashlib

BASE_MODELS_DIR = Path("workspace/models")


def save_model(uploaded_file, subfolder: str):

    target_dir = BASE_MODELS_DIR / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / uploaded_file.name

    file_bytes = uploaded_file.getbuffer()

    file_path.write_bytes(file_bytes)

    return file_path, hashlib.md5(file_bytes).hexdigest()
