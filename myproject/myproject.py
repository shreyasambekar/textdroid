import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import base64
from PIL import Image

import cv2
from image_processing import process_image

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
    filepath = "/home/shreyas/BTECHPROECT/myproject/image/" + filename + '.jpg'

    with open(filepath, 'wb') as f:
        f.write(imgdata)
        f.close()
    
    processed_image = process_image(filepath)
    
    cv2.imwrite('result.jpg', processed_image)
    #try:
    #   with Image.open(filepath) as image:
    #        image.save("/home/hbubuntu/myproject/image/" + filename + ".jpg")
    #except:
    #    return "error in jpg save file"
    return "OK"


if __name__ == "__main__":
    app.run('0.0.0.0')
