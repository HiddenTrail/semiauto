# disable misleading E1101: Module 'cv2' has no '***' member (no-member)
# disable C0103: Module name "ImageSimilarityLibrary" doesn't conform to snake_case naming style (invalid-name)
# pylint: disable=E1101,C0103

import urllib.request
from robot.api.deco import keyword, not_keyword
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import imagehash

class ImageSimilarityLibrary:
    @keyword("Assert Images Are Similar")
    def assert_images_are_similar(self, expected_image_path, actual_image_url):
        diff1, diff2, diff3, diff4 = self._compare_images(expected_image_path, actual_image_url)
        if diff1 < 1 or diff2 < 1 or diff3 < 1 or diff4 < 1:
            raise AssertionError(f"Images are not similar: {expected_image_path} vs {actual_image_url}")

    @keyword("Assert Images Are Not Similar")
    def assert_images_are_not_similar(self, expected_image_path, actual_image_url):
        diff1, diff2, diff3, diff4 = self._compare_images(expected_image_path, actual_image_url)
        if diff1 == 1 or diff2 == 1 or diff3 == 1 or diff4 == 1:
            raise AssertionError(f"Images are similar: {expected_image_path} vs {actual_image_url}")

    @not_keyword
    def _compare_images(self, expected_image_path, actual_image_url):
        expected_image = _read_image(expected_image_path)
        actual_image = _read_image_from_url(actual_image_url)
        actual_image = _resize_image(actual_image, _image_size(expected_image))
        # write_image_to_file(actual_image, "actual_image.jpg")  # just debug

        diff1 = _compare_images_opencv(actual_image, expected_image)
        diff2 = _compare_images_pillow(actual_image, expected_image)
        diff3 = _compare_images_scikit(actual_image, expected_image)
        diff4 = _compare_images_imagehash(actual_image, expected_image)

        print("similarity opencv:   ", diff1)
        print("similarity pillow:   ", diff2)
        print("similarity scikit:   ", diff3)
        print("similarity imagehash:", diff4)

        return diff1, diff2, diff3, diff4

def _read_image(file_path):
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {file_path}")

    return image

def _read_image_from_url(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image from URL")

    return image

def _write_image_to_file(cv2_image, file_path):
    success = cv2.imwrite(file_path, cv2_image)
    if not success:
        raise IOError("Failed to write image to file at " + file_path)

def _image_size(image):
    height, width = image.shape[:2]

    return (width, height)

def _resize_image(image, size, keep_aspect_ratio=False):
    if keep_aspect_ratio:
        (height, width) = _image_size(image)
        (new_width, new_height) = size
        ratio_w = new_width / width
        ratio_h = new_height / height
        ratio = min(ratio_w, ratio_h)
        new_size = (int(width * ratio), int(height * ratio))
    else:
        new_size = size
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

    return resized_image

def _compare_images_opencv(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gray1 - gray2) ** 2)
    if mse == 0:
        return 1.0
    else:
        return 1 / (1 + mse)

def _compare_images_pillow(image1, image2):
    np_img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    np_img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    difference = np.abs(np_img1 - np_img2)
    score = 1.0 - np.mean(difference) / 255.0

    return score

def _compare_images_scikit(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)

    return score

def _compare_images_imagehash(image1, image2):
    pil_image1 = Image.fromarray(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    pil_image2 = Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    hash1 = imagehash.average_hash(pil_image1)
    hash2 = imagehash.average_hash(pil_image2)
    difference = hash1 - hash2
    max_difference = max(len(hash1.hash)**2, len(hash2.hash)**2)
    similarity = 1 - difference / max_difference

    return similarity
