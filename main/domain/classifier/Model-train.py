import os
from yolov10.ultralytics import YOLOv10

data_path = './main/data/data.yaml'
os.environ['WANDB_MODE'] = 'disabled'

model = YOLOv10.from_pretrained("jameslahm/yolov10n")
model.train(data=data_path, epochs=50, batch=32)
