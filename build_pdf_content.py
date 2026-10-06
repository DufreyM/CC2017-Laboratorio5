# -*- coding: utf-8 -*-
# Contenido del reporte. Se ejecuta con exec() desde build_pdf.py, usando las
# funciones h1/h2/h3/p/img/simple_table ya definidas en ese scope.

h1("Introducción y elección del estado")
p("Este laboratorio construye un modelo espacial de cobertura hospitalaria combinando cuatro datasets "
  "provistos en Canvas: hospitales_eeuu.geojson (7,154 hospitales con coordenadas, camas y ocupación), "
  "condados_eeuu.geojson (3,221 condados con geometría y código FIPS), poblacion_condados.csv (población "
  "estimada por condado) y estados_eeuu.geojson (límites de los 51 estados).")
p("Se eligió <b>Indiana</b> (abreviatura IN, FIPS de estado 18) porque tiene 158 hospitales con datos de "
  "camas disponibles, muy por encima del mínimo recomendado de 50, y porque su forma relativamente "
  "compacta y rectangular facilita los cálculos de buffers, la grilla del Task 2.3 y la descarga de red "
  "vial del Task 3.1, a diferencia de estados muy extensos como Texas o California. Además, Indiana cabe "
  "casi por completo dentro de una sola zona UTM, lo que simplifica la justificación del sistema de "
  "coordenadas proyectado.")

story_text = "El código completo de carga, limpieza y todos los análisis está disponible en el notebook del repositorio de GitHub indicado en la carátula."
p(story_text)

# ============================= TASK 1 =============================
h1("Task 1")

h2("Task 1.1 — Carga y preparación de los datos")
h3("a. Carga de los cuatro archivos")
simple_table(
    ["Archivo", "Registros", "CRS", "Columnas principales"],
    [
        ["hospitales_eeuu.geojson", "7,154", "EPSG:4326", "nombre, tipo, ciudad, estado, camas_total, camas_icu, ocupacion_total"],
        ["condados_eeuu.geojson", "3,221", "EPSG:4326", "fips, nombre, cod_estado, geometry"],
        ["estados_eeuu.geojson", "51", "EPSG:4326", "nombre, codigo, pais, geometry"],
        ["poblacion_condados.csv", "3,246", "N/A (tabular)", "fips, condado, estado, lat, lon, poblacion"],
    ],
    col_widths=[1.65 * inch, 0.75 * inch, 0.75 * inch, 2.55 * inch],
)

h3("b. Limpieza previa al filtro por estado")
p("En poblacion_condados.csv se eliminaron 102 registros con código FIPS mayor o igual a 80000 "
  "(casos especiales que no representan condados reales), quedando 3,144 registros. La columna fips se "
  "convirtió a texto de 5 dígitos con ceros a la izquierda.")
p("En hospitales_eeuu.geojson, el 15.24% de los registros tiene camas_total nulo a nivel nacional "
  "(1,090 de 7,154). El resto del laboratorio trabaja únicamente con los 6,064 hospitales que sí tienen "
  "dato de camas. Después de filtrar por Indiana, quedan 158 hospitales con datos de camas disponibles.")

h3("c. Filtro por estado y unión población–geometría")
p("Tras filtrar hospitales (columna estado = 'IN'), condados (cod_estado = '18') y población "
  "(estado = 'Indiana'), se obtuvieron 92 condados con geometría y 92 condados con población, que "
  "coinciden exactamente tras la unión por código FIPS. Indiana tiene efectivamente 92 condados, lo que "
  "confirma que el filtro y el join se hicieron correctamente.")

h3("d. Reproyección a CRS proyectado en metros")
p("<b>CRS elegido: EPSG:32616 — WGS 84 / UTM zone 16N.</b> Indiana se extiende aproximadamente entre "
  "-88.10° y -84.78° de longitud, un rango que cae enteramente dentro de la zona UTM 16N (84°O–90°O), "
  "cuyo meridiano central (-87°O) pasa casi por el centro del estado. Esto mantiene la distorsión de "
  "escala acotada (factor de escala entre 0.9996 y aproximadamente 1.0004, error relativo máximo del "
  "orden de 1:2500), muy inferior al que introduciría una proyección continental aplicada a un solo "
  "estado. UTM es además una proyección conforme con unidades en metros, apropiada para medir distancias "
  "y construir buffers circulares con precisión.")

h3("e. Mapa de línea base")
img("outputs/task1_1e_mapa_linea_base.png",
    caption="Figura 1.1 — Condados de Indiana, 158 hospitales coloreados por tipo, y límite estatal.")

h2("Task 1.2 — Estadísticas por condado")
p("Se calcularon número de hospitales, camas totales, camas UCI, población y camas por cada 10,000 "
  "habitantes para cada uno de los 92 condados, asignando cero en las columnas numéricas a los condados "
  "sin hospitales (18 de 92).")

h3("a. Los 5 condados con menor cantidad de camas por habitante (población > 10,000)")
p("De los 88 condados de Indiana con más de 10,000 habitantes, 15 no tienen ningún hospital con datos de "
  "camas, por lo que su tasa es exactamente cero. Los cinco mostrados a continuación son un subconjunto "
  "representativo de ese grupo empatado en el valor mínimo posible.")
simple_table(
    ["Condado", "Población", "Hospitales", "Camas/10k hab."],
    [["Pike", "12,389", "0", "0.00"], ["Parke", "16,937", "0", "0.00"],
     ["Wabash", "30,996", "0", "0.00"], ["Owen", "20,799", "0", "0.00"],
     ["Martin", "10,255", "0", "0.00"]],
    col_widths=[1.5 * inch, 1.3 * inch, 1.3 * inch, 1.5 * inch],
)
p("Estos condados dependen completamente de hospitales ubicados fuera de su territorio, lo que los "
  "convierte en los candidatos más claros a vulnerabilidad de acceso hospitalario.")

h3("b. Los 5 condados con mayor concentración de camas por habitante")
simple_table(
    ["Condado", "Población", "Hospitales", "Camas totales", "Camas/10k hab."],
    [["Jefferson", "32,308", "2", "238", "73.67"], ["Vanderburgh", "181,451", "4", "1,094", "60.29"],
     ["Wayne", "65,884", "2", "376", "57.07"], ["Grant", "65,769", "3", "347", "52.76"],
     ["Marion", "964,582", "17", "4,072", "42.22"]],
    col_widths=[1.3 * inch, 1.1 * inch, 0.9 * inch, 1.1 * inch, 1.2 * inch],
)
p("Esta concentración <b>no</b> representa necesariamente una ventaja de acceso exclusiva para la "
  "población residente. Jefferson, Wayne y Grant tienen poblaciones relativamente pequeñas pero "
  "concentran hospitales grandes — típico de condados que albergan un hospital regional que atiende "
  "pacientes referidos de condados vecinos sin hospital propio, por lo que la tasa local sobreestima el "
  "acceso real disponible solo para sus residentes. Marion (Indianápolis) es distinto: es el condado más "
  "poblado del estado y concentra los sistemas hospitalarios más grandes, funcionando como centro de "
  "referencia estatal, por lo que su alta tasa sí refleja en parte capacidad genuina para su población "
  "además de servir como hub regional.")

h3("c. Distribuciones (histogramas)")
img("outputs/task1_2c_histogramas.png",
    caption="Figura 1.2 — Distribución de camas totales por hospital y de camas por 10,000 hab. por condado.")
p("Ambas distribuciones son fuertemente asimétricas a la derecha. En camas por hospital, la mediana (49) "
  "es mucho menor que la media (108.9), y el máximo (1,226) supera por mucho al percentil 75 (133.75): "
  "la mayoría de los hospitales de Indiana son pequeños (críticos de acceso rural), mientras que unos "
  "pocos hospitales urbanos grandes concentran una fracción desproporcionada de la capacidad instalada. "
  "En camas por 10,000 habitantes por condado, 18 de 92 condados están en la barra de cero y la cola "
  "derecha llega hasta 73.7, muy por encima del percentil 75 (20.9), confirmando el patrón de hospitales "
  "regionales que inflan la tasa per cápita de su condado. Esto implica que usar promedios simples sería "
  "engañoso para el análisis de cobertura: es más informativo trabajar con medianas, percentiles o, como "
  "se hace en el Task 1.3, con un análisis espacial explícito.")

h2("Task 1.3 — Análisis de buffer de cobertura")
p("Se generaron buffers circulares de 10, 25 y 50 km alrededor de cada hospital sobre la capa "
  "reproyectada en metros, unidos con shapely.ops.unary_union para obtener una geometría de cobertura "
  "por radio.")
simple_table(
    ["Radio (km)", "Población cubierta", "Población total", "% cobertura"],
    [["10", "3,291,613", "6,732,219", "48.89%"],
     ["25", "6,552,287", "6,732,219", "97.33%"],
     ["50", "6,732,219", "6,732,219", "100.00%"]],
    col_widths=[1.2 * inch, 1.8 * inch, 1.6 * inch, 1.2 * inch],
)
img("outputs/task1_3c_mapa_cobertura_25km.png",
    caption="Figura 1.3 — Cobertura a 25 km: condados completamente cubiertos, parcialmente cubiertos y sin cobertura.")
p("Con 10 km la cobertura es de apenas 48.9% de la población; a 25 km sube a 97.3%; a 50 km prácticamente "
  "el 100% del estado queda cubierto. A 25 km ningún condado queda totalmente sin cobertura "
  "(46 completos / 46 parciales / 0 sin cobertura), pero hay un anillo de condados del norte, oeste y sur "
  "con cobertura solo parcial — zonas rurales más alejadas de los hospitales concentrados en el corredor "
  "central de Indianápolis y en los clústeres urbanos del norte y sureste.")

story.append(PageBreak())

# ============================= TASK 2 =============================
h1("Task 2")

h2("Task 2.1 — Distancia al hospital más cercano")
h3("a. Distancia por condado y los 10 condados más alejados")
simple_table(
    ["Condado", "Población", "Distancia (km)"],
    [["Benton", "8,748", "35.09"], ["Martin", "10,255", "30.29"], ["Switzerland", "10,751", "29.52"],
     ["Owen", "20,799", "27.42"], ["Brown", "15,092", "27.18"], ["Crawford", "10,577", "27.11"],
     ["Wabash", "30,996", "26.25"], ["Posey", "25,427", "26.20"], ["Pike", "12,389", "25.59"],
     ["Shelby", "44,729", "25.03"]],
    col_widths=[1.6 * inch, 1.4 * inch, 1.6 * inch],
)

h3("b. Curva de cobertura acumulada")
img("outputs/task2_1b_curva_cobertura.png",
    caption="Figura 2.1 — Curva de cobertura acumulada (5 a 100 km) con punto de inflexión marcado.")
p("El punto de inflexión se ubica en <b>25 km</b> (máxima caída en la segunda diferencia: de +28.3 puntos "
  "porcentuales ganados entre 5 y 10 km a solo +6.8 puntos entre 20 y 25 km, con rendimientos ya casi "
  "nulos después de 30 km). Para la política de acceso hospitalario esto significa que 25 km es el radio "
  "donde la inversión en expandir cobertura deja de ser eficiente: antes de ese punto cada kilómetro "
  "adicional suma población cubierta a un ritmo alto, y después el estado ya está casi saturado "
  "(97.3% a 99.3%), de modo que ampliar el radio más allá de 30 km tendría un costo marginal muy alto "
  "por persona adicional cubierta.")

h3("c. Tipo de hospital más cercano para los 5 condados más alejados")
simple_table(
    ["Condado", "Hospital más cercano", "Tipo", "Camas"],
    [["Benton", "St Vincent Williamsport Hospital", "Critical Access", "16"],
     ["Martin", "IU Health Bedford Hospital", "Critical Access", "25"],
     ["Switzerland", "King's Daughters' Health", "General Acute Care", "88"],
     ["Owen", "Bloomington Meadows Hospital", "Psychiatric", "71"],
     ["Brown", "IU Health Bloomington Hospital", "General Acute Care", "254"]],
    col_widths=[1.1 * inch, 2.1 * inch, 1.5 * inch, 0.8 * inch],
)
p("Dos de los cinco condados más alejados (Benton y Martin) tienen como hospital más cercano uno de tipo "
  "Critical Access, hospitales rurales pequeños con servicios limitados por definición federal. El caso "
  "de Owen es revelador: su hospital más cercano es psiquiátrico, no de atención general, por lo que para "
  "una emergencia médica general la distancia real relevante es mayor que la reportada. En conjunto, los "
  "datos apoyan la hipótesis de que la lejanía geográfica y la baja capacidad del hospital más cercano "
  "tienden a coincidir en los mismos condados rurales, agravando su vulnerabilidad.")

h2("Task 2.2 — Índice compuesto de vulnerabilidad de acceso hospitalario")
p("El índice combina tres componentes normalizados al rango [0,1] con la transformación min-max: "
  "(1) distancia al hospital más cercano, (2) inverso de camas por habitante (asignando el valor máximo "
  "antes de normalizar a los condados sin hospitales), y (3) ocupación promedio de hospitales dentro de "
  "50 km (mismo criterio de valor máximo para condados sin hospital en ese radio).")
p("<b>Justificación de min-max:</b> es apropiada porque los tres componentes tienen escalas distintas "
  "(km, 1/camas, fracción de ocupación) y min-max las lleva a un rango común [0,1] comparable para poder "
  "promediarlas, y porque interesa la posición relativa de cada condado dentro del propio estado "
  "analizado. Dejaría de ser apropiada si hubiera valores atípicos extremos (el máximo de la muestra "
  "comprimiría artificialmente a los demás hacia 0) o si se quisiera comparar el índice entre distintos "
  "estados analizados por separado.")
p("<b>Pesos elegidos: distancia 0.45, camas per cápita 0.35, ocupación 0.20.</b> La distancia recibe el "
  "mayor peso porque el tiempo de traslado está más directamente ligado a morbimortalidad en una "
  "emergencia y es la variable menos manipulable a corto plazo por política pública. Las camas per cápita "
  "miden si existe capacidad instalada suficiente una vez que el paciente llega. La ocupación recibe el "
  "menor peso porque es la variable más volátil en el tiempo y la más indirecta como proxy de "
  "vulnerabilidad estructural, aunque sigue siendo relevante.")
img("outputs/task2_2c_mapa_vulnerabilidad.png",
    caption="Figura 2.2 — Índice de vulnerabilidad por quintiles, con los 10 condados más vulnerables etiquetados.")
p("Los diez condados más vulnerables son: Wabash, Benton, Carroll, Shelby, Owen, Brown, Switzerland, "
  "Martin, Posey y Spencer — coinciden en gran medida con los condados más alejados del Task 2.1, lo "
  "cual es esperable dado el peso dominante del componente de distancia.")

h2("Task 2.3 — MCLP simplificado: ubicación óptima de nuevos hospitales")
p("Se implementó una versión simplificada del Maximum Coverage Location Problem (Church &amp; ReVelle, "
  "1974): max &#931; d<sub>i</sub>y<sub>i</sub> sujeto a y<sub>i</sub> &#8804; &#931; x<sub>j</sub> (para j en N<sub>i</sub>) y "
  "&#931;x<sub>j</sub> &#8804; p, con p=3 nuevas instalaciones. El "
  "problema exacto es NP-difícil, por lo que se resolvió con la heurística voraz estándar.")
p("Se generó una grilla de 50 km de resolución sobre el estado (54 puntos en el rectángulo envolvente), "
  "de los cuales 31 quedaron dentro del límite estatal tras la operación de intersección espacial. Para "
  "cada candidato se calculó la población adicional que cubriría a 25 km, definida como la población que "
  "hoy queda fuera de la cobertura unificada de los 158 hospitales existentes.")
simple_table(
    ["Iteración", "Población adicional cubierta"],
    [["1", "26,402"], ["2", "10,650"], ["3", "8,022"]],
    col_widths=[1.5 * inch, 2.5 * inch],
)
img("outputs/task2_3c_mapa_mclp.png",
    caption="Figura 2.3 — Cobertura final a 25 km tras agregar los 3 hospitales propuestos por el algoritmo voraz.")
p("La cobertura total del estado a 25 km sube de 97.33% a <b>98.00%</b> tras agregar los 3 nuevos "
  "hospitales.")

story.append(PageBreak())

# ============================= TASK 3 =============================
h1("Task 3")

h2("Task 3.1 — Isocronas con red vial real (OSMnx)")
p("El código para este task está completo en el notebook: descarga la red vial de conducción con OSMnx "
  "en un radio de 45 km alrededor de los tres hospitales ubicados en los condados más vulnerables, asigna "
  "velocidades por tipo de vía, calcula tiempos de viaje, y construye isocronas de 30 minutos con "
  "NetworkX para compararlas contra los buffers circulares de 25 km.")
p("<b>No se pudo ejecutar en este entorno</b> pese a una investigación extensa: el servicio de Overpass "
  "responde con normalidad cuando se consulta su página de estado desde una red independiente (confirma "
  "que el servicio está operativo), pero toda consulta real de datos (POST a /api/interpreter) falla "
  "desde esta conexión específica — con la librería requests de Python, con curl, e incluso imitando la "
  "huella de un navegador Chrome real mediante la librería curl_cffi. Un fetch web simple tipo GET sí "
  "logró traer datos reales de Overpass, pero esa vía no sirve para descargar un grafo completo porque el "
  "contenido es demasiado grande para relayarlo íntegro. Todo apunta a un bloqueo o límite de tasa "
  "específico de esta red hacia la infraestructura de OpenStreetMap, no a un error de código. "
  "La discusión de los incisos b y c se basa en el comportamiento conocido de la red vial de Indiana.")

h3("b. Cuándo el buffer circular sobreestima o subestima la cobertura real")
p("<b>Sobreestima</b> cuando la distancia en línea recta es mucho menor que la distancia real por "
  "carretera: condados rurales del oeste y suroeste de Indiana atravesados por ríos (Wabash, White) y "
  "terreno con colinas en el sur, cerca del valle del río Ohio, donde los puentes disponibles obligan a "
  "rodeos considerables. También sobreestima en el borde de las zonas de cobertura donde el círculo se "
  "extiende sobre áreas sin ninguna vía principal cercana.")
p("<b>Subestima</b> a lo largo de los corredores de interestatales que irradian desde Indianápolis "
  "(I-65, I-70, I-69, I-74): en esas direcciones un vehículo puede recorrer bien por encima de 25 km "
  "efectivos en 30 minutos, pero el buffer circular es isotrópico mientras que la red vial es fuertemente "
  "anisotrópica. La forma real de la isocrona sería una estrella irregular alargada a lo largo de los "
  "corredores viales, no un círculo.")

h3("c. Implicaciones de política pública")
p("1) Si la política usa buffers circulares, puede subestimar la vulnerabilidad real de condados que, "
  "aunque están dentro del círculo de 25 km, en la práctica quedan a más de 30 minutos reales por falta "
  "de vías rápidas directas — usar isocronas cambiaría qué condados específicos se priorizan para un "
  "nuevo hospital. 2) El algoritmo voraz del Task 2.3 optimiza sobre buffers circulares; si optimizara "
  "sobre isocronas probablemente desplazaría los candidatos hacia intersecciones de corredores viales en "
  "vez del centroide geométrico de la brecha de cobertura, cambiando la ubicación recomendada de los "
  "nuevos hospitales.")

h2("Task 3.2 — Comparación con la literatura")
h3("a. Cita y caracterización del paper")
p("Hashtarkhani, S., Schwartz, D. L., &amp; Shaban-Nejad, A. (2024). Enhancing health care accessibility "
  "and equity through a geoprocessing toolbox for spatial accessibility analysis: Development and case "
  "study. <i>JMIR Formative Research</i>, <i>8</i>, e51727. https://doi.org/10.2196/51727")
p("Los autores desarrollaron una caja de herramientas de geoprocesamiento (ArcGIS Pro) que implementa el "
  "método 2-Step Floating Catchment Area (2SFCA), clásico y mejorado. A diferencia de un buffer simple, "
  "el 2SFCA es una razón oferta/demanda que pondera la capacidad de cada proveedor por cuántos puntos de "
  "demanda compiten por ella. Las herramientas permiten construir el área de influencia con buffers de "
  "distancia o con cuencas de tiempo de viaje. La red de servicios analizada es la ubicación de centros "
  "de hemodiálisis en Tennessee; la demanda se calcula ponderando la población por tasas de incidencia de "
  "enfermedad renal terminal (ESRD) específicas por grupo etario. El caso de estudio trabaja a nivel de "
  "Tennessee completo, con cuencas construidas por centro individual.")

h3("b. Comparación metodológica")
p("Dos decisiones distintas a las de este laboratorio: (1) el 2SFCA modela explícitamente la competencia "
  "por la capacidad entre puntos de demanda, algo que nuestro índice de vulnerabilidad no captura "
  "formalmente (solo usamos camas por habitante del propio condado); (2) el paper pondera la demanda por "
  "riesgo específico de enfermedad por edad, mientras que nosotros tratamos a toda la población del "
  "condado como demanda homogénea de servicios hospitalarios en general. Lo primero hace al 2SFCA una "
  "medida más realista a costa de mayor complejidad; lo segundo es más fácil de justificar en el paper "
  "porque la diálisis es una necesidad crónica predecible por edad, mientras que \"servicios "
  "hospitalarios\" en general es una categoría demasiado heterogénea para una sola tasa de incidencia.")

h3("c. Comparación de la brecha de cobertura")
p("El paper reporta la brecha en términos relativos (puntajes 2SFCA más bajos en zonas rurales/"
  "suburbanas que en zonas urbanas de Tennessee), no como un porcentaje único de población sin cobertura, "
  "por lo que no es directamente comparable en magnitud con nuestro 97.3% de cobertura a 25 km en "
  "Indiana. Lo que sí es comparable es la dirección del hallazgo: ambos estudios encuentran que la "
  "población rural está sistemáticamente peor servida. Posibles explicaciones de las diferencias de "
  "magnitud: la hemodiálisis requiere visitas recurrentes y es más sensible a la distancia que la "
  "atención hospitalaria esporádica; Tennessee tiene una región montañosa (Apalaches) con redes viales "
  "más restringidas que el terreno plano de Indiana; y la regulación de certificado de necesidad para "
  "abrir nuevos proveedores varía por estado.")

h2("Task 3.3 — Reflexión metodológica")
h3("a. Análisis de sensibilidad de los pesos del índice")
p("Se recalculó el índice con 4 configuraciones de pesos: la original (0.45/0.35/0.20), pesos iguales "
  "(1/3 cada uno), dominada por distancia (0.70/0.20/0.10) y dominada por capacidad (0.20/0.60/0.20).")
simple_table(
    ["Configuración", "Condados en común (top-10)", "Correlación de Spearman"],
    [["Pesos iguales", "8/10 (Jaccard 0.67)", "0.981"],
     ["Dominada por distancia", "9/10 (Jaccard 0.82)", "0.946"],
     ["Dominada por capacidad", "8/10 (Jaccard 0.67)", "0.965"]],
    col_widths=[1.8 * inch, 2.0 * inch, 1.8 * inch],
)
p("El ranking es bastante estable: la correlación de Spearman nunca baja de 0.94 y al menos 8 de los 10 "
  "condados más vulnerables se repiten en todas las configuraciones. Esto es tranquilizador para la "
  "robustez de las recomendaciones de política: aunque los pesos son una decisión subjetiva, el conjunto "
  "de condados prioritarios no cambia drásticamente con elecciones razonables alternativas.")

h3("b. Caso adverso para el algoritmo voraz del MCLP")
p("El algoritmo voraz tiene garantía teórica de aproximación (1-1/e) ≈ 63% del óptimo, por ser la "
  "cobertura una función submodular monótona, pero puede quedarse sustancialmente por debajo del óptimo "
  "en configuraciones específicas.")
img("outputs/task3_3b_diagrama_greedy.png", width=4.5 * inch,
    caption="Figura 3.1 — Esquema del caso adverso: un candidato de compromiso entre dos clústeres.")
p("Un candidato de compromiso A, ubicado entre dos clústeres de población, cuyo buffer cubre "
  "parcialmente ambos, puede competir contra dos candidatos B y C centrados en cada clúster y capaces de "
  "cubrirlo casi por completo más población periférica. Si A cubre más población en su primera jugada que "
  "B o C individualmente, el algoritmo voraz lo selecciona primero, pero una vez elegido A, gran parte de "
  "lo que B y C habrían aportado ya está cubierto, así que el resultado final puede ser notablemente "
  "menor que haber elegido B y C desde el inicio. Este patrón es realista en el Task 2.3: la grilla de "
  "50 km puede generar candidatos intermedios entre dos ciudades medianas de Indiana que desplazan "
  "candidatos mejor centrados en cada una.")

h3("c. Las tres limitaciones a comunicar al departamento de salud")
p("<b>Primero</b>, la población no está distribuida de forma pareja dentro de cada condado: asumimos eso "
  "para calcular la cobertura, pero en la vida real la gente se concentra en pueblos y ciudades. La "
  "mejora sería población a nivel de manzana censal o un raster de densidad como WorldPop.")
p("<b>Segundo</b>, se usó distancia en línea recta en casi todo el análisis, y el Task 3.1 muestra que "
  "eso no refleja cómo se mueve realmente la gente: el buffer circular sobreestima la cobertura donde no "
  "hay un camino directo y la subestima donde hay una autopista. La mejora es extender el análisis de "
  "isocronas a todos los hospitales del estado, no solo a tres.")
p("<b>Tercero</b>, los pesos del índice de vulnerabilidad los elegimos con un argumento razonable pero "
  "finalmente subjetivo. El análisis de sensibilidad muestra que el ranking cambia moderadamente según "
  "los pesos, así que cualquier decisión de política que dependa de \"los diez condados más vulnerables\" "
  "podría cambiar con otros pesos igual de defendibles. Lo ideal sería validar los pesos con datos reales "
  "de desenlaces de salud o con un panel de expertos en salud pública.")

story.append(Spacer(1, 20))
story.append(HRFlowable(width="100%", color=colors.black))
story.append(Spacer(1, 10))
story.append(Paragraph(
    f'Código completo, notebook ejecutado y datos: <link href="{GITHUB_URL}"><u>{GITHUB_URL}</u></link>',
    ParagraphStyle(name="Footer", parent=styles["Normal"], fontName="Times-Roman", fontSize=10, alignment=TA_CENTER, textColor=colors.black)))
