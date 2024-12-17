import os
from yolov10.ultralytics import YOLOv10
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
import imghdr


data_path = './data/data.yaml'
os.environ['WANDB_MODE'] = 'disabled'


model = YOLOv10.from_pretrained("jameslahm/yolov10n")
model.train(data=data_path, epochs=5, batch=16)



