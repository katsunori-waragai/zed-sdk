"""
library for simple use of FaceMe SDK
FaceMe SDK is developed by Cyberlink.

Documentation for  FaceMe will be placed in ~/FaceMeSDK/Documents.

"""
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np

import FaceMe.FaceMePython3SDK as FaceMe
from FaceMe.FaceMeSDK import FaceMeSDK, FR_FAILED, FR_SUCC


REPO_ROOT = Path(__file__).resolve().parent
LICENSE_FILE = REPO_ROOT / ".LICENSE_KEY"
LICENSE_KEY = LICENSE_FILE.open("rt").read().strip()

def initialize_SDK():
    global faceMe_sdk
    faceMe_sdk = FaceMeSDK()
    app_bundle_path = os.path.dirname(os.path.realpath(__file__))
    app_cache_path = os.path.join(os.getenv('HOME'), ".cache")
    app_data_path = os.path.join(os.getenv('HOME'), ".local", "share")
    options = {}

    ret = faceMe_sdk.initialize(LICENSE_KEY, app_bundle_path, app_cache_path, app_data_path, options)
    if FR_FAILED(ret):
        outputDict = {"Result": "Fail",
                      "Error Code": ret,
                      "Error Reason": "Fail to register license"}
        OutputJsonResult(outputDict)
        return ret
    return ret


initialize_SDK()

def pil2cv(image) -> np.ndarray:
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image: np.ndarray):
    ''' OpenCV型 -> PIL型 '''
    from PIL import Image
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def OutputJsonResult(outputStr):
    print(json.dumps(outputStr, sort_keys=False, indent=2, separators=(',', ': '), ensure_ascii=False))
def putText_utf(cvimg: np.ndarray, unicode_text: str, org: Tuple, font_size: int, color) -> np.ndarray:
    """
    cv2.putText() like function.

    Note: cv2.putText() cannot handle Unicode Text.
    :param cvimg:
    :param unicode_text:
    :param org:
    :param font_size:
    :param color:
    :return:
    """
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    im = cv2pil(cvimg)
    draw = ImageDraw.Draw (im)
    FONT_TTF = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    unicode_font = ImageFont.truetype(FONT_TTF, font_size)
    draw.text (org, unicode_text, font=unicode_font, fill=color)
    out_cvimg = pil2cv(im)
    return out_cvimg


def gen_output_dict(ret, similar_faces: List, recognized: Dict) -> Dict:
    if ret == FaceMe.FR_RETURN_NOT_FOUND or len(similar_faces) == 0:
        return {"Result": "Fail",
                      "Error Code": ret,
                      "Error Reason": "Similar face not found",
                      "boundingBox": recognized["boundingBox"]}
    elif FR_FAILED(ret):
        return {"Result": "Fail",
                      "Error Code": ret,
                      "Error Reason": "Fail to search similiar face",
                      "boundingBox": recognized["boundingBox"]}
    else:
        return {"Result": "Success",
                      "Similiar Face Info": similar_faces,
                      "boundingBox": recognized["boundingBox"]}
def draw_recognized(out_cvimg, recognize_results, search_results, enable_print=False) -> np.ndarray:
    for recognized, searched in zip(recognize_results, search_results):
        ret, similar_faces = searched
        outputDict = gen_output_dict(ret, similar_faces, recognized)
        if enable_print:
            OutputJsonResult(outputDict)
        person = similar_faces[0]["name"] if similar_faces else "visitor"

        bbox = recognized["boundingBox"]
        (xl, yu), (xr, yd) = bbox
        cv2.rectangle(out_cvimg, (xl, yu), (xr, yd), color=(0, 255, 0), thickness=3)
        out_cvimg = putText_utf(out_cvimg, unicode_text=person, org=(xl, yu), font_size=36, color=(255, 0, 0))
    return out_cvimg

def bbox_and_name(recognize_results, search_results):
    r = []
    for recognized, searched in zip(recognize_results, search_results):
        ret, similar_faces = searched
        person = similar_faces[0]["name"] if similar_faces else "visitor"
        recognized["boundingBox"]
        r.append((recognized["boundingBox"], person))
    return r

def process_image(img: np.ndarray) -> Tuple[Dict, Dict]:
    ret, faceme_img = faceMe_sdk.convert_opencvMat_to_faceMe_image(img)
    images = [faceme_img]
    ret, recognize_results = faceMe_sdk.recognize_faces(images)
    if FR_FAILED(ret):
        outputDict = {"Result": "Fail",
                      "Error Code": ret,
                      "Error Reason": "Fail to recognize face"}
        OutputJsonResult(outputDict)
        exit()

    search_config = {'maxNumOfCandidates': 2, 'far': "1E-5"}

    search_results = [
        faceMe_sdk.search_similar_faces(recognized['faceFeatureStruct'], search_config) for recognized in recognize_results
    ]
    return recognize_results, search_results

