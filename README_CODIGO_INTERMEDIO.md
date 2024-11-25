## Objetivo
Optimizar el calculo de distancias de los objetos rojos que entran en el umbral en funcion de su ancho, empleando una proporcion arbitraria obtenida por tanteo.
## Librerias utilizadas 
Python 3.12, Numpy y OpenCV2
## Flujo de trabajo para el codigo intermedio
### Configuracion de la camara y los intervalos de color
Se establecen los intervalos de deteccion permitidos que en este caso son para los del color rojo y tambien verifica si la camara se abrio correctamente. Si no, aparece un mensaje de error y se termina el programa.
### Verificacion de lectura del fotograma
Se comprueba si se esta leyendo un fotograma debido a la camara. Si no se lee ningun fotograma entonces aparecera un mensaje de error y se termina el programa.
### Conversion de codificacion de color
Se convierte el fotograma BGR a HSV.
### Creacion de mascara
Genera una mascara binaria donde los pixeles que son permitidos por el umbral son blancos (valor 255) y los que no son negros (valor 0).
### Deteccion de contornos 
Se hace la deteccion de los contornos debido a las regiones blancas del proceso anterior.
### Filtrado de contornos
Itera sobre cada uno de los contornos detectados para posteriormente filtrar aquellos que poseen un area menor a los 500 pixeles para evitar ruido.
### Rectangulo delimitador y centro del anillo
Se dibuja un rectangulo alrededor del contorno y se calcula las coordenadas del centro del rectangulo y se muestra como un punto.
### Calculo de las distancias
Se calcula la distancia aproximada como una relacion inversa con el ancho del rectangulo (distancia= 100/w). Se utiliza el valor 100 ya que es un factor arbitrario para pruebas preeliminares.
### -Etiquetas visuales
Muestra el numero del anillo detectado con su respectiva distancia utilizando la funcion cv2.putText.
### -Finalizacion del programa
Muestra el fotograma procesado en una ventana y le pregunta al usuario si quiere salir del bucle presionando la letra 'q'. Si presiona esa tecla entonces se libera la camara y se cierran todas las ventanas.
