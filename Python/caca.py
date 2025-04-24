# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os # Importar os para verificar si los archivos existen

# --- Configuración ---
# Rutas a los archivos del modelo MobileNet SSD
# Asegúrate de que estos archivos estén en la misma carpeta o proporciona la ruta completa
prototxt_path = "MobileNetSSD_deploy.prototxt.txt"
model_path = "MobileNetSSD_deploy.caffemodel"
# Ruta a la imagen que quieres analizar
image_path = "imagen_ejemplo.jpg" # Cambia esto por la ruta a tu imagen
# Nivel de confianza mínimo para considerar una detección válida (0.0 a 1.0)
confidence_threshold = 0.4

# --- Validación de Archivos ---
if not os.path.exists(prototxt_path):
    print(f"[ERROR] Archivo prototxt no encontrado en: {prototxt_path}")
    print("Descárgalo desde: https://github.com/opencv/opencv/raw/master/samples/dnn/models/MobileNetSSD_deploy.prototxt.txt")
    exit()

if not os.path.exists(model_path):
    print(f"[ERROR] Archivo del modelo no encontrado en: {model_path}")
    print("Descárgalo desde: https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20180205_fp16/MobileNetSSD_deploy.caffemodel")
    exit()

if not os.path.exists(image_path):
    print(f"[ERROR] Imagen no encontrada en: {image_path}")
    print("Asegúrate de que la imagen exista o crea una llamada 'imagen_ejemplo.jpg'.")
    # Crear una imagen de ejemplo si no existe
    print("Creando una imagen de ejemplo en blanco...")
    img_ejemplo = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.putText(img_ejemplo, "Reemplazar con tu imagen", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(image_path, img_ejemplo)
    print(f"Imagen de ejemplo creada: {image_path}")
    # exit() # Podrías salir aquí o continuar con la imagen en blanco

# --- Cargar el Modelo ---
print("[INFO] Cargando el modelo...")
try:
    # Carga el modelo de detección de objetos (MobileNet SSD) entrenado en el dataset COCO
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    print("[INFO] Modelo cargado exitosamente.")
except cv2.error as e:
    print(f"[ERROR] No se pudo cargar el modelo: {e}")
    print("Verifica que los archivos .prototxt y .caffemodel sean válidos y no estén corruptos.")
    exit()


# --- Clases del Modelo COCO ---
# Estas son las clases que el modelo MobileNet SSD puede detectar
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# --- Cargar y Procesar la Imagen ---
print(f"[INFO] Cargando imagen: {image_path}")
image = cv2.imread(image_path)

if image is None:
    print(f"[ERROR] No se pudo cargar la imagen desde: {image_path}")
    exit()

print("[INFO] Imagen cargada. Procesando...")
(h, w) = image.shape[:2] # Obtener alto y ancho

# Crear un 'blob' desde la imagen.
# Un blob es la imagen preprocesada para la red neuronal.
# Parámetros:
#   image: La imagen de entrada.
#   0.007843: Factor de escala.
#   (300, 300): Tamaño espacial esperado por el modelo MobileNet SSD.
#   127.5: Valores de resta media (para normalizar).
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
                             (300, 300), 127.5)

# --- Realizar Detección ---
print("[INFO] Realizando detección de objetos...")
net.setInput(blob) # Pasar el blob a la red
detections = net.forward() # Obtener las detecciones

# --- Contar Personas ---
person_count = 0
print("[INFO] Analizando detecciones...")

# Iterar sobre todas las detecciones encontradas
for i in np.arange(0, detections.shape[2]):
    # Extraer la confianza (probabilidad) de la detección
    confidence = detections[0, 0, i, 2]

    # Filtrar detecciones débiles (menor confianza que el umbral)
    if confidence > confidence_threshold:
        # Obtener el índice de la clase detectada
        idx = int(detections[0, 0, i, 1])

        # Verificar si la clase detectada es 'person'
        if CLASSES[idx] == "person":
            person_count += 1
            # Opcional: Dibujar un rectángulo alrededor de la persona detectada
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # Dibujar el rectángulo en la imagen original
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            # Añadir etiqueta con la confianza
            label = f"Persona: {confidence:.2f}"
            cv2.putText(image, label, (startX, startY - 15 if startY - 15 > 15 else startY + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# --- Mostrar Resultados ---
print(f"\n[RESULTADO] Número total de personas detectadas: {person_count}")

# Mostrar la imagen con las detecciones (opcional)
# Redimensionar para visualización si es muy grande
scale_percent = 60 # porcentaje de la escala original
if max(h, w) > 1000: # Solo redimensionar si es grande
    width_new = int(w * scale_percent / 100)
    height_new = int(h * scale_percent / 100)
    dim = (width_new, height_new)
    image_display = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
else:
    image_display = image

cv2.imshow("Detecciones", image_display)
print("\nPresiona cualquier tecla en la ventana de la imagen para cerrar.")
cv2.waitKey(0) # Espera a que se presione una tecla
cv2.destroyAllWindows() # Cierra la ventana de la imagen
