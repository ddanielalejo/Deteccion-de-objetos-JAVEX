"""
Este programa tiene como objetivo la detección de anillos de colores en un video, basado en procesamiento 
de imágenes con OpenCV. El código detecta objetos rojos y azules, especificamente, los anillos usados en la 
competencia de VEX 2024-2025 High Stakes, en estos dibuja contornos apropiados alrededor de ellos.

Autor: María Lucía Peña - Nicolas Garcia - Daniel Vergara 
Fecha: 24 - 11 - 2025
Dependencias: OpenCV, NumPy

"""

import cv2
import numpy as np

# Se definen los intervalos para los colores que se detectaran con el fin de en un solo codigo se detecten ambos. 
# Los colores se definen mediante la transformación no lineal del espacio de color RGB, HSV, traducida con HSV
# [H:0–179, S:0–255, V:0–255].

lower_red = np.array([175, 50, 50])     # Límite inferior para el rojo
upper_red = np.array([180, 255, 255])   # Límite superior para el rojo
lower_blue = np.array([80, 120, 150])   # Límite inferior para el azul
upper_blue = np.array([120, 255, 255])  # Límite superior para el azul

"""
Detecta objetos rojos en el fotograma dado y dibuja sus contornos.
    
Parametros:
frame: Fotograma capturado desde la cámara.
        
Returns:
frame: Fotograma con los objetos detectados y sus detalles dibujados.

"""
def detect_red_object(frame):

    # Se convierte la imagen a la codificacion de color HSV teniendo en cuenta que inicia siendo BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    # Se crea una máscara para el color rojo 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Detecta los contornos directamente en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Itera para cada contorno encontrado
    for contour in contours:
        if cv2.contourArea(contour) > 500:                          # Filtra los objetos pequeños
            x, y, w, h = cv2.boundingRect(contour)                  #Dibuja el rectangulo delimitador
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Calcula una distancia aproximada según el ancho del objeto
            if w != 0:
                distance = 100 / w
            else:
                distance = 0

            #Genera las coordenadas del objeto
            center_x = x + w // 2
            center_y = y + h // 2

            #Muestra el centro del objeto
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    return frame

"""
Detecta objetos azules en el fotograma dado y dibuja sus contornos.
    
Parametros:
frame: Fotograma capturado desde la cámara.
        
Returns:
frame: Fotograma con los objetos detectados y sus detalles dibujados.

"""
def detect_blue_object(frame):
    # Se convierte la imagen a la codificacion de color HSV teniendo en cuenta que inicia siendo BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     # Se crea una máscara para el color azul
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Detecta los contornos directamente en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Itera para cada contorno encontrado
    for contour in contours:
        if cv2.contourArea(contour) > 500:                              # Filtra los objetos pequeños
            x, y, w, h = cv2.boundingRect(contour)                      # Se crea y dibuja el rectangulo delimitador
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Se generan las coordenadas
            center_x = x + w // 2
            center_y = y + h // 2

            # Se dibuja el centro del anillo
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 255), -1)

    return frame

"""
Función principal para capturar video desde la cámara, detectar objetos rojos y azules, 
y mostrar los resultados.

El objetivo de este código es verificar la capacidad de detectar los anillos segun su color, como parte
de una versión inicial del desarrollo.

"""
def main():

    # Accede a la cámara del computador
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error al abrir la cámara")
        return

    print("Presiona 'q' para salir del programa")

    while True:
        ret, frame = cap.read()                                     #Lee cada fotograma desde la camara
        if not ret:
            print("Error al leer el fotograma")
            break

        frame = detect_red_object(frame)                             # Detecta los objetos rojos y azules
        frame = detect_blue_object(frame)
        cv2.imshow('Detección de Objetos Rojos y Azules', frame)     # Muestra el fotograma procesado

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y cierra las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
