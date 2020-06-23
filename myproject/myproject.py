import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
import logging
import os, sys, stat
import time
from ImagePreprocessing import openImage, Setting_image_to_300DPI, convertToGrayscale, shadowRemoval, borderRemoval, deskew, imageBinarisation,checkBackgroundColor, Inversion, saveImage, deleteFiles
from PIL import Image
import tempfile
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
from IPython.display import display

app = Flask(__name__)


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/file-upload', methods=['POST'])
def uploadimg():
    data = dict(request.form)
    img = data['image']
    try:
        imgdata = base64.b64decode(img)
    except:
        return "base64 decode error"
    filename = data['filename']
    filepath = "/home/ubuntu/BTECHPROECT/myproject/images_from_client/" + filename + '.jpg'

    with open(filepath, 'wb') as f:
        f.write(imgdata)
        f.close()

    os.chmod(filepath, 0o666)

    image = Image.open(filepath)
    rescaledImage = Setting_image_to_300DPI(image, filename)
    l = convertToGrayscale(rescaledImage)
    #saveImage(l[1], image_no, 'Grayscale')
    rotatedImage = deskew(l[1], l[0], (0, 0, 0))
    #saveImage(rotatedImage, image_no, 'Rotated')
    binImage = imageBinarisation(rotatedImage)
    color = checkBackgroundColor(binImage)
    if color == 'white' :
        imageWithoutShadow = shadowRemoval(rotatedImage)
        #saveImage(imageWithoutShadow, image_no, 'WithoutShadow')
        imageWithoutBorder = borderRemoval(imageWithoutShadow)
        #saveImage(imageWithoutBorder, image_no, 'WithoutBorder')
        binarisedImage = imageBinarisation(imageWithoutBorder)
    else :
        binarisedImage = imageBinarisation(rotatedImage)
    #saveImage(binarisedImage, image_no, 'Binarised')
    invertedImage = Inversion(binarisedImage, color)
    deleteFiles('/home/ubuntu/BTECHPROECT/myproject/RescaledImages/')
    deleteFiles('/home/ubuntu/BTECHPROECT/myproject/images_from_client/')
    saveImage(invertedImage, filename, 'static/processed_images')
    
    return filename


if __name__ == "__main__":
    print(os.getcwd())
    app.run(host='0.0.0.0')

