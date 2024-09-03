# CC4303 Redes: Tarea 1
# Andrés Gallardo Cornejo

## 1. Presentación

En esta tarea se implementan tres servidores en python que son capaces de recibir peticiones HTTP y responderlas. Los servidores soportan SÓLO el método GET. Para la implementación se utilizó la librería `socket` de python.
Un servidor principal recibe las consultas de cualquier red social y se comunica con los servidores secundarios para obtener la información. Los servidores secundarios son especializados en cada red social y devuelven la información solicitada al servidor principal.
Como optimización, los 3 servidores cuentan con un caché de las últimas 10 consultas.

En el archivo `.env` se deben definir las variables de entorno que utilizará cada servidor (host, puerto, etc) y el path hacia el archivo que contiene los datos. Se provee un archivo `/data/data.csv` con datos de ejemplo. Se deben inicializar MANUALMENTE los 3 servidores antes de realizar consultas, para ello se provee un archivo `main.py` que ayuda con la inicialización.

## 2. Requerimientos

La tarea fue programada con Python 3.12 y sólo utiliza una librería externa: `python-dotenv`. Para su correcto funcionamiento se debe tener un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```
HTTP_HOST
HTTP_PORT
INSTAGRAM_HOST
INSTAGRAM_PORT
WHATSAPP_HOST
WHATSAPP_PORT
DATA_PATH
```

El archivo con los datos puede estar ubicado en cualquier directorio, pero se debe especificar la ruta completa en la variable `DATA_PATH`.

## 3. Ejecución

Para ejecutar la tarea, se deben seguir los siguientes pasos:

### 3.1 Clonar o descargar el proyecto
#### 3.1.1 Clonar el proyecto desde GitHub
```bash
git clone github.com/AsessionGuy/CC4303-Tarea1.git
cd CC4303-Tarea1
```

#### 3.1.2 Descargar el proyecto
Es importante ejecutar los siguientes comandos en la raíz del proyecto.

### 3.2 Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Instalar dependencias

```bash
pip install python-dotenv
```

### 3.4 Inicializar servidores

#### 3.4.1 Opcional: 

Ejecutar el archivo `main.py` para asistr en la incialización de los servidores:
```bash
python main.py
```

#### 3.4.2 Escencial:
En una terminal, ejecutar el siguiente comando:
```bash
python HttpServer.py
```

En otra terminal, ejecutar el siguiente comando:
```bash
python InstagramServer.py
```

En otra terminal, ejecutar el siguiente comando:
```bash
python WhatsappServer.py
```

Si se ejectuó el archivo `main.py`, se mostrará un mensaje indicando que los servidores están listos para recibir consultas.

