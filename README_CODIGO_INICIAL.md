## Objetivo
Este programa tiene como objetivo la detección de anillos de colores en un video, basado en procesamiento de imágenes con OpenCV. El código detecta objetos rojos y azules, especificamente, los anillos usados en la competencia de VEX 2024-2025 High Stakes, en estos dibuja contornos apropiados alrededor de ellos.
competencia de VEX 2024-2025 High Stakes, en estos dibuja contornos apropiados alrededor de ellos.
## Librerias utilizadas
Python 3.12, Numpy y OpenCV2
## Flujo de trabajo para el codigo inicial
### Definicion de intervalos
 Se definen los intervalos para los colores que se van a detectar (lower_red, upper_red, lower_blue, upper blue) con el fin de que en un solo codigo se detecten ambos.
### Capturar video desde la camara
Se accede a la camara del computador y se comprueba si se pudo leer un fotograma dado por la camara del computador. Sino se pudo leer ningun fotograma entonces aparece un error y se cierra el programa; de lo contrario se continua el analisis.
### Deteccion de objetos rojos y azules
Los colores se definen mediante la transformación no lineal del espacio de color BGR traducida con HSV por lo que si se detecta algun color dentro del umbral previamente establecido entonces se dibujara su contorno y su centro debido a la aplicacion de mascaras de mascaras para azul y rojo.
### Fotograma procesado
Aparecera el fotograma procesado con los objetos detectados
### Finalizacion del programa
El usuario escogera si quiere detener el bucle presionando la letra 'q'; si lo hace entonces liberará la camara y cerrará todas las ventanas.
