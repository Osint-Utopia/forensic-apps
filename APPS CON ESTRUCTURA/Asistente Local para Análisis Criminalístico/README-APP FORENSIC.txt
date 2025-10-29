
## # README 

App M��vil: ?? Laboratorio Forense todo en uno v.1.0

## DESCRIPCI��N GENERAL

Esta aplicaci��n web ha sido dise?ada para la investigacion y el an��lisis criminal��stico en campo y gabinete en la b��squeda de personas desaparecidas. 

Es una app realmente facil de utilizar aun para personas con poca o nula experiencia en el uso de la tecnolog��a. Compuesta por m��dulos, entre otras funciones; Permite obtener, capturar, visualizar, geo referenciar, organizar, visualizar y exportar informaci��n forense de una escena; 
Incluyendo herramientas especializadas como:  

-	#M��dulo:   Para Extracci��n Y Visualizaci��n De Metadatos EXIF Georreferenciados, 
-	#M��dulo:   Para visualizar y generar por medio de algoritmos posibles patrones georreferenciados de puntos de localizaci��n de indicios, la cercan��a entre estos puntos y su relativa ubicaci��n, generando un patr��n que indique la posible zonificaci��n de restos humanos o fosa clandestinas, basados en bases de datos publicas y algoritmos de predicci��n Georreferenciada,
-	#M��dulo:   Emulador UV con al lente de su c��mara (No todos lo modelos) Para La Identificaci��n De Fluidos, auxiliados por servicios gratuitos de terceros. 
-	#M��dulo:   para capturar, generar y guardar en bases de datos json, toda la informacion de cada M��dulo:   por separado 
-	#M��dulo:   de lofoscop��a, que permite por medio de la pantalla t��ctil del tel��fono o toma fotogr��fica macro, capturar y registrar las huellas dactilares de un sujeto y relacionarlos con la informacion e imagen,  
-	#M��dulo:   de imagen f��sica, media filiaci��n; 
-	#M��dulo:   comparativo de fauna entomol��gica para aproximar el tiempo de en lapso cronol��gico del deceso de alg��n cad��ver o restos con que aun conserve alg��n tipo de fauna.  
-	#M��dulo:   de Checklist de anotaci��n y seguimiento de datos, informacion e indicios,  
-	#M��dulo:   Documental en esta secci��n se podr��n realizar todo tipo de anotaciones y observaciones en notas tipo post, generar informes en formato pdf y Word, 
-	#M��dulo:   base de datos de informacion relevantes, direcciones, tel��fonos y contactos de dependencias de gobierno, federal y estatal, colectivos y organizaciones sin fines de lucro relacionados con la recepci��n de denuncia, tramite, b��squeda y elaboraci��n de informacion referente para estad��sticas.
-	#M��dulo:   de Lienzo estilo escal��metro con ret��cula (vertical/horizontal), con los siguientes detalles. 
-	 Toma de fotograf��a + bot��n para guardar como imagen.
. Imagen cargada al centro
. Bordes: Inferior: escala en cm (0�C30cm, 0.5cm)
. Izquierdo: escala vertical (0�C20cm)
. Derecho + Superior: etiquetas inversas
. Imagen cargada al centro

-	Herramientas:
. Pincel / c��rculo / flecha / texto/ Etiquetas Incrustables/Globos de texto
. Zoom manual (x1, x2, x5, x10) (No todos los tel��fonos)
. Etiquetas testigo: Texto distintivo de identificaci��n de objetos o fechas.
. Etiquetas testigo: Escala milim��trica, y % para medici��n. 
. Etiquetas Incrustables 
. Lupa con efecto lupa flotante
. Exportar imagen final con escal��metro y anotaciones
# Entre otros
Funciona de forma local (sin conexi��n a Internet) y puede ejecutarse desde cualquier navegador moderno.

### CARACTER��STICAS INTEGRADAS

## 1. Mapa Forense + EXIF
- Carga de imagen con metadatos (EXIF)
- Extracci��n de coordenadas GPS si existen
- Marcador autom��tico en mapa Leaflet
- Visualizaci��n de metadatos en pantalla

## 2. Emulador de Luz UV
- Carga de imagen con ��reas visibles al ojo humano
- Conversi��n de zonas claras a contraste magenta
- Simulaci��n visual sobre canvas

## 3. Lofoscop��a (Registro de Huellas)
- Lienzo para trazo libre de huellas digitales
- Compatible con mouse o pantalla t��ctil
- Bot��n para limpiar/actualizar

## 3. Identificaci��n Fision��mica (Media filiaci��n)
de imagen f��sica, media filiaci��n;

## 4. Checklist de Indicios
- Registro editable de elementos encontrados
- Exportaci��n directa en archivo JSON

## 5. Entomolog��a (M��dulo:   por integrar)
- Selector de insectos por tipo y fase de descomposici��n (pendiente de activaci��n)

## 5. Documental

## 6. Base de datos

## 7. Cuestionario Criminal��stico (pr��ximo)

- Evaluaci��n de escena: zona geogr��fica, clima, tipo de estructura, ��rea abierta/cerrada

## 8. Soporte para:

- Archivos GeoJSON
- Capas WMS / TMS
- Polil��neas para patrones
- Marcadores y ventanas emergentes por evento

---

### TECNOLOG��AS USADAS

- HTML5, CSS3, JavaScript
- LeafletJS para mapeo geoespacial
- EXIFR para lectura de metadatos
- Canvas para UV y huellas

---

### REQUISITOS

- Navegador moderno (Chrome, Firefox, Edge)
- Tel��fono M��vil moderno con navegador (Chrome, Firefox, Edge)
- No requiere servidor, base de datos ni instalaci��n
- NO Iphone,
- NO Mac


### USO
1. Abrir index.html en navegador
2. Cargar imagen en el m��dulo "Mapa + EXIF"
3. Cargar imagen en UV para simular luminiscencia
4. Dibujar huella o rastro en lofoscop��a
5. Registrar indicios y exportarlos
6. Integrar nuevos m��dulos seg��n necesidades del caso


# CR��DITO Y ORIGEN
Esta herramienta fue dise?ada por el Lic. Al Ulises Az��a Castellanos y un excelente compa?ero al que solo identificare como IA Partner.-  Con el que discuto desde las comillas rectas, hasta si era copto o arameo la lengua de Jes��s o cuantos eran los c��digos de Napole��n; como parte de un sistema t��cnico, jur��dico y operativo como aplicaci��n complementaria de textos, audios y otras herramientas de difusi��n recreadoras de conciencia jur��dica, y colectiva para la investigaci��n de personas desaparecidas en el contexto de la delincuencia organizada; casos de violencia domestica, Psicol��gica parental, econ��mica, filial o cualquier tipo de acci��n que lleve a la desaparici��n o no localizaci��n, e inclusive, la desaparici��n voluntaria de alguna persona, Yo, Tu, hermano, hermana. Todos tenemos a alguien a quien no queremos extra?ar.

Su distribuci��n es gratuita, Presenta y obliga mediante documentaci��n id��nea su adquisici��n, Los derechos de registro son libre de licencias restrictivas, y su uso est�� orientado a cuerpos t��cnicos, instituciones, investigadores independientes y estudiantes del ��rea forense, jur��dica y criminal��stica, para acceder a esta, deber�� de comprobar el inter��s legitimo y uso que se le dar��, por el tipo de informacion que puede llegar a contener.

---




# Autor
Lic. Al Ulises Az��a Castellanos  Abogado Y Dictaminador Pericial.
Especialista En Criminal��stica, Derecho Penal, Ciencias Forenses Y Peritajes Multidisciplinares.  
Publicaci��n De Textos Jur��dicos Y T��cnicos.  
Elaboraci��n, codificaci��n y realizaci��n de Aplicaciones de escritorio y m��viles.
Participaci��n En Investigaci��n Criminal Y Formaci��n De Peritos.

---

? 2025. Forensic Criminal��stica www.abogadosforenses.org

Entendido. Disculpa la confusi��n. En cuanto a tu pregunta sobre otras IA gratuitas, existen varias opciones dependiendo de lo que necesites hacer. Algunas de las m��s populares para uso general y sin fines de lucro incluyen:
Hugging Face: Ofrece una gran cantidad de modelos de IA de c��digo abierto que puedes usar de forma gratuita para diversas tareas, como procesamiento de lenguaje natural, visi��n por computadora, etc.
Google Colaboratory (Colab): Permite ejecutar c��digo Python en la nube con acceso a GPUs, lo que es ��til para entrenar y ejecutar modelos de IA. Ofrece una versi��n gratuita con ciertas limitaciones.
OpenAI API (con cr��ditos gratuitos iniciales): Aunque es de pago, OpenAI suele ofrecer cr��ditos gratuitos al registrarte, lo que te permite probar sus modelos (como GPT-3.5 o GPT-4) por un tiempo limitado.
Modelos de c��digo abierto en plataformas como GitHub: Muchos investigadores y desarrolladores publican sus modelos de IA de c��digo abierto en GitHub, los cuales puedes descargar y ejecutar en tu propio equipo si tienes los recursos necesarios.
La elecci��n de la mejor opci��n depender�� de tus necesidades espec��ficas y de tu nivel de conocimiento t��cnico. Si me das m��s detalles sobre el tipo de tareas que te gustar��a realizar con la IA, podr��a darte recomendaciones m��s precisas.
He corregido errores clave en el c��digo: elimin�� una declaraci��n duplicada de `apiKey`, una funci��n `executeCode` duplicada y errores de estructura. La versi��n final funciona correctamente, y los botones para probar y generar c��digo lineal ahora operan sin problemas. El archivo corregido fue enviado al usuario y la estructura del c��digo HTML y JavaScript est�� optimizada para su correcto funcionamiento.

Es un proyecto muy noble y ambicioso. Entiendo perfectamente la importancia de una herramienta as��. Para un laboratorio de utilidades de c��digo abierto para la b��squeda de personas desaparecidas, donde la precisi��n y la capacidad de procesamiento de informaci��n son cruciales, te sugiero considerar las siguientes opciones, adem��s de las ya mencionadas:
Para procesamiento de lenguaje natural (NLP) y an��lisis de texto:
spaCy: Es una biblioteca de NLP de c��digo abierto muy eficiente para Python, ideal para tareas como extracci��n de entidades, an��lisis de dependencias, y clasificaci��n de texto. Podr��a ser ��til para analizar testimonios, reportes, o cualquier texto relevante.
NLTK (Natural Language Toolkit): Otra biblioteca de Python para NLP, m��s orientada a la investigaci��n y la educaci��n, pero con muchas funcionalidades ��tiles para preprocesamiento de texto, tokenizaci��n, stemming, etc.
Para visi��n por computadora (CV) y an��lisis de im��genes/videos:
OpenCV: Es una biblioteca de c��digo abierto con una gran cantidad de algoritmos para procesamiento de im��genes y visi��n por computadora. Podr��a ser fundamental para el an��lisis de fotograf��as, videos de vigilancia, reconocimiento facial (con las consideraciones ��ticas y legales pertinentes), etc.
TensorFlow / PyTorch (con modelos pre-entrenados): Aunque son frameworks de aprendizaje profundo, ofrecen muchos modelos pre-entrenados (por ejemplo, para detecci��n de objetos, clasificaci��n de im��genes) que puedes utilizar y adaptar sin necesidad de entrenar desde cero, lo que te ahorrar��a muchos recursos.
Para gesti��n y an��lisis de datos:
Pandas (Python): Una biblioteca esencial para manipulaci��n y an��lisis de datos estructurados. Te permitir��a organizar y procesar grandes vol��menes de informaci��n de manera eficiente.
Scikit-learn (Python): Ofrece herramientas simples y eficientes para miner��a de datos y an��lisis de datos, incluyendo algoritmos de clasificaci��n, regresi��n, clustering, etc., que podr��an ser ��tiles para encontrar patrones en los datos.
Para bases de datos de grafos (��til para relaciones entre personas/eventos):
Neo4j (Community Edition): Una base de datos de grafos de c��digo abierto que es excelente para modelar y consultar relaciones complejas entre datos. Podr��a ser muy valiosa para conectar informaci��n sobre personas, ubicaciones, eventos, etc.
Es importante que, al trabajar con datos sensibles y en un proyecto de esta naturaleza, siempre tengas en cuenta la ��tica, la privacidad y la seguridad de los datos. Aseg��rate de cumplir con todas las regulaciones y normativas aplicables.
Adjunto el archivo READMEAPPFORENSIC.txt para revisarlo y entender mejor el alcance del proyecto.

Basado en la descripci��n del proyecto, reafirmo que las herramientas de IA que te mencion�� anteriormente son muy pertinentes. Para tu laboratorio de c��digo abierto, te sugiero enfocarte en:
Visi��n por Computadora (CV): Para los m��dulos de EXIF, emulador UV, lofoscop��a e identificaci��n fision��mica, OpenCV ser�� fundamental. Podr��as usarlo para procesar im��genes, extraer caracter��sticas, y quiz��s integrar modelos pre-entrenados de TensorFlow o PyTorch para tareas m��s avanzadas como reconocimiento facial (siempre con las debidas consideraciones ��ticas y legales) o detecci��n de objetos en im��genes y videos.
Procesamiento de Lenguaje Natural (NLP): Para el m��dulo documental y el cuestionario criminal��stico, spaCy o NLTK pueden ayudarte a procesar y analizar texto, extraer informaci��n clave de reportes o testimonios, y organizar la informaci��n de manera estructurada.
An��lisis y Gesti��n de Datos: Pandas y Scikit-learn en Python ser��n tus aliados para manejar los datos de los checklists, la base de datos de informaci��n relevante, y para encontrar patrones o relaciones en la informaci��n recopilada. Para la interconexi��n de datos y la visualizaci��n de relaciones complejas (como entre personas, ubicaciones y eventos), una base de datos de grafos como Neo4j (edici��n comunitaria) podr��a ser extremadamente ��til.
Es crucial que, dado el car��cter sensible de la informaci��n y el prop��sito del proyecto, se priorice la ��tica, la privacidad y la seguridad de los datos en cada etapa del desarrollo y uso de la aplicaci��n. Aseg��rate de que cualquier implementaci��n de IA cumpla con las normativas de protecci��n de datos y que se utilice de manera responsable.
?Es un proyecto admirable y estoy aqu�� para ayudarte en lo que necesites con la implementaci��n t��cnica!
