from __future__ import print_function
import requests
import json
import cv2

addr = 'http://localhost'
test_url = addr + '/preprocess'

# prepare headers for http request
content_type = 'image/jpg'
headers = {'content-type': content_type}

img = cv2.imread('lena.jpg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)

# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

print(json.loads(response.text))


# decode response
#image = response.json()#jsonpickle.decode(response.content)
#print(image)

#info = json.loads(response.json())
#print(info)
#cv2.imdecode(np.frombuffer(image, np.uint8), 1)
#cv2.imshow('Result', image)
