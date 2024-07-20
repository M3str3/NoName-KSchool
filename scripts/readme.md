# TgCrawler
# Descripción
TgCrawler es un script en Python diseñado para descargar mensajes de un canal de Telegram especificado y almacenarlos en una base de datos SQLite. Este script permite la recuperación y análisis fácil de los mensajes del canal, usuarios e interacciones.

## Características
- Obtiene y almacena información del canal, incluyendo el ID del canal, nombre de usuario, título y estado de difusión.
- Descarga y guarda mensajes, usuarios e interacciones del canal de Telegram especificado.
- Maneja los límites de tasa de manera eficiente utilizando la excepción FloodWaitError.
## Requisitos
- Python 3.6+
- Telethon
## Instalación
Instala las bibliotecas de Python requeridas usando pip:

1. `pip install telethon`
2. Clona o descarga el script en tu máquina local.

## Uso
Obtén las credenciales de la API de Telegram:

Visita my.telegram.org para crear una nueva aplicación y obtener tu api_id y api_hash.

Ejecuta el script:

```
python tgcrawler.py -c @nombre_canal --database tu_base_de_datos.db
```
Reemplaza @nombre_canal con el nombre de usuario real del canal de Telegram que deseas rastrear.
El argumento --database es opcional. Si no se proporciona, el nombre predeterminado de la base de datos será telegram.db.

## Archivo de Configuración:

La primera vez que ejecutes el script, se te pedirá el api_id y api_hash. Estos se almacenarán en un archivo llamado tgcrawler.json para su uso futuro.