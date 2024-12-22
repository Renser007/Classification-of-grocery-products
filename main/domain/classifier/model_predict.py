import cv2
import re
from yolov10.ultralytics import YOLOv10 as YOLO


# image_path = "C:/MastersProject/Classification-of-grocery-products/main/data/test/images/IMG_1117_rotated180_jpg.rf.6357826749278bdf988d1b11890f1937.jpg"
# model = YOLO('C:/MastersProject/Classification-of-grocery-products/runs/detect/train11/weights/best.pt')

class Predict:
    model = YOLO('C:/MastersProject/Classification-of-grocery-products/runs/detect/train11/weights/best.pt')

    def predict(self, chosen_model, img, classes=None, conf=0.5):
        if classes is None:
            classes = []
        if classes:
            results = chosen_model.predict(img, classes=classes, conf=conf)
        else:
            results = chosen_model.predict(img, conf=conf)

        return results

    def predict_and_detect(self, output_path, chosen_model, img, classes=[], conf=0.5):
        results = self.predict(chosen_model, img, classes, conf=conf)
        products = []

        for box in results[0].boxes:  # Loop through all predictions
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract bounding box coordinates
            conf = box.conf[0].item()  # Extract confidence score
            cls = int(box.cls[0].item())  # Extract class index

            # Get the label for the class
            label = f'{chosen_model.names[cls]} {conf:.2f}'
            product = re.sub(r'\d+(\.\d+)?', '', label).strip()
            products.append(product)

            # Draw bounding box and label
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 5)

        cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGBA2RGB))

        return img, products