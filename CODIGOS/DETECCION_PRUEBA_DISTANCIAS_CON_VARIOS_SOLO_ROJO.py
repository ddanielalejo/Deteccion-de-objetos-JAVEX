"""
Este programa tiene como objetivo la detección de anillos rojos mediante la webcam de un computador, basado en
procesamiento de imágenes con OpenCV. El código detecta  especifcamente, los anillos usados en la competencia 
de VEX 2024-2025 High Stakes, en estos dibuja contornos apropiados alrededor de ellos y  calcula su distancia en 
función del ancho en píxeles.

Autor: María Lucía Peña - Nicolas Garcia - Daniel Vergara 
Fecha: 24 - 11 - 2025
Dependencias: OpenCV, NumPy

"""

import cv2
import numpy as np
 

# Se definen los intervalos para el color rojo, estos se definen mediante la transformación no lineal
# del espacio de color RGB, HSV, traducida con HSV [H:0–179, S:0–255, V:0–255].

lower_red = np.array([175, 100, 60])  # Límite inferior para el rojo
upper_red = np.array([180, 255, 255])  # Límite superior para el rojo
 
"""
Detecta objetos rojos en el fotograma dado, dibuja sus contornos y calcula su distancia.
Esta función identifica las áreas que coincidan con el rango de color rojo definido. Posteriormente, 
calcula la distancia aproximada en función del ancho del contorno detectado.
    
Parámetros:

frame (numpy.ndarray): Fotograma capturado desde la cámara.
    
Retorna:

numpy.ndarray: Fotograma procesado con anotaciones visuales para los objetos detectados.

"""
def detect_red_object(frame):

    # Se convierte la imagen a la codificacion de color HSV teniendo en cuenta que inicia siendo BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Crea una máscara para el color rojo
    mask = cv2.inRange(hsv, lower_red, upper_red)                     
    # Detecta los contornos directamente en la máscara              
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    # Inicializa el contador de anillos
    ring_count = 0                                               
 
    # Se itera para cada contorno encontrado 
    for contour in contours:
        if cv2.contourArea(contour) > 500:                      # Se filtran los objetos pequeños de acuerdo a su contorno
            ring_count += 1                                     # Se incrementa el contador
            x, y, w, h = cv2.boundingRect(contour)              # Dibuja el contorno con un rectángulo delimitador
            cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 200, 200), 2)  # Color gris claro
            
            if w != 0:                                          # Calcula la distancia basada en el ancho del anillo
                distance = 100 / w                              # Nota: El factor de escala "100" es arbitrario y se usó para pruebas preliminares.
            else:
                distance = 0
 
            # Se generan las coordenas del centro del anillo
            center_x = x + w // 2
            center_y = y + h // 2
 
            # Dibuja el centro del anillo
            cv2.circle(frame, (center_x, center_y), 5, (200, 200, 200), -1)  # Color gris claro
            cv2.putText(frame, f"Anillo {ring_count}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
            cv2.putText(frame, f"Dist: {distance:.2f}m", (x, y - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
 
    return frame
 

"""
Función principal que utiliza la cámara del computador para capturar video en tiempo real, detectar objetos
rojos en cada fotograma y mostrar los resultados en una ventana.
    
El objetivo de este código es verificar la capacidad de detectar anillos rojos y estimar su distancia 
aproximada, como parte de una versión intermedia del desarrollo.

"""
def main():

    # Accede a la cámara del computador
    cap = cv2.VideoCapture(0)
 
    if not cap.isOpened():
        print("Error al abrir la cámara")
        return
 
    print("Presiona 'q' para salir del programa")
 
    while True:
        ret, frame = cap.read()                                     # Lee cada fotograma desde la cámara
        if not ret:
            print("Error al leer el fotograma")
            break

        processed_frame = detect_red_object(frame)                  # Detecta el objeto rojo en el fotograma
        cv2.imshow('Detección de Anillos Rojos', processed_frame)   # Muestra el fotograma procesado
 
        # Sale del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    # Libera la cámara y cierra las ventanas
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()