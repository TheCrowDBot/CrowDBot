from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


def load_images(folder_path: str) -> list[str]:
    target = Path(folder_path)

    if not target.exists():
        return []

    # Handle single images
    if target.is_file():
        if target.suffix.lower() in IMAGE_EXTENSIONS:
            return [str(target)]
        return []

    # Handle dir with multiple images
    if target.is_dir():
        return sorted(
            str(p)
            for p in target.rglob("*")
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        )

    return []
