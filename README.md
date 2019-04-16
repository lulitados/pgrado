# Detección de sujetos omitidos en el español

A continuación se incluyen las dependencias que son necesarias instalar. Las mismas se basan en la instalación de cero de un ambiente Linux.  

**Dependencias de sistema:**

```sudo apt install python-pip python3 python3-dev libboost-dev foma-bin foma libfoma-dev build-essential tial automake autoconf libtool git libboost-regex-dev libboost-program-options libboost-program-options-dev libboost-system-dev libboost-thread-dev```

  

**Instalación de Freeling**

Clonar el repositorio de freeling:

`git clone  [https://github.com/TALP-UPC/FreeLing.git](https://github.com/TALP-UPC/FreeLing.git)`

Se debe utilizar la branch `master`, pero una versión bastante mas vieja que la actual. Se supone que funciona con la version 4.0, pero por las dudas para estar seguros usar el commit:

`git checkout ff81c77efea3130d2b0a4dda603398da0c65dd96`

Para finalizar la instalación hay que seguir los  [pasos detallados acá](https://talp-upc.gitbooks.io/freeling-4-0-user-manual/content/installation.html#install-from-github-repositories) , que es básicamente correr los scripts de configuraciones y hacer el make.

 
 
**Entorno de desarrollo**

Para simplificar la instalación de dependencias utilizar un [entorno virtual de Python](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation). Es importante que el entorno se cree con Python3 para que los módulos puedan correr.

`mkvirtualenv pgrado --python=/usr/bin/python3.5`

Una vez dentro del entorno creado instalar las dependencias incluidas en el archivo  **requirements.txt**  adjunto.

`pip install -r requirements.txt`

Se utilizó una versión especifica de sckit-learn por lo que se debe instalar corriendo:
`pip install git+git://[github.com/scikit-learn/scikit-learn.git@0679bbc3fe6685fddedb5e673a9469caf951d36a](http://github.com/scikit-learn/scikit-learn.git@0679bbc3fe6685fddedb5e673a9469caf951d36a)`

 
Finalmente, es necesario declarar la ubicación de la API Python del modulo Free-Ling. El mismo se encuentra en la ruta `APIs/python` relativa al directorio donde se clonó el repositorio de la herramienta. Para esto se utilizan la variable de ambiente `FREELING API`, declarada de la siguiente manera:
`export FREELING API=/home/usuario/FreeLing/APIs/python`



**Utilización del modulo**

Para ejecutar el programa, con el entorno virtual activado y desde la carpeta raiz del modulo ejecutar:

`python pgrado.py`

Una vez dentro del programa se presenta un texto de ayuda y se habilita el input del usuario. El comando principal es  **`clasificar`**. Una vez ingresado ese comando, sin argumentos, se habilita el input para ingresar texto a clasificar. El mismo conviene copiarlo directamente, ya que la interfaz no permite navegar con el cursor hacia atrás. Para comenzar con la clasificación luego de ingresar el texto es necesario agregar  **una nueva línea con el caracter `#` y enter**. Esto le indica el final del input al programa. Luego, se imprime el listado de clausulas extraídas con el verbo principal identificado y la predicción del clasificador seleccionado.

Es posible cambiar el clasificador a utilizar con el comando  **`clasificador <nombre_clasificador>`**  donde `<nombre_clasificador>` es uno de los ofrecidos en la lista que se muestra al inicial el programa o al utilizar el comando  **`help`**.