# Deteccion de objetos JAVEX
## Integrantes
Nicolas Garcia Ramirez, Maria Lucia Peña Martinez y Daniel Alejandro Vergara Diaz
## Objetivo
Desarrollar un sistema capaz de identificar los anillos de VEX por medio de una camara digital y un codigo en un lenguaje de programacion basándose en su color, forma y distancia a la que se encuentran dichos objetos para ser mas eficientes en la competición.
## Librerias necesarias
Python 3.12, OpenCV2, Numpy, OS
## Flujo de trabajo para el codigo final
### -Carga de video y umbral de colores
Se carga al codigo un video ya grabado anteriormente y se establecen los umbrales de los colores que van a ser detectados.
### -Seleccion de color
El usuario escoge si quiere detectar anillos rojos o azules dependiendo del equipo que sea.
### -Conversion a HSV
Se convierte el fotograma del video de BGR a HSV para segmentar los colores con mas precision.
### -Archivo cargado correctamente
Se verifica que el archivo de entrada exista y pueda abrirse. De lo contrario aparecera un mensaje de error y se cerrara el programa.
### -Cargar video
Si el video puede cargarse exitosamente entonces se creara una salida para el video procesado o si no saldra un error y se finalizara el programa.
### -Creacion de archivos
Se obtienen las propiedades del video original como lo son el ancho,alto y FPS para crear dos salidas procesadas las cuales seran la de velocidad normal y la de velocidad reducida a la mitad; este ultimo se crea para mejorar la visualizacion.
### -Procesamiento de video
