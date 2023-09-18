
# Proyecto La Caprichosa: Análisis y Predicción de Resultados Futbolísticos
Este README proporciona una visión general de la metodología del proyecto. Para obtener una comprensión más técnica de los archivos y códigos, diríjase a este [enlace](https://github.com/Aalg26/la_caprichosa/blob/master/documentacion.txt).

## Objetivo
El objetivo principal de este proyecto es analizar los resultados históricos de cada equipo de fútbol y determinar qué aspectos son más relevantes para definir quién se lleva la victoria en un partido.

## Equipos Estudiados
Inicialmente, nos centraremos en la inclusión de equipos que compiten en las cinco principales ligas actuales, abarcando tanto la primera como la segunda división. Esto nos llevará a analizar un estimado de alrededor de 200 equipos en total.

### Definición de Equipos de Primera y Segunda División para el Proyecto
- **Primera División**: En esta categoría incluiremos a los equipos que han mantenido su presencia en la primera división de su país en los últimos años.

- **Segunda División**: Los equipos que consideraremos como pertenecientes a la segunda división son aquellos que han experimentado ascensos o descensos entre la primera y la segunda división durante los últimos 5 años. No tendremos en cuenta el tiempo que un equipo haya pasado en divisiones inferiores a estas dos mencionadas.

## Alcance Temporal de los Datos Utilizados
El alcance de los datos varía según la división a la que pertenezca el equipo:

- Primera División: En este caso, se estudiará el rendimiento del equipo en las últimas 5 temporadas.

- Segunda División: Para los equipos de segunda división, se analizará su rendimiento en las últimas 3 temporadas.

Este enfoque en el alcance temporal nos permite realizar un análisis más detallado y específico de acuerdo con la división a la que pertenece cada equipo, considerando su trayectoria reciente.

## Características Consideradas de los Equipos
La pregunta central que buscaba abordar en las etapas iniciales de este proyecto era la siguiente: ¿Qué información es esencial para evaluar el rendimiento de un equipo de fútbol? Más allá de la audiencia, la calidad de local o visitante, la formación, el entrenador o el nombre del equipo, nos dimos cuenta de que las estadísticas de los jugadores a nivel individual desempeñaban un papel fundamental. Para obtener una comprensión más precisa del rendimiento de un equipo en una temporada dada, calculamos las estadísticas del equipo como promedios basados en las contribuciones individuales de cada jugador durante esa temporada. Esto incluyó métricas como la cantidad de disparos por cada 90 minutos y los duelos aéreos ganados, entre otras.

## Origen de la Información sobre los Jugadores
Los datos son obtenidos a través de la plataforma [Fbref](https://fbref.com/).

## Estadísticas Individuales Utilizadas para el Análisis
En nuestra búsqueda de datos precisos y relevantes, aprovechamos la plataforma Fbref, la cual nos ofrece un valioso recurso: el [informe de reclutamiento](https://fbref.com/es/jugadores/1f44ac21/Erling-Haaland) de cada jugador. Este informe resume las características fundamentales de un jugador según su posición, proporcionándonos información clave para nuestro análisis.

## Elección de Estadísticas Relevantes
En este proyecto, adoptamos una estrategia que prioriza la precisión y la relevancia de los datos. En lugar de abrumarnos con una gran cantidad de datos desde el principio, hemos optado por una estrategia más selectiva. La razón detrás de esta decisión es la importancia de identificar las variables o estadísticas verdaderamente relevantes para nuestro análisis. Comprender qué datos son esenciales para evaluar el rendimiento de un equipo de fútbol es fundamental para lograr resultados significativos. Al comenzar con un conjunto de datos más limitado y enfocarnos en identificar las métricas más influyentes, podemos garantizar que nuestras conclusiones y predicciones estén respaldadas por información de calidad. Este enfoque nos permite minimizar el ruido y centrarnos en las variables que realmente importan. A medida que avancemos en el proyecto y acumulemos experiencia, evaluaremos constantemente la relevancia de los datos y ajustaremos nuestro enfoque según sea necesario. Esto nos permitirá construir un modelo sólido y efectivo basado en datos cuidadosamente seleccionados y análisis respaldados por evidencia sólida.

## Consideración de Factores Externos en el Análisis
En nuestro análisis, hemos tenido en cuenta varios factores externos que pueden influir en el rendimiento de un equipo de fútbol. Algunos de estos factores incluyen:

- Cantidad de jugadores útiles en la plantilla.
- Número de competiciones en las que el equipo participó durante esa temporada.
- Cantidad de audiencia que asistió al partido.
- Franja horaria en la cual se jugó el partido.
- Calidad de local o visitante.

Estos factores adicionales son cruciales para comprender completamente el contexto en el que se desarrollan los partidos y permiten una evaluación más precisa del rendimiento de los equipos.

## Obtención de Datos desde la Plataforma Fbref
Para obtener los datos de Fbref, utilizamos estas bibliotecas en conjunto:
- ![Requests](https://img.shields.io/badge/Requests-Library-blue) **Requests**: Esta biblioteca se utiliza para realizar solicitudes web y acceder a la información disponible en Fbref.
- ![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-Library-green) **Beautiful Soup**: La empleamos para analizar y extraer los datos relevantes de las páginas web obtenidas a través de las solicitudes.
- ![Pandas](https://img.shields.io/badge/Pandas-Library-orange) **Pandas**: Nos ayuda a estructurar y manejar las tablas de datos recopiladas durante el proceso de extracción.

## Modelo de Aprendizaje Utilizado: XGBoost
En este proyecto, hemos seleccionado el modelo de aprendizaje XGBoost, que significa "Extreme Gradient Boosting", como nuestra elección principal para abordar el análisis y predicción de resultados futbolísticos. A continuación, explico algunas de mis razones para elegirlo:

1. Capacidad para Manejar Datos Complejos:
El mundo del fútbol es intrincado y diverso, con una gran cantidad de variables que pueden influir en el resultado de un partido. XGBoost es capaz de manejar datos complejos y relaciones no lineales entre características, lo que lo convierte en una opción sólida para este proyecto.

2. Excelente Rendimiento en Problemas de Clasificación:
Este modelo ha demostrado un rendimiento excepcional en problemas de clasificación, como predecir si un equipo ganará o perderá un partido. Esto es fundamental para nuestro objetivo de analizar y prever los resultados de partidos de fútbol.

3. Robustez Frente a Datos Ruidosos:
En el análisis de datos deportivos, es común encontrar datos ruidosos o atípicos que pueden afectar la calidad de las predicciones. XGBoost es robusto y puede lidiar efectivamente con tales situaciones, lo que garantiza resultados confiables incluso en condiciones difíciles.

4. Interpretación de la Importancia de las Características:
XGBoost permite evaluar la importancia relativa de las características en nuestras predicciones. Esto es fundamental para identificar cuáles son los aspectos más influyentes en la determinación de quién se lleva la victoria en un partido de fútbol.

5. Ajuste Fino de Hiperparámetros:
XGBoost ofrece una amplia gama de hiperparámetros que pueden ajustarse para adaptarse a las necesidades específicas de nuestro proyecto. Esto nos permite optimizar el modelo y obtener el mejor rendimiento posible.

En resumen, XGBoost se destaca como una elección natural para este proyecto debido a su capacidad para manejar datos complejos, su rendimiento en problemas de clasificación, su robustez y su capacidad de interpretación de características. Estamos seguros de que este modelo nos ayudará a alcanzar nuestros objetivos de análisis y predicción de resultados futbolísticos con precisión y confiabilidad.

## Como puedo acceder a las predicciones:
Puedes acceder a las predicciones una vez que estén disponibles a través de una API que proporcionará acceso a los resultados del proyecto. Sin embargo, ten en cuenta que en este momento, el proyecto se encuentra en una etapa de desarrollo y la API aún no está disponible. Para estar al tanto de cuándo se lanzará la API y se pondrán a disposición las predicciones, te recomendamos estar atento a las actualizaciones del proyecto y seguir las instrucciones proporcionadas en el README o la documentación del proyecto para acceder a la API cuando esté lista.

## Contribución
¡Agradecemos tu interés en contribuir a este proyecto! Aquí hay algunas formas en las que puedes ayudar:

- Informar errores o problemas abriendo un [issue](https://github.com/Aalg26/la_caprichosa/issues).
- Proponer mejoras a través de solicitudes de extracción (pull requests).
- Compartir tus ideas y sugerencias en la sección de [discusiones](https://github.com/Aalg26/la_caprichosa/discussions).

### Cómo Contribuir

1. Clona el repositorio en tu máquina local.
2. Crea una rama (branch) para tu contribución: `git checkout -b tu-rama`.
3. Realiza tus cambios y asegúrate de seguir las convenciones de estilo y las pautas de contribución.
4. Hacer commit de tus cambios: `git commit -m "Descripción de tus cambios"`.
5. Sube tus cambios a tu repositorio remoto: `git push origin tu-rama`.
6. Abre una solicitud de extracción (pull request) describiendo tus cambios y por qué deben ser incluidos.
7. Espera comentarios y revisión de tu solicitud antes de que se fusione.

Recuerda ser respetuoso con los demás colaboradores y mantener un ambiente colaborativo y amigable. ¡Esperamos tus contribuciones!

## Contáctame
Puedes contactar conmigo a través de mi [LinkedIn](https://www.linkedin.com/in/adriánleóngracia) o escribir a este correo adrian2012011@gmail.com.










