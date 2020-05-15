from PIL import Image
import os

from utils.constants import Constants


class Util:
    @staticmethod
    def proportionalThumbnail(image: Image, width=0, height=0) -> None:
        """
            Resize image with keeping proportion

        :param image: pill image object
        :param width: width
        :param height: height
        :return:
        """
        if not width and not height:
            raise AttributeError

        w, h = image.width, image.height
        proportion = max(w, h) / min(w, h)
        size = (
            width or (proportion * image.width),
            height or (proportion * image.height)
        )
        image.thumbnail(size)

    @staticmethod
    def imagePathsGenerator(path: str):
        """
            Return the generator of image file paths contained in directory

        :param path: path to directory
        :return:
        """
        path = os.path.abspath(path)
        expands = Constants.AVAILABLE_EXTENSIONS

        for f in os.listdir(path):
            ext = os.path.splitext(f)[-1]
            if ext.lower() not in expands:
                continue

            yield os.path.join(path, f)
