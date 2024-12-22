import io
import os
from collections import Counter

import cv2
from nicegui import events, ui

from main.domain.classifier.handle_db import SaveDb
from main.domain.classifier.model_predict import Predict

output_path = "C:/MastersProject/Classification-of-grocery-products/main/outputs/output.jpg"

def predict_and_display(image):
    predictor = Predict()

    result_image, prediction = predictor.predict_and_detect(output_path, predictor.model, image, None, conf=0.5)
    return result_image, prediction


def main():

    dbService = SaveDb()

    def handle_upload(event):
        uploaded_file = event.content
        image = cv2.imread(uploaded_file)

        result_image, prediction = predict_and_display(image)
        result_display.set_source(output_path)
        result_display.force_reload()

        product_counts = Counter(prediction)

        prices = dbService.retrieve_price(prediction)
        price_dict = {product_name: price for product_name, price in prices}

        table_data = []
        for product, quantity in product_counts.items():
            if product in price_dict:
                price = price_dict[product]
                subtotal = price * quantity
                table_data.append({
                    'Product': product,
                    'Quantity': quantity,
                    'Price': price,
                    'Subtotal': subtotal
                })

        label_container.rows.clear()
        label_container.update()
        label_container.add_rows(table_data)

        total = sum(product_counts[product] * price_dict[product] for product in product_counts if product in price_dict)
        total_price.set_text('Total cost: ' + str(total))

    with ui.row():
        with ui.column():
            upload = ui.upload(on_upload=handle_upload, label="Predict")
            result_display = ui.image().style('width: 100%; margin: 20px auto; display: block;')
        with ui.column():
            with ui.column().style('width: 100%; margin: 20px auto; display: block;'):
                ui.label('Predicted Products:').style('font-weight: bold; margin-bottom: 10px;')
                label_container = ui.table(
            columns=[
                {'name': 'Product', 'label': 'Product', 'field': 'Product'},
                {'name': 'Quantity', 'label': 'Quantity', 'field': 'Quantity'},
                {'name': 'Price', 'label': 'Price', 'field': 'Price'},
                {'name': 'Subtotal', 'label': 'Subtotal', 'field': 'Subtotal'},
            ], rows = [])
                total_price = ui.label().style('margin-top: 10px;')


ui.run(native=True)

if __name__ in {"__main__", "__mp_main__"}:
    main()
