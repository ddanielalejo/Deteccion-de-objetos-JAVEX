"""
Este programa tiene como objetivo la detección de anillos de colores en un video, basado en procesamiento 
de imágenes con OpenCV. El código detecta objetos rojos y azules, especificamente, los anillos usados en la 
competencia de VEX 2024-2025 High Stakes, en estos dibuja contornos apropiados alrededor de ellos y  calcula
su distancia en función de la altura en píxeles.

Autor: María Lucía Peña - Nicolas Garcia - Daniel Vergara 
Fecha: 24 - 11 - 2025
Dependencias: OpenCV, NumPy, os

"""
import cv2           #OpenCV2
import numpy as np   #Para datos matriciales
import os            #Para manejo de archivos

# Se definen los intervalos para los colores que se detectaran con el fin de en un solo codigo se detecten ambos. 
# Los colores se definen mediante la transformación no lineal del espacio de color RGB, HSV, traducida con HSV
# [H:0–179, S:0–255, V:0–255].

colors = {
    'Anillo rojo': {
        'lower': np.array([160, 100, 100]),
        'upper': np.array([179, 255, 255])
    },
    'Anillo azul': {
        'lower': np.array([80, 120, 150]),
        'upper': np.array([120, 255, 255])
    }
}

# Se ajusta un mínimo de área para considerar un contorno como objeto válido, esto debido a que se esta detectando 
# un objeto especifico, sin embargo, estos pueden llegar a estar apilados

MIN_CONTOUR_AREA = 500  

"""
Funcion establecida para la deteccion de objetos basados en el rango de color especificado anteriormente,
donde dibuja sus contornos y calcula su distancia en función de la altura, en esta solo detecta
rectángulos horizontales, es decir, que su ancho sea mayor a su altura. Esta condicion establecida en 
funcion de la forma del objeto a detectar y demas objetos no relevantes en el espacio. 

    Parámetros:
        frame (ndarray): Fotograma del video en formato BGR.
        lower_bound (ndarray): Límite inferior del rango de color en HSV.
        upper_bound (ndarray): Límite superior del rango de color en HSV.
        color_name (str): Nombre del color del objeto que se está detectando.
        real_distance (float) : Distancia de un objeto de referencia
        real_h (float): Altura del objeto de referencia

    Retorna:
        frame (ndarray): Fotograma con las detecciones dibujadas.
        detected_objects (list): Lista de objetos detectados, incluyendo etiqueta, distancia y coordenadas del centro.
"""

def detect_objects(frame, lower_bound, upper_bound, color_name, real_distance, real_h):
    
    # Se convierte la imagen a la codificacion de color HSV teniendo en cuenta que inicia siendo BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Se crea la  máscara para el color seleccionado usando los intervalos designados de acuerdo a HSV
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Se crea una matriz kernel para aplicar la operacion morfologica de apertura o erosion seguida de 
    # dilatacion para reducir el para eliminar pequeños puntos blancos o ruido en la máscara.
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Detecta los contornos de la mascara creada
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crea e inicializa la lista para almacenar los objetos detectados, asimismo, se cuentan los detectados
    detected_objects = []
    object_count = 0

    # Se crea un ciclo para iterar sobre cada contorno detectado donde: 
    for contour in contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:       # Se filtran solo los contornos de interes
            
            x, y, w, h = cv2.boundingRect(contour)            # Se obtiene el rectángulo delimitador

            if w > h:                                         # Filtra solo para rectángulos horizontales
                object_count += 1                             # Realiza el conteo
                cv2.rectangle(frame, (x, y), (x + w, y + h), (211, 211, 211), 2) # Traza el rectangulo
                
                if h != 0:                                    # Calcula la distancia basada en la altura del objeto 
                    distance = ((real_distance* real_h)/10) / h  
                else:
                    distance = 0

                # Define las del centro del objeto
                center_x = x + w // 2
                center_y = y + h // 2

                # Cre al etiqueta del objeto
                label = f"{color_name} {object_count}"

                # Dibuja la etiqueta con fondo negro para una mejor identificacion
                cv2.rectangle(frame, (x, y - 40), (x + 150, y), (0, 0, 0), -1)  # Negro
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # Blanco
                cv2.putText(frame, f"Dist: {distance:.2f}m", (x, y - 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # Blanco

                # Dibuja el centro del objeto
                cv2.circle(frame, (center_x, center_y), 5, (211, 211, 211), -1)  # Gris claro

                # Almacena la información necesaria del objeto, es decir, su etiqueta, su centro y la distancia a la que esta
                detected_objects.append({
                    'label': label,
                    'distance': distance,
                    'center': (center_x, center_y)
                })

    return frame, detected_objects

def main():
    """
    Función principal para procesar un video cargado, detectar objetos, mostrar los resultados y guardar los videos procesados.
    """
    # Se selecciona el color de acuerdo a la alianza establecida 
    print("Selecciona el color para detectar:")
    print("1: Rojo")
    print("2: Azul")
    color_choice = input("Ingrese el número de su elección: ")
    real_distance = 64                                          #Distancia de referencia de un objeto CM
    real_h = 5.58                                               #Altura del objeto CM
    last_print_second = -2                                      #Para imprimir información cada 2 segundos

    if color_choice == '1':
        selected_color = 'Anillo rojo'
    elif color_choice == '2':
        selected_color = 'Anillo azul'
    else:
        print("Opción inválida. Saliendo del programa.")
        return

    # Se asignan los intervalos de acuerdo al color de eleccion
    lower_bound = colors[selected_color]['lower']
    upper_bound = colors[selected_color]['upper']

    video_filename = 'video_recorrido.mp4'                      # Nombre del archivo de video de entrada

    # Verifica si el archivo existe
    if not os.path.isfile(video_filename):
        print(f"El archivo {video_filename} no existe.")
        return
    
    cap = cv2.VideoCapture(video_filename)                      # Cargar el video desde el archivo

    # Carga el video
    if not cap.isOpened():
        print(f"Error al abrir el video {video_filename}.")
        return

    print("Presiona 'q' para salir del programa")

    # Obtiene las propiedades del video original
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_original = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Crea un nuevo video ya procesado a velocidad original
    out_original = cv2.VideoWriter('video_procesado.mp4', fourcc, fps_original, (width, height))

    # Crear un nuevo video ya procesado relentizado a la mitad de velocidad para observar su funcionamiento mejor
    fps_slow = fps_original / 2
    out_slow = cv2.VideoWriter('video_procesado_lento.mp4', fourcc, fps_slow, (width, height))

    while True:
        # Lee fotograma del video
        ret, frame = cap.read()
        if not ret:
            print("Fin del video o error al leer el fotograma")
            break

        # Detecta objetos en el fotograma
        processed_frame, detected_objects = detect_objects(frame, lower_bound, upper_bound, selected_color, real_distance, real_h)

        # Escribe el fotograma procesado en los videos
        out_original.write(processed_frame)
        out_slow.write(processed_frame)

        # Muestra el fotograma procesado
        cv2.imshow('Detección de Objetos', processed_frame)

        # Obtener el tiempo actual del video en milisegundos
        ms_elapsed = cap.get(cv2.CAP_PROP_POS_MSEC)
        seconds = int(ms_elapsed // 1000)
        milliseconds = int(ms_elapsed % 1000)

        # Imprime información solo cada 2 segundos
        if seconds - last_print_second >= 2:
            if detected_objects:
                # Ordena los objetos por distancia (de menor a mayor)
                sorted_objects = sorted(detected_objects, key=lambda obj: obj['distance'])

                # Toma el objeto más cercano
                closest_object = sorted_objects[0]

                # Escribe la instrucción para el objeto más cercano
                instruction = (
                    f"El {closest_object['label']} más cercano está a {closest_object['distance']:.2f} metros, "
                    f"en el segundo {seconds}.{milliseconds:03d}."
                )
                print(instruction)
            else:
                print(f"Segundo {seconds}.{milliseconds:03d}: No se detectaron objetos en el fotograma actual.")

            last_print_second = seconds

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera el video y cierra las ventanas
    cap.release()
    out_original.release()
    out_slow.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()