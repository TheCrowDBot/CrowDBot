from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


def load_images(folder_path: str) -> list[str]:
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return []

    return sorted(
        str(p)
        for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )
