
## # README 

App M車vil: ?? Laboratorio Forense todo en uno v.1.0

## DESCRIPCI車N GENERAL

Esta aplicaci車n web ha sido dise?ada para la investigacion y el an芍lisis criminal赤stico en campo y gabinete en la b迆squeda de personas desaparecidas. 

Es una app realmente facil de utilizar aun para personas con poca o nula experiencia en el uso de la tecnolog赤a. Compuesta por m車dulos, entre otras funciones; Permite obtener, capturar, visualizar, geo referenciar, organizar, visualizar y exportar informaci車n forense de una escena; 
Incluyendo herramientas especializadas como:  

-	#M車dulo:   Para Extracci車n Y Visualizaci車n De Metadatos EXIF Georreferenciados, 
-	#M車dulo:   Para visualizar y generar por medio de algoritmos posibles patrones georreferenciados de puntos de localizaci車n de indicios, la cercan赤a entre estos puntos y su relativa ubicaci車n, generando un patr車n que indique la posible zonificaci車n de restos humanos o fosa clandestinas, basados en bases de datos publicas y algoritmos de predicci車n Georreferenciada,
-	#M車dulo:   Emulador UV con al lente de su c芍mara (No todos lo modelos) Para La Identificaci車n De Fluidos, auxiliados por servicios gratuitos de terceros. 
-	#M車dulo:   para capturar, generar y guardar en bases de datos json, toda la informacion de cada M車dulo:   por separado 
-	#M車dulo:   de lofoscop赤a, que permite por medio de la pantalla t芍ctil del tel谷fono o toma fotogr芍fica macro, capturar y registrar las huellas dactilares de un sujeto y relacionarlos con la informacion e imagen,  
-	#M車dulo:   de imagen f赤sica, media filiaci車n; 
-	#M車dulo:   comparativo de fauna entomol車gica para aproximar el tiempo de en lapso cronol車gico del deceso de alg迆n cad芍ver o restos con que aun conserve alg迆n tipo de fauna.  
-	#M車dulo:   de Checklist de anotaci車n y seguimiento de datos, informacion e indicios,  
-	#M車dulo:   Documental en esta secci車n se podr芍n realizar todo tipo de anotaciones y observaciones en notas tipo post, generar informes en formato pdf y Word, 
-	#M車dulo:   base de datos de informacion relevantes, direcciones, tel谷fonos y contactos de dependencias de gobierno, federal y estatal, colectivos y organizaciones sin fines de lucro relacionados con la recepci車n de denuncia, tramite, b迆squeda y elaboraci車n de informacion referente para estad赤sticas.
-	#M車dulo:   de Lienzo estilo escal赤metro con ret赤cula (vertical/horizontal), con los siguientes detalles. 
-	 Toma de fotograf赤a + bot車n para guardar como imagen.
. Imagen cargada al centro
. Bordes: Inferior: escala en cm (0每30cm, 0.5cm)
. Izquierdo: escala vertical (0每20cm)
. Derecho + Superior: etiquetas inversas
. Imagen cargada al centro

-	Herramientas:
. Pincel / c赤rculo / flecha / texto/ Etiquetas Incrustables/Globos de texto
. Zoom manual (x1, x2, x5, x10) (No todos los tel谷fonos)
. Etiquetas testigo: Texto distintivo de identificaci車n de objetos o fechas.
. Etiquetas testigo: Escala milim谷trica, y % para medici車n. 
. Etiquetas Incrustables 
. Lupa con efecto lupa flotante
. Exportar imagen final con escal赤metro y anotaciones
# Entre otros
Funciona de forma local (sin conexi車n a Internet) y puede ejecutarse desde cualquier navegador moderno.

### CARACTER赤STICAS INTEGRADAS

## 1. Mapa Forense + EXIF
- Carga de imagen con metadatos (EXIF)
- Extracci車n de coordenadas GPS si existen
- Marcador autom芍tico en mapa Leaflet
- Visualizaci車n de metadatos en pantalla

## 2. Emulador de Luz UV
- Carga de imagen con 芍reas visibles al ojo humano
- Conversi車n de zonas claras a contraste magenta
- Simulaci車n visual sobre canvas

## 3. Lofoscop赤a (Registro de Huellas)
- Lienzo para trazo libre de huellas digitales
- Compatible con mouse o pantalla t芍ctil
- Bot車n para limpiar/actualizar

## 3. Identificaci車n Fision車mica (Media filiaci車n)
de imagen f赤sica, media filiaci車n;

## 4. Checklist de Indicios
- Registro editable de elementos encontrados
- Exportaci車n directa en archivo JSON

## 5. Entomolog赤a (M車dulo:   por integrar)
- Selector de insectos por tipo y fase de descomposici車n (pendiente de activaci車n)

## 5. Documental

## 6. Base de datos

## 7. Cuestionario Criminal赤stico (pr車ximo)

- Evaluaci車n de escena: zona geogr芍fica, clima, tipo de estructura, 芍rea abierta/cerrada

## 8. Soporte para:

- Archivos GeoJSON
- Capas WMS / TMS
- Polil赤neas para patrones
- Marcadores y ventanas emergentes por evento

---

### TECNOLOG赤AS USADAS

- HTML5, CSS3, JavaScript
- LeafletJS para mapeo geoespacial
- EXIFR para lectura de metadatos
- Canvas para UV y huellas

---

### REQUISITOS

- Navegador moderno (Chrome, Firefox, Edge)
- Tel谷fono M車vil moderno con navegador (Chrome, Firefox, Edge)
- No requiere servidor, base de datos ni instalaci車n
- NO Iphone,
- NO Mac


### USO
1. Abrir index.html en navegador
2. Cargar imagen en el m車dulo "Mapa + EXIF"
3. Cargar imagen en UV para simular luminiscencia
4. Dibujar huella o rastro en lofoscop赤a
5. Registrar indicios y exportarlos
6. Integrar nuevos m車dulos seg迆n necesidades del caso


# CR谷DITO Y ORIGEN
Esta herramienta fue dise?ada por el Lic. Al Ulises Az迆a Castellanos y un excelente compa?ero al que solo identificare como IA Partner.-  Con el que discuto desde las comillas rectas, hasta si era copto o arameo la lengua de Jes迆s o cuantos eran los c車digos de Napole車n; como parte de un sistema t谷cnico, jur赤dico y operativo como aplicaci車n complementaria de textos, audios y otras herramientas de difusi車n recreadoras de conciencia jur赤dica, y colectiva para la investigaci車n de personas desaparecidas en el contexto de la delincuencia organizada; casos de violencia domestica, Psicol車gica parental, econ車mica, filial o cualquier tipo de acci車n que lleve a la desaparici車n o no localizaci車n, e inclusive, la desaparici車n voluntaria de alguna persona, Yo, Tu, hermano, hermana. Todos tenemos a alguien a quien no queremos extra?ar.

Su distribuci車n es gratuita, Presenta y obliga mediante documentaci車n id車nea su adquisici車n, Los derechos de registro son libre de licencias restrictivas, y su uso est芍 orientado a cuerpos t谷cnicos, instituciones, investigadores independientes y estudiantes del 芍rea forense, jur赤dica y criminal赤stica, para acceder a esta, deber芍 de comprobar el inter谷s legitimo y uso que se le dar芍, por el tipo de informacion que puede llegar a contener.

---




# Autor
Lic. Al Ulises Az迆a Castellanos  Abogado Y Dictaminador Pericial.
Especialista En Criminal赤stica, Derecho Penal, Ciencias Forenses Y Peritajes Multidisciplinares.  
Publicaci車n De Textos Jur赤dicos Y T谷cnicos.  
Elaboraci車n, codificaci車n y realizaci車n de Aplicaciones de escritorio y m車viles.
Participaci車n En Investigaci車n Criminal Y Formaci車n De Peritos.

---

? 2025. Forensic Criminal赤stica www.abogadosforenses.org

Entendido. Disculpa la confusi車n. En cuanto a tu pregunta sobre otras IA gratuitas, existen varias opciones dependiendo de lo que necesites hacer. Algunas de las m芍s populares para uso general y sin fines de lucro incluyen:
Hugging Face: Ofrece una gran cantidad de modelos de IA de c車digo abierto que puedes usar de forma gratuita para diversas tareas, como procesamiento de lenguaje natural, visi車n por computadora, etc.
Google Colaboratory (Colab): Permite ejecutar c車digo Python en la nube con acceso a GPUs, lo que es 迆til para entrenar y ejecutar modelos de IA. Ofrece una versi車n gratuita con ciertas limitaciones.
OpenAI API (con cr谷ditos gratuitos iniciales): Aunque es de pago, OpenAI suele ofrecer cr谷ditos gratuitos al registrarte, lo que te permite probar sus modelos (como GPT-3.5 o GPT-4) por un tiempo limitado.
Modelos de c車digo abierto en plataformas como GitHub: Muchos investigadores y desarrolladores publican sus modelos de IA de c車digo abierto en GitHub, los cuales puedes descargar y ejecutar en tu propio equipo si tienes los recursos necesarios.
La elecci車n de la mejor opci車n depender芍 de tus necesidades espec赤ficas y de tu nivel de conocimiento t谷cnico. Si me das m芍s detalles sobre el tipo de tareas que te gustar赤a realizar con la IA, podr赤a darte recomendaciones m芍s precisas.
He corregido errores clave en el c車digo: elimin谷 una declaraci車n duplicada de `apiKey`, una funci車n `executeCode` duplicada y errores de estructura. La versi車n final funciona correctamente, y los botones para probar y generar c車digo lineal ahora operan sin problemas. El archivo corregido fue enviado al usuario y la estructura del c車digo HTML y JavaScript est芍 optimizada para su correcto funcionamiento.

Es un proyecto muy noble y ambicioso. Entiendo perfectamente la importancia de una herramienta as赤. Para un laboratorio de utilidades de c車digo abierto para la b迆squeda de personas desaparecidas, donde la precisi車n y la capacidad de procesamiento de informaci車n son cruciales, te sugiero considerar las siguientes opciones, adem芍s de las ya mencionadas:
Para procesamiento de lenguaje natural (NLP) y an芍lisis de texto:
spaCy: Es una biblioteca de NLP de c車digo abierto muy eficiente para Python, ideal para tareas como extracci車n de entidades, an芍lisis de dependencias, y clasificaci車n de texto. Podr赤a ser 迆til para analizar testimonios, reportes, o cualquier texto relevante.
NLTK (Natural Language Toolkit): Otra biblioteca de Python para NLP, m芍s orientada a la investigaci車n y la educaci車n, pero con muchas funcionalidades 迆tiles para preprocesamiento de texto, tokenizaci車n, stemming, etc.
Para visi車n por computadora (CV) y an芍lisis de im芍genes/videos:
OpenCV: Es una biblioteca de c車digo abierto con una gran cantidad de algoritmos para procesamiento de im芍genes y visi車n por computadora. Podr赤a ser fundamental para el an芍lisis de fotograf赤as, videos de vigilancia, reconocimiento facial (con las consideraciones 谷ticas y legales pertinentes), etc.
TensorFlow / PyTorch (con modelos pre-entrenados): Aunque son frameworks de aprendizaje profundo, ofrecen muchos modelos pre-entrenados (por ejemplo, para detecci車n de objetos, clasificaci車n de im芍genes) que puedes utilizar y adaptar sin necesidad de entrenar desde cero, lo que te ahorrar赤a muchos recursos.
Para gesti車n y an芍lisis de datos:
Pandas (Python): Una biblioteca esencial para manipulaci車n y an芍lisis de datos estructurados. Te permitir赤a organizar y procesar grandes vol迆menes de informaci車n de manera eficiente.
Scikit-learn (Python): Ofrece herramientas simples y eficientes para miner赤a de datos y an芍lisis de datos, incluyendo algoritmos de clasificaci車n, regresi車n, clustering, etc., que podr赤an ser 迆tiles para encontrar patrones en los datos.
Para bases de datos de grafos (迆til para relaciones entre personas/eventos):
Neo4j (Community Edition): Una base de datos de grafos de c車digo abierto que es excelente para modelar y consultar relaciones complejas entre datos. Podr赤a ser muy valiosa para conectar informaci車n sobre personas, ubicaciones, eventos, etc.
Es importante que, al trabajar con datos sensibles y en un proyecto de esta naturaleza, siempre tengas en cuenta la 谷tica, la privacidad y la seguridad de los datos. Aseg迆rate de cumplir con todas las regulaciones y normativas aplicables.
Adjunto el archivo READMEAPPFORENSIC.txt para revisarlo y entender mejor el alcance del proyecto.

Basado en la descripci車n del proyecto, reafirmo que las herramientas de IA que te mencion谷 anteriormente son muy pertinentes. Para tu laboratorio de c車digo abierto, te sugiero enfocarte en:
Visi車n por Computadora (CV): Para los m車dulos de EXIF, emulador UV, lofoscop赤a e identificaci車n fision車mica, OpenCV ser芍 fundamental. Podr赤as usarlo para procesar im芍genes, extraer caracter赤sticas, y quiz芍s integrar modelos pre-entrenados de TensorFlow o PyTorch para tareas m芍s avanzadas como reconocimiento facial (siempre con las debidas consideraciones 谷ticas y legales) o detecci車n de objetos en im芍genes y videos.
Procesamiento de Lenguaje Natural (NLP): Para el m車dulo documental y el cuestionario criminal赤stico, spaCy o NLTK pueden ayudarte a procesar y analizar texto, extraer informaci車n clave de reportes o testimonios, y organizar la informaci車n de manera estructurada.
An芍lisis y Gesti車n de Datos: Pandas y Scikit-learn en Python ser芍n tus aliados para manejar los datos de los checklists, la base de datos de informaci車n relevante, y para encontrar patrones o relaciones en la informaci車n recopilada. Para la interconexi車n de datos y la visualizaci車n de relaciones complejas (como entre personas, ubicaciones y eventos), una base de datos de grafos como Neo4j (edici車n comunitaria) podr赤a ser extremadamente 迆til.
Es crucial que, dado el car芍cter sensible de la informaci車n y el prop車sito del proyecto, se priorice la 谷tica, la privacidad y la seguridad de los datos en cada etapa del desarrollo y uso de la aplicaci車n. Aseg迆rate de que cualquier implementaci車n de IA cumpla con las normativas de protecci車n de datos y que se utilice de manera responsable.
?Es un proyecto admirable y estoy aqu赤 para ayudarte en lo que necesites con la implementaci車n t谷cnica!
