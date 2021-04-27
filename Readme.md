

# Billing API

## Instalación

- Crear [ambiente virtual](https://docs.python.org/es/3/tutorial/venv.html) en python con el comando

    `python -m virtualenv venv`

- Activar ambiente virtual con el siguiente comando:

    - Si es linux:
    `source venv/bin/activate`

    - Si es windows:
    `.\venv\Scripts\activate.bat`

    Deberá aprecer un (venv) en la consola. Siempre que se ejecute una nueva consola se deberá seguir el procedimiento, la maquina virtual tiene librerías y dependencias diferentes a las que se encuentran en el entorno normal de windows, esto para mantener la integridad de las aplicaciones en el sistema operativo.

- Instalar las dependencias

`python -m pip install -r requirements.txt`

- Relizar migracíón de base de datos

`python migrate.py`

## Ejecución

- Con la maquina virtual activada, ejecutar el siguiente comando en consola:

`uvicorn app:app --reload --port 5000`

## Azure

Lo que viene a continuación es para realizar el despliegue en Docker de la imagen en la nube manualmente ( Por favor, no tocar )

#### Build

docker build . -t zapacommerce.azurecr.io/zapacommerce-build

#### Push

docker push zapacommerce.azurecr.io/zapacommerce-build