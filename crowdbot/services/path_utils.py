from pathlib import Path
import re


def sanitize_filename(name: str) -> str:
    return re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        name,
    ).strip("_")


def get_output_folder(
    image_path: str | Path,
    output_dir: str | Path,
):
    image_name = sanitize_filename(Path(image_path).stem)

    print("IMAGE:", image_path)
    print("OUTPUT:", image_name)

    output_folder = Path(output_dir) / image_name

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return output_folder, image_name
