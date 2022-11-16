# Proyecto Final de Sistemas de Recuperación de Información

## Integrantes:
- Javier A. Oramas Lopez C312
- Lia Zerquera Ferrer C312
- Daniel A. Cardenas Cabrera C311

## Escenario 1: Buscador de datasets de Kaggle con info sobre un jugador de Fútbol o un equipo de fútbol
### Modelo a utilizar: Modelo Booleano Clásico

En este escenario se desea recopilar todos los documentos que tengan información acerca de un jugador de fútbol especificando nombre y apellidos, además de esto es posible querer recopilar solo los documentos que tengan datos del jugador con su selección, o no recopilar los que incluyan un club de fútbol que se desee ignorar

En este caso se decidió utilizar el modelo booleano ya que se desean todos los documentos que puedan aportar información acerca del jugador, como en este escenario todos los documentos son datasets de kaggle, sabemos que si aparece el término el documento será relevante (en principio)

Un ejemplo de consulta que se pudiera desear realizar sería obtener todos los documentos que contengan información de messi con datos de argentina

~~~bash
>>> messi & (arg | argentina)
['2021-2022 Football Player Stats.csv', 'Final-player.txt', 'FullData (1).csv', 'FullData.csv', 'players_15.csv', 'players_16.csv', 'players_17.csv', 'players_18.csv', 'players_19.csv', 'players_20.csv']
~~~

### Ejecucion:
Para la Ejecucion del modelo se debe contar con python 3.9, e instalar los paquetes designados en requirements.txt

~~~bash
pip install -r requirements.txt
~~~

Luego ejecutar main.py
~~~bash
python main.py
~~~

Nota: si los comandos anteriores dan error sustituir pip por pip3 y python por python3 respectivamente
El proyecto ha sido probado en archlinux con python 3.9.7
