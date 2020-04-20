from PIL import Image
import tempfile
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils

def process_image(filepath):
	#Image Rescaling
	im = Image.open(filepath)
	length_x, width_y = im.size
	factor = min(1, float(1024.0 / length_x))
	size = int(factor * length_x), int(factor * width_y)
	im_resized = im.resize(size, Image.ANTIALIAS)
	temp_file = tempfile.NamedTemporaryFile(delete=False,   suffix='.jpg')
	rescaledImage = temp_file.name
	im_resized.save(rescaledImage, dpi=(300, 300))

	#Conversion to Grayscale
	src = cv2.imread(rescaledImage) 
	grayScaleImage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY, dstCn = 2)

	#Noise Removal using Median Blurring
	DenoisedImage = cv2.medianBlur(grayScaleImage, 3)

	#Shadow Removal
	#img = cv2.imread('C:/Users/hp/Desktop/AndroidOCR/denoising-dirty-documents/test/test/1.png', -1)
	rgb_planes = cv2.split(DenoisedImage) 
	result_planes = []
	for plane in rgb_planes:
	    dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
	    bg_img = cv2.medianBlur(dilated_img, 21)
	    diff_img = 255 - cv2.absdiff(plane, bg_img)
	    result_planes.append(diff_img)
	result = cv2.merge(result_planes)

	#Removal of Border
	mask = np.zeros(result.shape, dtype=np.uint8) #it was DenoisedImage earlier
	cnts = cv2.findContours(DenoisedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	cv2.fillPoly(mask, cnts, [255,255,255])
	mask = 255 - mask
	imageWithoutBorder = cv2.bitwise_or(DenoisedImage, mask)

	#Image Binarisation
	binarisedImage = cv2.threshold(imageWithoutBorder, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

	#Image Deskewing
	coords = np.column_stack(np.where(binarisedImage > 0))
	angle = cv2.minAreaRect(coords)[-1]
	if angle < -45:
		angle = -(90 + angle)
	else:
		angle = -angle

	(h, w) = binarisedImage.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotatedImage = cv2.warpAffine(binarisedImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
	
	#cv2.putText(rotatedImage, "Angle: {:.2f} degrees".format(angle),
	#	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	#print("[INFO] angle: {:.3f}".format(angle))

	#Image Inversion
	invertedImage = cv2.bitwise_not(rotatedImage)

	#Shadow Removal
	#img = cv2.imread('C:/Users/hp/Desktop/AndroidOCR/denoising-dirty-documents/test/test/1.png', -1)
	#rgb_planes = cv2.split(invertedImage)
	#result_planes = []
	#for plane in rgb_planes:
	#    dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
	#    bg_img = cv2.medianBlur(dilated_img, 21)
	#    diff_img = 255 - cv2.absdiff(plane, bg_img)
	#    result_planes.append(diff_img)
	#result = cv2.merge(result_planes)
	return invertedImage #it was return result earlier
	
	#cv2.imwrite('shadows_out.png', result)





