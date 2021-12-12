import io
import cv2
import base64
import numpy as np

from PIL import Image

#####################################################################################################

class ImageCodecs(object):

    def __init__(self):
        pass

    def decode_image(self, imageData) -> np.ndarray:
        header, imageData = imageData.split(",")[0], imageData.split(",")[1]
        image = np.array(Image.open(io.BytesIO(base64.b64decode(imageData))))
        image = cv2.cvtColor(src=image, code=cv2.COLOR_BGRA2RGB)
        return header, image


    def encode_image(self, header: str, image: np.ndarray) -> str:
        _, imageData = cv2.imencode(".jpeg", image)
        imageData = base64.b64encode(imageData)
        imageData = str(imageData).replace("b'", "").replace("'", "")
        imageData = header + "," + imageData
        return imageData

image_codecs = ImageCodecs()    

#####################################################################################################

class ImageProcessor(object):
    def __init__(self):
        pass

    def blur(self, image: np.ndarray, kernel: int) -> np.ndarray:
        return cv2.GaussianBlur(src=image, ksize=(kernel, kernel), sigmaX=0)
    
    def adjust_gamma(self, image: np.ndarray, gamma: float) -> np.ndarray:
        image = image / 255
        image = np.clip(((image ** gamma) * 255), 0, 255).astype("uint8")
        return image
    
    def adjust_hue(self, image: np.ndarray, hue: float) -> np.ndarray:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_RGB2HSV)
        feature = image[:, :, 0]
        feature = np.clip((hue * feature), 0, 179).astype("uint8")
        image[:, :, 0] = feature
        return cv2.cvtColor(src=image, code=cv2.COLOR_HSV2RGB)

    def adjust_saturation(self, image: np.ndarray, saturation: float) -> np.ndarray:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_RGB2HSV)
        feature = image[:, :, 1]
        feature = np.clip((saturation * feature), 0, 255).astype("uint8")
        image[:, :, 1] = feature
        return cv2.cvtColor(src=image, code=cv2.COLOR_HSV2RGB)

    def adjust_vibrance(self, image: np.ndarray, vibrance: float) -> np.ndarray:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_RGB2HSV)
        feature = image[:, :, 2]
        feature = np.clip((vibrance * feature), 0, 255).astype("uint8")
        image[:, :, 2] = feature
        return cv2.cvtColor(src=image, code=cv2.COLOR_HSV2BGR)
    
    def sharpen(self, image:np.ndarray, ksize: int):
        kernel = cv2.getStructuringElement(shape=cv2.MORPH_CROSS, ksize=(ksize, ksize)) * -1
        kernel[int(ksize / 2), int(ksize / 2)] = ((ksize - 1) * 2) + 1

        image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
        image = np.clip(image, 0, 255).astype("uint8")
        return image

image_processor = ImageProcessor()

#####################################################################################################
