import crowmatcher
from dataclasses import asdict
from PIL import Image
import numpy as np

from crowdbot.services.json_utils import save_json
from crowdbot.services.path_utils import get_output_folder


class MatcherPipeline:
    name = "matcher"

    def _save_result(
        self,
        image_path,
        output_dir,
        result,
    ):
        output_folder, image_name = get_output_folder(
            image_path,
            output_dir,
        )

        output_file = output_folder / f"{image_name}_matcher.json"

        save_json(
            result,
            output_file,
        )

        return output_file

    def run(
        self,
        obb,
        image_path,
        output_dir=None,
        outputs=None,
        **kwargs,
    ):
        image_array = np.array(Image.open(obb["image"]))

        result = crowmatcher.process(
            image=image_array,
            detections=obb["detections"],
        )
        result_dict = asdict(result)

        if output_dir and outputs and outputs.get("matcher", False):
            self._save_result(image_path, output_dir, result_dict)

        return result_dict
