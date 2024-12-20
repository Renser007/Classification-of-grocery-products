import os
from handle_db import SaveDb

from yolov10.ultralytics import YOLOv10


class Train:
    def train(self):
        data_path = './main/data/data.yaml'
        os.environ['WANDB_MODE'] = 'disabled'

        model = YOLOv10.from_pretrained("jameslahm/yolov10n")
        model.train(data=data_path, epochs=50, batch=32)

        saveWeights = SaveDb()
        saveWeights.insert_record('active', './runs/detect/train11/weights/best.pt')


if __name__ == "__main__":
    obj_b = Train()
    obj_b.train()
