# Deteccion de objetos JAVEX
## Integrantes
Nicolas Garcia Ramirez, Maria Lucia Peña Martinez y Daniel Alejandro Vergara Diaz
## Objetivo
Desarrollar un sistema capaz de identificar los anillos de VEX por medio de una camara digital y un codigo en un lenguaje de programacion basándose en su color, forma y distancia a la que se encuentran dichos objetos para ser mas eficientes en la competición.
## Librerias necesarias
Python 3.12, OpenCV2, Numpy, OS
## Flujo de trabajo para el codigo final
### Carga de video y umbral de colores
Se carga al codigo un video ya grabado anteriormente y se establecen los umbrales de los colores que van a ser detectados.
### Seleccion de color
El usuario escoge si quiere detectar anillos rojos o azules dependiendo del equipo que sea.
### Archivo cargado correctamente
Se verifica que el archivo de entrada exista y pueda abrirse. De lo contrario aparecera un mensaje de error y se cerrara el programa.
### Cargar video
Si el video puede cargarse exitosamente entonces se creara una salida para el video procesado o si no saldra un error y se finalizara el programa.
### Creacion de archivos
Se obtienen las propiedades del video original como lo son el ancho,alto y FPS para crear dos salidas procesadas las cuales seran la de velocidad normal y la de velocidad reducida a la mitad; este ultimo se crea para mejorar la visualizacion.
### Conversion a HSV
Se convierte el fotograma del video de BGR a HSV para segmentar los colores con mas precision.
### Creacion de mascara
Genera una mascara binaria para resaltar los pixeles del color deseado dependiendo de que color se haya escogido.
### Reduccion de ruido
Aplica una combinacion de operaciones morfologicas las cuales son erosion y dilatacion para eliminar las imperfecciones en las mascaras.
### Extraccion de contornos
Detecta contornos en la mascara utilzando la funcion cv2.findContours.
### Filtrado por area
Desecha contornos con un area menor al umbral que en este caso seria de 500 pixeles.
### Validacion por forma 
Filtra solo los rectangulos horizontales, es decir, que su ancho sea mayor al alto para asegurarse que lo que se esta detectando es un anillo.
### Calculo de la distancia
Se utiliza la formula distancia=(distancia real X distancia real)/ Altura en contorno de pixeles.
### Etiquetado 
Dibuja un rectángulo, etiqueta con distancia y nombre, y muestra el centro del objeto.
### almacenamiento de datos
Registra información del objeto detectado (etiqueta, distancia y coordenadas) en una lista.
### Escritura de videos
Guarda los fotogramas procesados en las salidas previamente creadas.
### Visualizacion 
Muestra el fotograma cada dos segundos con las detecciones del objeto mas cercano en una ventana.
### Finalizacion del programa 
Se le pregunta al usuario si desea parar el bucle presionando la tecla 'q'. Si es asi entonces se termina el procesamiento, se liberan recursos y cierran todas las ventanas.
