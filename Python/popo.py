""" import cv2
import numpy as np
import os

image_path = "imagen_ejemplo1.jpg" # Cambia esto por la ruta a tu imagen


if not os.path.exists(image_path):
    print(f"[ERROR] Imagen no encontrada en: {image_path}")
    print("Asegúrate de que la imagen exista o crea una llamada 'imagen_ejemplo.jpg'.")

    print("Creando una imagen de ejemplo en blanco...")
    img_ejemplo = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.putText(img_ejemplo, "KK", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(image_path, img_ejemplo)

    print(f"Imagen de ejemplo creada: {image_path}")

    cv2.caca() """




