# Proyecto Final de Sistemas de Recuperación de Información

## Escenario 1: Buscador de datasets de Kaggle con info sobre un jugador de Fútbol o un equipo de fútbol
### Modelo a utilizar: Modelo Booleano Clásico

En este escenario se desea recopilar todos los documentos que tengan información acerca de un jugador de fútbol especificando nombre y apellidos, además de esto es posible querer recopilar solo los documentos que tengan datos del jugador con su selección, o no recopilar los que incluyan un club de fútbol que se desee ignorar

En este caso se decidió utilizar el modelo booleano ya que se desean todos los documentos que puedan aportar información acerca del jugador, como en este escenario todos los documentos son datasets de kaggle, sabemos que si aparece el término el documento será relevante (en principio)

Un ejemplo de consulta que se pudiera desear realizar sería obtener todos los documentos que contengan información de messi con datos de argentina

~~~bash
>>> messi & (arg | argentina)
['2021-2022 Football Player Stats.csv', 'Final-player.txt', 'FullData (1).csv', 'FullData.csv', 'players_15.csv', 'players_16.csv', 'players_17.csv', 'players_18.csv', 'players_19.csv', 'players_20.csv']
~~~
