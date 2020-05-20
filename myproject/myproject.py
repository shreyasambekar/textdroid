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
    
    return "OK"


if __name__ == "__main__":
    app.run('0.0.0.0')

