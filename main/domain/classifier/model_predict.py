from PIL import Image
import cv2
import numpy as np
import torch
from yolov10.ultralytics import YOLOv10 as YOLO

model = YOLO('C:/MastersProject/Classification-of-grocery-products/runs/detect/train11/weights/best.pt')

image_path = "C:/MastersProject/Classification-of-grocery-products/main/data/test/images/IMG_1117_rotated180_jpg.rf.6357826749278bdf988d1b11890f1937.jpg"

def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results

def predict_and_detect(chosen_model, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
    results = predict(chosen_model, img, classes, conf=conf)
    for result in results:
        for box in result.boxes:
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    return img, results

image = cv2.imread(image_path)
result_img, _ = predict_and_detect(model, image, classes=[], conf=0.5)

cv2.imshow("Image", result_img)
cv2.imwrite("C:/Users/user/Desktop/", result_img)
cv2.waitKey(0)