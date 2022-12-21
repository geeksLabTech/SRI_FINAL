# Informe Proyecto Final Sistemas de Recuperación de Información

- [Informe Proyecto Final Sistemas de Recuperación de Información](#informe-proyecto-final-sistemas-de-recuperación-de-información)
  - [Integrantes:](#integrantes)
  - [Pasos para ejecutar:](#pasos-para-ejecutar)
  - [Modelos Implementados](#modelos-implementados)
    - [Modelo Booleano](#modelo-booleano)
    - [Modelo Fuzzy](#modelo-fuzzy)
    - [Modelo Vectorial](#modelo-vectorial)
    - [Modelo de semantica latente](#modelo-de-semantica-latente)
  - [Errores y Recomendaciones](#errores-y-recomendaciones)


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

- Se implementó de forma tal que también puede ser utilizado como biblioteca separada y con total soporte a los corpus disponibles en ir_datasets, además de poder cargar corpus desde una dirección en el almacenamiento, solo se debe garantizar que se encuentre en archivos de texto plano.

## Modelos Implementados
Los modelos se manejan desde la clase InformationRetrievalSystem en system.py, esta posee la funcionalidad de cargar los corpus de ir_dataset o desde una ruta especificada, la cual esta implementada en la clase CorpusLoader en corpus_loader.py. Al cargar un corpus se construye el diccionario vocabulary_dict que tiene como llaves todas las palabras del corpus y como valores diccionarios q tienen como llaves los id de los documentos donde aparece la palabra y como valor la frecuencia con que aparece en ese documento. Tambien se construye el diccionario documents que tiene como llaves los id de los documentos del corpus y como valor una Clase DocumentData que tiene informacion util de cada documento como la cantidad de veces que esta la palabra que mas se repite o el total de pabalabras.
Todos los modelos implementados utilizan estos dicciionarios para realizar sus operaciones.
Cuenta ademas con la funcionalidad de testear todas las queries de un dataset de ir_datasets mostrando las medidas de evaluacion por cada query.
Las medidas de evaluacion implementadas pueden encontrarse en evaluation_measures.py

### Modelo Booleano
Este modelo fue seleccionado para filtrar un corpus de datasets de kaggle (particularmente datasets relacionados con el fútbol) y se utilizó como una herramienta que puede ayudar a determinar cuales datasets pueden contener información relevante (por ejemplo se desean encontrar los datasets que tienen información de Messi con la selección Argentina la consulta sería: Messi & Argentina). Está orientado a un usuario especializado que sabe exactamente qué busca, por esto se consideró que es el mejor modelo para esto.
### Modelo Fuzzy
Este modelo tiene un funcionamiento simular al fuzzy en cuanto a la manera de leer la query y leer los documentos, difieren en primera instancia en cuanto a implementación en la manera de procesar la query ya que el fuzzy, necesita la misma en forma normal diyuntiva completa, una vez que tenemos de la manera correcta para este modelo, se debe analizar el conjunto de documentos para determinar que nivel de relevaancia. Para esta tarea se siguieron los siguientes pasos:
- Se calculo el grado de pertenencia de cada documento del corpus al conjunto difuso de cada término de la consulta utilizando la siguiente fórmula:  
  $F(d,t)=tf×idf$, donde tf = the number of occurrences of query term t in d/the number of all words in d e 
  idf = log(the total number of documents in the retrieved set / the number of documents indexed by query term t+1)  
   La ecuación anterior es obtenida del siguiente paper Fuzzy Information Retrieval Based on Continuous Bag-of-Words Model, que se puede encontrar en este link https://www.mdpi.com/2073-8994/12/2/225/htm
- Luego se calcula la relevancia del documento,utilizando la siguiente fórmula:   
     $r = 1 - \prod 1 - cc_{ij}$, donde $cc_{ij}$  es la relevancia del documento i con respecto al término j  
   Esta fórmula fue obtenida del seminario Modelo de Recuperación de información Fuzzy de Andy Rosquet y Relando Sanchéz  curso 2021-2022   
El escenario para el cual fue diseñado este modelo fue el siguiente: Para investigadores, cuando van a iniciar un proyecto, necesitan hacer una búsqueda del estado del arte, donde necesitan tener coicidencias parciales para saber las diferentes ramas donde se esta usando la técnica, precedimiento o concépto que esta investigando.
### Modelo Vectorial
Para el calculo del idf se utilizo la formula $idf = log [ (1 + N) / (1 + n) ] + 1$ que es un poco diferente a la formula clasica, la explicacion de por que se escogio esta forma se encuentra en
la [documentacion de sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer).

### Modelo de semantica latente
La clase SliModel donde se implementa el modelo de semantica latente hereda de VectorialModel para reutilizar las funciones de crear la matriz de terminos y documentos, se utilizan las formulas presentadas en el seminario de Niley Gonzales y Arian Pazo 2022 pero como matriz A para descomponer se escoge la representacion de $tf*idf$ en vez de simplemente la matriz de frecuencias

## Errores y Recomendaciones
Probar otros datasets aparte de Cranfield para evaluar la efectivad y eficiencia de los modelos con consultas diferentes y muchos mas documentos

Probar como se afectan las medidas de evaluacion en los modelos al eliminar ciertos tipos de palabras de los documentos

Probar otros tipos de tokenizadores como el de spacy y ver cual da mejor resultado

Se recomienda añadir soporte a archivos que no estén en texto plano: PDF, Word entre otros.


