"""
Image generation module using OpenAI's gpt-image-1.5 API.
Generates images and saves them locally for use as OBS sources.
"""

import base64
import os
from datetime import datetime

from openai import OpenAI


class ImageGenerator:
    VALID_SIZES = {"1024x1024", "1536x1024", "1024x1536", "1920x1080"}
    VALID_QUALITIES = {"low", "medium", "high", "auto"}
    VALID_BACKGROUNDS = {"transparent", "opaque", "auto"}

    def __init__(self, api_key: str, output_dir: str = None):
        self._client = OpenAI(api_key=api_key)
        self._output_dir = output_dir or os.path.join(os.path.dirname(__file__), "generated_images")
        os.makedirs(self._output_dir, exist_ok=True)

    def generate(self, prompt: str, size: str = "1920x1080",
                 quality: str = "high", background: str = "opaque") -> dict:
        if size not in self.VALID_SIZES:
            raise ValueError(f"Invalid size '{size}'. Must be one of: {', '.join(sorted(self.VALID_SIZES))}")
        if quality not in self.VALID_QUALITIES:
            raise ValueError(f"Invalid quality '{quality}'. Must be one of: {', '.join(sorted(self.VALID_QUALITIES))}")
        if background not in self.VALID_BACKGROUNDS:
            raise ValueError(f"Invalid background '{background}'. Must be one of: {', '.join(sorted(self.VALID_BACKGROUNDS))}")

        result = self._client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size=size,
            quality=quality,
            background=background,
            output_format="png",
            n=1,
        )

        image_b64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_b64)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"obs_image_{timestamp}.png"
        filepath = os.path.join(self._output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        abs_path = os.path.abspath(filepath)

        return {
            "path": abs_path,
            "size": size,
            "prompt": prompt,
        }
