LOCAL_PATH := $(call my-dir)

ILEPTONICA_PATH := $(LOCAL_PATH)/libs/ileptonica/leptonica

LEPTONICA_PATH := $(LOCAL_PATH)/libs/leptonica/leptonica
TESSERACT_PATH := $(LOCAL_PATH)/libs/tesseract/tesseract
HOCR2PDF_PATH := $(LOCAL_PATH)/libs/hocr2pdf/hocr2pdf
LIBPNG_PATH := $(LOCAL_PATH)/libs/libpng
LIBJPEG_PATH := $(LOCAL_PATH)/libs/libjpeg
IMAGE_PROCESSING_PATH := $(LOCAL_PATH)/libs/image_processing/image_processing
ADAPTIVE_BINARIZER_PATH := $(LOCAL_PATH)/libs/image_processing/image-processing-private

HLIBPNG_PATH := $(LOCAL_PATH)/libs/libpng-android/jni
HLIBJPEG_PATH := $(LOCAL_PATH)/libs/hlibjpeg


include $(ILEPTONICA_PATH)/../Android.mk

include $(LIBPNG_PATH)/Android.mk
include $(LIBJPEG_PATH)/Android.mk
include $(HOCR2PDF_PATH)/../Android.mk
include $(LEPTONICA_PATH)/../Android.mk
include $(TESSERACT_PATH)/../Android.mk
include $(IMAGE_PROCESSING_PATH)/../Android.mk

include $(HLIBPNG_PATH)/Android.mk
include $(HLIBJPEG_PATH)/Android.mk

