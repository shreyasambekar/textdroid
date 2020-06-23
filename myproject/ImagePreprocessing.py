#!/usr/bin/env python
# coding: utf-8

# In[426]:


import PIL
import cv2
import numpy as np
import os
from PIL import Image

#newly added modules :

import natsort
from typing import Tuple, Union
import math
from deskew import determine_skew


# In[412]:


def Setting_image_to_300DPI(img, img_ref) :
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    imgResult = img.resize(size, Image.ANTIALIAS).convert('RGB')
    if img.mode != 'RGB':
        img = img.convert('RGB')
    name = '/home/ubuntu/BTECHPROECT/myproject/RescaledImages/' + img_ref + '.jpg'
    img.save(name, dpi = (300, 300))
    return name


# In[413]:


def convertToGrayscale(img) :
    im = cv2.imread(img)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY, dstCn = 2)
    angle = determine_skew(image)
    if(angle == None):
        angle = 0
    grayScaleImage = PIL.Image.fromarray(image)
    l = [angle, grayScaleImage]
    return l


# In[414]:


def shadowRemoval(img) :
    arr = np.array(img)
    rgb_planes = cv2.split(arr)
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    result = cv2.merge(result_planes)
    imageWithoutShadow = PIL.Image.fromarray(result)
    return imageWithoutShadow


# In[415]:


def borderRemoval(img) :
    arr = np.array(img)
    mask = np.zeros(arr.shape, dtype=np.uint8)
    cnts = cv2.findContours(arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]  
    cv2.fillPoly(mask, cnts, [255,255,255])
    mask = 255 - mask
    result = cv2.bitwise_or(arr, mask)
    imageWithoutBorder = PIL.Image.fromarray(result)
    return imageWithoutBorder


# In[416]:


def deskew(image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
    image = np.array(image)
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    result = cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)
    rotatedImage = PIL.Image.fromarray(result)
    return rotatedImage


# In[417]:


def imageBinarisation(img) :
    arr = np.array(img)
    result = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    binarisedImage = PIL.Image.fromarray(result)
    return binarisedImage


# In[418]:


def checkBackgroundColor(img, black_max_bgr=(50)) :
    arr = np.array(img)
    mean_bgr_float = np.mean(arr, axis=(0,1))
    mean_bgr_rounded = np.round(mean_bgr_float)
    mean_bgr = mean_bgr_rounded.astype(np.uint8)
    mean_intensity = int(round(np.mean(arr)))
    return 'black' if np.all(mean_bgr < black_max_bgr) else 'white'


# In[419]:


def Inversion(img, color) :
    arr = np.array(img)
    result = arr if color == "white" else cv2.bitwise_not(arr)
    invertedImage = PIL.Image.fromarray(result)
    return invertedImage


# In[420]:


def saveImage(img, img_ref, folder) :
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    image = img.resize(size, Image.ANTIALIAS)
    name = '/home/ubuntu/BTECHPROECT/myproject/' + folder + '/' + img_ref + '.jpg'
    image.save(name, 'JPEG')


# In[421]:


def deleteFiles(path) :
    for f in os.listdir(path):
        os.remove(path + f)

def openImage(img) :
    image = Image.open(img)
    return image
