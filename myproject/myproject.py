# -*- coding: utf-8 -*-
import logging
import os
import tempfile
import io
import base64

import werkzeug
from flask import Flask, jsonify
from flask import abort
from flask import request, Response


import jsonpickle
import numpy as np
import cv2


from image_preprocessing.remove_noise import process_image_for_ocr



app = Flask(__name__)



@app.route('/preprocess', methods=['POST'])
def process():
    _setup()  #Loads model and weights - takes ~2 seconds
    r = request
    nparr = np.fromstring(r.data, np.uint8)  #convert string of image data to uint8
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  #decode image
    cv2.imwrite('server.jpg', img)
    img = process_image_for_ocr('/home/shreyas/BTECHPROECT/myproject/server.jpg')  #processing the image
    #cv2.imshow('Result', img)
    #cv2.waitkey()
    cv2.imwrite('result.jpg', img)
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    _, img_encoded = cv2.imencode('.jpg', img)  #again encode the image
    cv2.imwrite('new.jpeg', img)  #also write non-encoded image
    # build a response dict to send back to client
    #response = img_encoded
    #response_pickled = jsonpickle.encode(response.tostring())  #encode response using jsonpickle
    #return Response(response=response_pickled, status=200, mimetype="application/json")
    return flask.jsonify(response_value_1=img_encoded)


def _setup():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
