# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 16:34:35 2019

@author: skambli
"""

from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()
print(execution_path)
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "storeimage.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )