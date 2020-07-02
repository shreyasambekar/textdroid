We have made changes in the [textfairy][1] application so that it uses tesseract version 4. Also option is given in the
application to upload image to the server allowing to employ processing power of the server to implement different image
processing operations to improve the accuracy.

You can drop us a mail at shreyasambekar2@gmail.com/hrishibudhwant@gmail.com/pranitgandhi98@gmail.com for configuration files of nginx and gunicorn on
server, feature ideas or other queries.

Textdroid
=========

Android OCR App


Features
--------
* convert images to pdf
* recognize text in images
* upload images to server for prerprocessing for better accuracy
* basic document management
 * delete
 * edit
 * merge multiple documents into one
 * view table of content

Project Structure
-----------------
* *app* contains the android app code
* *myproject* contains the server side files. Server setup was done on aws using the instructions in the following link.
  https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
* *app/libs/hocr2pdf* contains c++ code to create pdf files
* *app/libs/image_processing* contains image processing code (binarization and page segmentation)
  * can be compiled to a command line executable main.cpp 
  * *app/libs/image_processing/CppTestProject* contains an XCode project to debug and test the image processing code on desktop
* *app/libs/[leptonica][6]*, *app/libs/[libjpeg][3]*, *app/libs/[libpng-android][4]*, *app/libs/[hocr2pdf][2]* and *app/libs/[tesseract][5]* are external dependencies that where added to the sources directly either because they were modified or they are not available as git repos.
* *Devanagari_OCR.zip* contains the images of Hindi, Marathi, Sanskrit, Nepalese, Konkani and Rajasthani language texts that were used to test image processing operations and measure the OCR accuracy.

You can visit [textfairy github repo][1] for build related and other information.


[1]: https://github.com/renard314/textfairy
[2]: http://www.exactcode.com/site/open_source/exactimage/hocr2pdf/
[3]: http://libjpeg.sourceforge.net/
[4]: https://github.com/julienr/libpng-android
[5]: https://github.com/tesseract-ocr/tesseract
[6]: https://github.com/DanBloomberg/leptonica

