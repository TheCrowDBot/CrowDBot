from pathlib import Path
import requests
import hashlib
from urllib.parse import urlparse


def _get_filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name

    if not name:
        name = "model.pt"

    return name


def _compute_hash(file_bytes: bytes) -> str:
    return hashlib.md5(file_bytes).hexdigest()


def download_model(url: str, target_dir: Path):
    """
    Downloads a model from a URL and stores it locally.

    Returns:
        (file_path, file_hash, filename)
    """

    target_dir.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    file_bytes = response.content

    filename = _get_filename_from_url(url)
    file_path = target_dir / filename

    # Avoid overwriting unless same content
    if file_path.exists():
        existing_hash = _compute_hash(file_path.read_bytes())
        new_hash = _compute_hash(file_bytes)

        if existing_hash == new_hash:
            return file_path, existing_hash, filename

    file_path.write_bytes(file_bytes)

    file_hash = _compute_hash(file_bytes)

    return file_path, file_hash, filename
