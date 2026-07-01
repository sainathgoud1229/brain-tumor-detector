"""
Image preprocessing utilities for Brain Tumor Detection.
"""

from pathlib import Path

import cv2
import numpy as np

IMAGE_SIZE = (224, 224)


def load_image(image_path: str | Path) -> np.ndarray:
    """
    Load an image from disk.

    Args:
        image_path: Path to image

    Returns:
        RGB image
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return image


def resize_image(image: np.ndarray) -> np.ndarray:
    """
    Resize image.
    """

    return cv2.resize(
        image,
        IMAGE_SIZE
    )


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize pixel values.
    """

    image = image.astype("float32")

    image = image / 255.0

    return image


def prepare_image(image_path: str | Path) -> np.ndarray:
    """
    Complete preprocessing pipeline.
    """

    image = load_image(image_path)

    image = resize_image(image)

    image = normalize_image(image)

    image = np.expand_dims(
        image,
        axis=0
    )

    return image