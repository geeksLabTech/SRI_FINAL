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
### Modelo Fuzzy
Este modelo tiene un funcionamiento simular al fuzzy en cuanto a la manera de leer la query y leer los documentos, difieren en primera instancia en cuanto a implementación en la manera de procesar la query ya que el fuzzy, necesita la misma en forma normal diyuntiva completa, una vez que tenemos de la manera correcta para este modelo, se debe analizar el conjunto de documentos para determinar que nivel de relevaancia. Para esta tarea se siguieron los siguientes pasos:
- Se calculo el grado de pertenencia de cada documento del corpus al conjunto difuso de cada término de la consulta utilizando la siguiente fórmula:
  F(d,t)=tf×idf, donde tf = the number of occurrences of query term t in d/the number of all words in d y 
  idf = log(the total number of documents in the retrieved set / the number of documents indexed by query term t+1)
   La ecuación anterior es obtenida del siguiente paper Fuzzy Information Retrieval Based on Continuous Bag-of-Words Model, que se puede encontrar en este link https://www.mdpi.com/2073-8994/12/2/225/htm
- Luego se calcula la relevancia del documento,utilizando la siguiente fórmula: 
   $r = 1 - \multimap 1 - cc_ij$, donde $cc_ij$  es la relevancia del documento i con respecto al término j 
   Esta fórmula fue obtenida del seminario Modelo de Recuperación de información Fuzzy de Andy Rosquet y Relando Sanchéz  curso 2021-2022 
El escenario para el cual fue diseñado este modelo fue el siguiente:
### Modelo Vectorial

## Errores y Recomendaciones
Se considera que los valores de precisión no son los más satifactorios, se recomienda 

Se recomienda añadir soporte a archivos que no estén en texto plano: PDF, Word entre otros.


