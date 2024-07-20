# Cazando al oso: Informe CTI sobre NoName057(16) | Material

<p align="center">
  <img src="https://github.com/user-attachments/assets/76dd9410-c1e8-4e59-b40a-d4455f07d02b" height=400px />
</p>
Este repositorio contiene todos los materiales utilizados para el Trabajo de Fin de Máster (TFM) sobre NoName057(16). Aquí encontrarás herramientas y estudios realizados como parte del análisis del grupo.

## Contenido del repositorio
```
├───data
├───versiones
├───ddosia-targets
├───ddosia-watcher
│ ├───interfaz(gateway)
│ │ ├───api
│ │ └───web
│ └───vm
├───Images
├───notebook
└───scripts
```

- **versiones**: Versiones del software de DDoSia 
- **data**: Carpeta con los datos recolectados y utilizados en el análisis.
- **ddosia-targets**: Carpeta con una guía para extraer objetivos del grupo NoName057(16).
- **ddosia-watcher**: Herramienta para visualizar los objetivos identificados.
  - **interfaz(gateway)**: Contiene los archivos relacionados con la interfaz de usuario.Ubicados en la maquina gateway
    - **api**: API para interactuar con los datos.
    - **web**: Archivos web para la visualización de datos.
  - **vm**: Archivos relacionados con la máquina virtual utilizada para sacar los objetivos.
- **Images**: Carpeta con imágenes utilizadas en el estudio y análisis.
- **notebook**: Notebooks de Jupyter con el análisis de datos.
- **scripts**: Carpeta con scripts utilizados para la recolección y análisis de datos.

## Descripción de las carpetas

### Data

Esta carpeta contiene los datos recolectados que se utilizaron para los análisis presentes en este repositorio.

### Ddosia-targets

En esta carpeta se encuentra una guía para extraer los objetivos del grupo NoName057(16) desde la memoria. Para más información, visita [la guía detallada](https://m3str3.vercel.app/posts/ddosia-targets-from-memory).

### Ddosia-watcher

Una herramienta para visualizar los objetivos identificados. Contiene:

- **Interfaz**: Archivos relacionados con la interfaz de usuario. Maquina que sirve de gateway para la VM y sirve simultaneamente los objetivos
  - **API**: Endpoint API para interactuar con los datos.
  - **Web**: Archivos necesarios para la visualización web de los datos.
- **VM**: Archivos relacionados con la configuración de la máquina virtual que saca los objetivos y los sirve a la otra maquina.

### Images

Esta carpeta contiene imágenes.

### Notebook

Notebooks de Jupyter con el análisis detallado de los datos recolectados.

### Scripts

Esta carpeta contiene scripts utilizados para la recolección y análisis de datos del grupo NoName057(16).

