
'''
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
from PIL import Image
from flask import send_file
import cv2
from AutomatedImagePreprocessing import openImage, imageRescaling, convertToGrayscale, shadowRemoval, borderRemoval, deskew, imageBinarisation,checkBackgroundColor, Inversion, saveImage


app = Flask(__name__)


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
    filepath = "/home/shreyas/BTECHPROECT/myproject/images_from_client/" + filename + '.jpg'

    with open(filepath, 'wb') as f:
        f.write(imgdata)
        f.close()
        
    image = Image.open(filepath)
    rescaledImage = imageRescaling(image, filename)
    l = convertToGrayscale(rescaledImage)
    #saveImage(l[1], image_no, 'Grayscale')
    rotatedImage = deskew(l[0])
    imageWithoutShadow = shadowRemoval(rotatedImage)
    #saveImage(imageWithoutShadow, image_no, 'WithoutShadow')
    imageWithoutBorder = borderRemoval(imageWithoutShadow)
    #saveImage(imageWithoutBorder, image_no, 'WithoutBorder')
    #saveImage(rotatedImage, image_no, 'Rotated')
    binarisedImage = imageBinarisation(imageWithoutBorder)
    #saveImage(binarisedImage, image_no, 'Binarised')
    color = checkBackgroundColor(binarisedImage)
    invertedImage = Inversion(binarisedImage, color)
    saveImage(invertedImage, filename, 'static/processed_images')
    
    return filename


if __name__ == "__main__":
    app.run('0.0.0.0')
'''


import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
import logging
import os, sys, stat
import time
from AutomatedImagePreprocessing import openImage, imageRescaling, convertToGrayscale, shadowRemoval, borderRemoval, deskew, imageBinarisation,checkBackgroundColor, Inversion, saveImage
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
    filepath = "/home/shreyas/BTECHPROECT/myproject/images_from_client/" + filename + '.jpg'

    with open(filepath, 'wb') as f:
        f.write(imgdata)
        f.close()

    os.chmod(filepath, 0o666)
    #try:
    #   with Image.open(filepath) as image:
    #        image.save("/home/hbubuntu/myproject/image/" + filename + ".jpg")
    #except:
    #    return "error in jpg save file"

    image = Image.open(filepath)
    rescaledImage = imageRescaling(image, filename)
    l = convertToGrayscale(rescaledImage)
    #saveImage(l[1], image_no, 'Grayscale')
    rotatedImage = deskew(l[0])
    imageWithoutShadow = shadowRemoval(rotatedImage)
    #saveImage(imageWithoutShadow, image_no, 'WithoutShadow')
    imageWithoutBorder = borderRemoval(imageWithoutShadow)
    #saveImage(imageWithoutBorder, image_no, 'WithoutBorder')
    #saveImage(rotatedImage, image_no, 'Rotated')
    binarisedImage = imageBinarisation(imageWithoutBorder)
    #saveImage(binarisedImage, image_no, 'Binarised')
    color = checkBackgroundColor(binarisedImage)
    invertedImage = Inversion(binarisedImage, color)
    saveImage(invertedImage, filename, 'static/processed_images')
    
    return "OK"

@app.route('/file-download', methods=['POST'])
def downloadimg():
    try:
        data = dict(request.form)
    except:
        return "Error retrieving data"
    try:
        filename = data['filename']
    except:
        return "Error in retrieving filename"
    filepath = '/home/shreyas/BTECHPROECT/myproject/static/processed_images/' + filename + '.jpg'
    #filepath = '/image/' + filename + '.jpg'
    time.sleep(2)
    try:
        f = open(filepath, 'rb')
    except:
        #f.close()
        return os.getcwd()
    #f = open(filepath, 'rb')
    try:
        imgdata = f.read()
    except:
        f.close()
        return "File reading error"
    finally:
        f.close()

    try:
        imgencoded = base64.b64encode(imgdata)
    except:
        return "base64 error"
    return imgencoded

if __name__ == "__main__":
    print(os.getcwd())
    app.run(host='0.0.0.0')

