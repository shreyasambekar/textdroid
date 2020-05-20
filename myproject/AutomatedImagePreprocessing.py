#!/usr/bin/env python
# coding: utf-8

# In[160]:

from PIL import Image
import tempfile
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
from IPython.display import display


# In[122]:


def openImage(img) :
    image = Image.open(img)
    return image


# In[215]:


def imageRescaling(img, img_ref) :
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    imgResult = img.resize(size, Image.ANTIALIAS).convert('RGB')
    name = '/home/shreyas/BTECHPROECT/myproject/RescaledImages/' + img_ref + '.png'
    imgResult.save(name, 'PNG')
    return name


# In[237]:


def convertToGrayscale(img) :
    im = cv2.imread(img) 
    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY, dstCn = 2)
    grayScaleImage = Image.fromarray(image)
    l = [image, grayScaleImage]
    # returning a list because saveImage method needs image of type PIL.Image.Image, and shadowRemoval needs numpy.ndarray object
    return l 


# In[238]:


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
    imageWithoutShadow = Image.fromarray(result)
    return imageWithoutShadow


# In[256]:


def borderRemoval(img) :
    arr = np.array(img)
    mask = np.zeros(arr.shape, dtype=np.uint8)
    cnts = cv2.findContours(arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.fillPoly(mask, cnts, [255,255,255])
    mask = 255 - mask
    result = cv2.bitwise_or(arr, mask)
    imageWithoutBorder = Image.fromarray(result)
    return imageWithoutBorder


# In[267]:


def deskew(img) :
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    result = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    rotatedImage = Image.fromarray(result)
    return rotatedImage


# In[275]:


def imageBinarisation(img) :
    arr = np.array(img)
    result = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    binarisedImage = Image.fromarray(result)
    return binarisedImage


# In[277]:


def checkBackgroundColor(img, black_max_bgr=(40)) :
    arr = np.array(img)
    mean_bgr_float = np.mean(arr, axis=(0,1))
    mean_bgr_rounded = np.round(mean_bgr_float)
    mean_bgr = mean_bgr_rounded.astype(np.uint8)
    mean_intensity = int(round(np.mean(arr)))
    return 'black' if np.all(mean_bgr < black_max_bgr) else 'white'


# In[279]:



def Inversion(img, color) :
    arr = np.array(img)
    result = arr if color == "white" else cv2.bitwise_not(arr)
    invertedImage = Image.fromarray(result)
    return invertedImage

# In[241]:


def saveImage(img, img_ref, folder) :
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    image = img.resize(size, Image.ANTIALIAS)
    name = '/home/shreyas/BTECHPROECT/myproject/' + folder + '/' + img_ref + '.png'
    image.save(name, 'PNG')


# In[187]:

"""
images = []
for image in os.listdir('C:/Users/hp/Desktop/AndroidOCR/Devanagari script dataset'):
    images.append('C:/Users/hp/Desktop/AndroidOCR/Devanagari script dataset/' + image) 


# In[280]:


image_no = 1
for im in images :
    image = Image.open(im)
    rescaledImage = imageRescaling(image, image_no)
    l = convertToGrayscale(rescaledImage)
    saveImage(l[1], image_no, 'Grayscale')
    imageWithoutShadow = shadowRemoval(l[0])
    saveImage(imageWithoutShadow, image_no, 'WithoutShadow')
    imageWithoutBorder = borderRemoval(imageWithoutShadow)
    saveImage(imageWithoutBorder, image_no, 'WithoutBorder')
    rotatedImage = deskew(imageWithoutBorder, l[0])
    saveImage(rotatedImage, image_no, 'Rotated')
    binarisedImage = imageBinarisation(rotatedImage)
    saveImage(binarisedImage, image_no, 'Binarised')
    color = checkBackgroundColor(binarisedImage)
    invertedImage = Inversion(binarisedImage, rotatedImage, color)
    saveImage(invertedImage, image_no, 'Inverted')
    image_no += 1
    
"""

# In[ ]:




