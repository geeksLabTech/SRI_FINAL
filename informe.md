# Informe Proyecto Final Sistemas de Recuperación de Información

## Integrantes:
- Javier A. Oramas Lopez C312
- Lia Zerquera Ferrer C312
- Daniel A. Cardenas Cabrera C311

## Pasos para ejecutar:
* Si ocurre un error a la hora de ejecutar lo comandos, sustituir `pip` por `pip3` y `python` por `python3`
* Este proyecto fue desarrollado con python 3.9.7, versiones anteriores no se garantiza compatibilidad

`pip install -r requirements.txt`

`python webui.py`

- Abrir en navegador http://localhost:5000
Abrirá un navegador con una barra de búsqueda en la que se podrán introducir las querys.

Justo al lado se encuentra el botón buscar y un dropdown para seleccionar el modelo con que se desea ejecutar la query sobre el corpus

Los resultados serán mostrados en forma de tabla justo debajo de la barra de búsqueda

- El software está desarrollado sobre Flask, utilizando la biblioteca InformationRetrievalSystem que fue desarrollada para unificar los tres modelos implementados y funcionar de interface para utilizarlos

- Se imoplementó de forma tal que también puede ser utilizado como biblioteca separada y con total soporte a los corpus disponibles en ir_datasets, además de poder cargar corpus desde una dirección en el almacenamiento, solo se debe garantizar que se encuentre en archivos de texto plano.

## Modelos Implementados

### Modelo Booleano
Este modelo fue seleccionado para filtrar un corpus de datasets de kaggle (particularmente datasets relacionados con el fútbol) y se utilizó como una herramienta que puede ayudar a determinar cuales datasets pueden contener información relevante (por ejemplo se desean encontrar los datasets que tienen información de Messi con la selección Argentina la consulta sería: Messi & Argentina). Está orientado a un usuario especializado que sabe exactamente qué busca, por esto se consideró que es el mejor modelo para esto.

### Modelo Vectorial

### Modelo Fuzzy

## Errores y Recomendaciones
Se considera que los valores de precisión no son los más satifactorios, se recomienda 

Se recomienda añadir soporte a archivos que no estén en texto plano: PDF, Word entre otros.


