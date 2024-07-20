# Ddosia-watcher

Esta carpeta contiene la aplicación de seguimiento del grupo NoName057(16). La configuración consta de dos máquinas separadas: una ejecutando DDoSia y la otra funcionando como gateway con ProtonVPN. La aplicación incluye una interfaz web y una API para visualizar los objetivos extraídos.

## Descripción general

El sistema se compone de dos máquinas:

1. **Máquina de DDoSia**: Ejecuta DDoSia en Windows 10, extrae los objetivos del grupo y los sirve mediante una API.
2. **Ubuntu Gateway**: Actúa como gateway para la máquina de Windows, utilizando ProtonVPN para salir a internet y reglas de iptables para gestionar el tráfico. También hospeda la aplicación React y la API para visualizar los objetivos.

## Configuración

### Máquina de DDoSia (Windows 10)

1. **Instalar y configurar DDoSia**:
    - Registrar el `client_id` y obtener el cliente de DDoSia.
    - Crear un script para extraer los objetivos utilizando `ddosia-targets`.

2. **Configurar tareas de Windows**:
    - Crear una tarea programada que ejecute el script de extracción de objetivos.
    - Configurar un servicio para servir los objetivos mediante una API.

3. **Red privada**:
    - Configurar la interfaz de red para conectarse únicamente a la red privada con la máquina Ubuntu Gateway.
    - Configurar la máquina Ubuntu como gateway predeterminado.

### Ubuntu Gateway

1. **Configurar ProtonVPN**:
    - Instalar y configurar ProtonVPN.
    - Crear reglas de iptables para permitir el tráfico a través de la interfaz de túnel de ProtonVPN.

2. **Montar la aplicación de React y la API**:
    - Clonar el repositorio y navegar a la carpeta `ddosia-watcher`.
    - Instalar las dependencias necesarias:
      ```bash
      npm install
      ```
    - Iniciar la aplicación:
      ```bash
      npm start
      ```

3. **Configurar la API para servir los objetivos**:
    - Crear una API en Ubuntu Gateway que consuma los datos de la API de la máquina de Windows y los sirva a la interfaz web.

## Uso

1. **Iniciar el sistema**:
    - Asegurarse de que la máquina de Windows esté ejecutando DDoSia y el script de extracción de objetivos.
    - Verificar que ProtonVPN esté activo y las reglas de iptables estén configuradas en la máquina Ubuntu.

2. **Visualizar los objetivos**:
    - Acceder a la interfaz web en la máquina Ubuntu a través del navegador:
      ```sh
      http://IPGATEWAY:3000
      ```
    - La interfaz mostrará los objetivos extraídos por DDoSia en tiempo real.

## Demo

