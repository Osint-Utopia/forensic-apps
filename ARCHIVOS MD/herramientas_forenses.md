# Impresionante Forense [![Link Status](https://github.com/cugu/awesome-forensics/workflows/CI/badge.svg)](https://github.com/cugu/awesome-forensics)

Lista curada de herramientas y recursos de análisis forense **gratuitos** (principalmente de código abierto) impresionantes.

- Impresionante Forense
- [Colecciones](#collections)
- [Herramientas](#tools)
- [Distribuciones](#distributions)
- [Frameworks](#frameworks)
- [Forense en Vivo](#live-forensics)
- [Escáner IOC](#ioc-scanner)
- [Adquisición](#acquisition)
- [Imagenología](#imaging)
- [Tallado](#carving)
- [Forense de Memoria](#memory-forensics)
- [Forense de Red](#network-forensics)
- [Artefactos de Windows](#windows-artifacts)
- [Procesamiento NTFS/MFT](#ntfsmft-processing)
- [Forense de OS X](#os-x-forensics)
- [Forense Móvil](#mobile-forensics)
- [Forense de Docker](#docker-forensics)
- [Artefactos de Internet](#internet-artifacts)
- [Análisis de Línea de Tiempo](#timeline-analysis)
- [Manejo de imágenes de disco](#disk-image-handling)
- [Desencriptación](#decryption)
- [Administración](#management)
- [Análisis de Imágenes](#picture-analysis)
- [Forense de Metadatos](#metadata-forensics)
- [Esteganografía](#steganography)
- [Aprender Forense](#learn-forensics)
- [CTFs y Desafíos](#ctfs-and-challenges)
- [Recursos](#resources)
- [Web](#web)
- [Blogs](#blogs)
- [Libros](#books)
- [Corpora de Sistemas de Archivos](#file-system-corpora)
- [Otros](#other)
- [Laboratorios](#labs)
- [Listas Impresionantes Relacionadas](#related-awesome-lists)
- [Contribuyendo](#contributing)

---

 Colecciones

- [AboutDFIR – El Proyecto Compendio Definitivo](https://aboutdfir.com) - Colección de recursos forenses para el aprendizaje y la investigación. Ofrece listas de certificaciones, libros, blogs, desafíos y más
- :star: [Repositorio de Artefactos de ForensicArtifacts.com](https://github.com/ForensicArtifacts/artifacts) - Base de conocimiento legible por máquina de artefactos forenses

 Herramientas

- [Herramientas forenses en Wikipedia](https://en.wikipedia.org/wiki/List_of_digital_forensics_tools)
- [Herramientas de Eric Zimmerman](https://ericzimmerman.github.io/#!index.md)

# Distribuciones

- [bitscout](https://github.com/vitaly-kamluk/bitscout) - LiveCD/LiveUSB para la adquisición y el análisis forense remoto
- [Remnux](https://remnux.org/) - Distribución para la ingeniería inversa y el análisis de software malicioso
- [SANS Investigative Forensics Toolkit (sift)](https://github.com/teamdfir/sift) - Distribución de Linux para el análisis forense
- [Tsurugi Linux](https://tsurugi-linux.org/) - Distribución de Linux para el análisis forense
- [WinFE](https://www.winfe.net/home) - Entorno forense de Windows

# Frameworks

- :star:[Autopsy](http://www.sleuthkit.org/autopsy/) - GUI para SleuthKit
- [dexter](https://github.com/coinbase/dexter) - Dexter es un framework de adquisición forense diseñado para ser extensible y seguro
- [dff](https://github.com/arxsys/dff) - Framework forense
- [Dissect](https://github.com/fox-it/dissect) - Dissect es un framework y conjunto de herramientas de respuesta a incidentes y análisis forense digital que permite acceder y analizar rápidamente artefactos forenses de varios formatos de disco y archivo, desarrollado por Fox-IT (parte de NCC Group).
- [hashlookup-forensic-analyser](https://github.com/hashlookup/hashlookup-forensic-analyser) - Una herramienta para analizar archivos de una adquisición forense para encontrar hashes conocidos/desconocidos desde la API de [hashlookup](https://www.circl.lu/services/hashlookup/) o usando un filtro Bloom local.
- [IntelMQ](https://github.com/certtools/intelmq) - IntelMQ recopila y procesa feeds de seguridad
- [Kuiper](https://github.com/DFIRKuiper/Kuiper) - Plataforma de Investigación Digital
- [Laika BOSS](https://github.com/lmco/laikaboss) - Laika es un escáner de objetos y sistema de detección de intrusiones
- [OpenRelik](https://openrelik.org/) - Plataforma forense para almacenar artefactos de archivos y ejecutar flujos de trabajo
- [PowerForensics](https://github.com/Invoke-IR/PowerForensics) - PowerForensics es un framework para el análisis forense de discos en vivo
- [TAPIR](https://github.com/tap-ir/tapir) - TAPIR (Analizador de artefactos confiables para respuesta a incidentes) es un framework de respuesta a incidentes multiusuario, cliente/servidor
- :star: [The Sleuth Kit](https://github.com/sleuthkit/sleuthkit) - Herramientas para el análisis forense de bajo nivel
- [turbinia](https://github.com/google/turbinia) - Turbinia es un framework de código abierto para implementar, administrar y ejecutar cargas de trabajo forenses en plataformas en la nube
- [IPED - Indexador e Processador de Evidências Digitais](https://github.com/sepinf-inc/IPED) - Herramienta de la Policía Federal Brasileña para Investigaciones Forenses
- [Wombat Forensics](https://github.com/pjrinaldi/wombatforensics) - Herramienta GUI forense

# Forense en Vivo

- [grr](https://github.com/google/grr) - GRR Respuesta Rápida: análisis forense remoto en vivo para respuesta a incidentes
- [Linux Expl0rer](https://github.com/intezer/linux-explorer) - Caja de herramientas forense en vivo fácil de usar para endpoints Linux escrita en Python & Flask
- [mig](https://github.com/mozilla/mig) - Análisis forense digital distribuido y en tiempo real a la velocidad de la nube
- [osquery](https://github.com/osquery/osquery) - Analítica del sistema operativo impulsada por SQL
- [POFR](https://github.com/gmagklaras/pofr) - The Penguin OS Flight Recorder recopila, almacena y organiza para su posterior análisis la ejecución de procesos, el acceso a archivos y los datos de endpoints de red/socket del sistema operativo Linux.
- [UAC](https://github.com/tclahr/uac) - UAC (Unix-like Artifacts Collector) es un script de recopilación de Respuesta en Vivo para Respuesta a Incidentes que utiliza binarios y herramientas nativas para automatizar la recopilación de artefactos de sistemas AIX, Android, ESXi, FreeBSD, Linux, macOS, NetBSD, NetScaler, OpenBSD y Solaris.

# Escáner IOC

- [Fastfinder](https://github.com/codeyourweb/fastfinder) - Buscador de archivos sospechosos multiplataforma rápido y personalizable. Admite hashes md5/sha1/sha256, cadenas literales/comodín, expresiones regulares y reglas YARA
- [Fenrir](https://github.com/Neo23x0/Fenrir) - Escáner IOC simple en Bash
- [Loki](https://github.com/Neo23x0/Loki) - Escáner simple de IOC y Respuesta a Incidentes
- [Redline](https://fireeye.market/apps/211364) - Herramienta de seguridad de endpoint gratuita de FireEye
- [THOR Lite](https://www.nextron-systems.com/thor-lite/) - Escáner gratuito de IOC y YARA
- [recon](https://github.com/rusty-ferris-club/recon) - Buscador de archivos orientado al rendimiento con soporte para consultas SQL, indexa y analiza metadatos de archivos con soporte para YARA.

# Adquisición

- [Acquire](https://github.com/fox-it/acquire) - Acquire es una herramienta para recolectar rápidamente artefactos forenses de imágenes de disco o un sistema en vivo en un contenedor ligero.
- [artifactcollector](https://github.com/forensicanalysis/artifactcollector) - Un agente personalizable para recolectar artefactos forenses en cualquier sistema Windows, macOS o Linux.
- [ArtifactExtractor](https://github.com/Silv3rHorn/ArtifactExtractor) - Extrae artefactos comunes de Windows desde imágenes fuente y VSCs.
- [AVML](https://github.com/microsoft/avml) - Una herramienta portátil de adquisición de memoria volátil para Linux.
- [Belkasoft RAM Capturer](https://belkasoft.com/ram-capturer) - Herramienta de Adquisición de Memoria Volátil.
- [DFIR ORC](https://dfir-orc.github.io/) - Herramienta de recolección de artefactos forenses para sistemas que ejecutan Microsoft Windows.
- [FastIR Collector](https://github.com/SekoiaLab/Fastir_Collector) - Recolecta artefactos en Windows.
- [FireEye Memoryze](https://fireeye.market/apps/211368) - Un software forense de memoria gratuito.
- [FIT](https://github.com/fit-project/fit) - Adquisición forense de páginas web, correos electrónicos, redes sociales, etc.
- [ForensicMiner](https://github.com/securityjoes/ForensicMiner) - Una herramienta de automatización DFIR basada en PowerShell, para la recopilación de artefactos y evidencia en máquinas Windows.
- [Fuji](https://github.com/Lazza/Fuji/) - Adquisición forense de MacOS simplificada. Crea copias completas del sistema de archivos o recopilación dirigida de computadoras Mac.
- [LiME](https://github.com/504ensicsLabs/LiME) - Módulo de Kernel Cargable (LKM), que permite la adquisición de memoria volátil desde Linux y dispositivos basados en Linux, anteriormente llamado DMD.
- [Magnet RAM Capture / DumpIt](https://www.magnetforensics.com/resources/magnet-dumpit-for-windows/) - Una herramienta de creación de imágenes gratuita diseñada para capturar la memoria física.
- [SPECTR3](https://github.com/alpine-sec/SPECTR3) - Adquiera, haga el triaje e investigue evidencia remota a través de acceso iSCSI portátil de solo lectura.
- [UFADE](https://github.com/prosch88/UFADE) - Extrae archivos de dispositivos iOS en Linux y MacOS. Principalmente un wrapper para pymobiledevice3. Crea copias de seguridad estilo iTunes y copias de seguridad lógicas avanzadas.
- [unix_collector](https://github.com/op7ic/unix_collector) - Un script de recolección forense en vivo para sistemas tipo UNIX como un único script.
- [Velociraptor](https://github.com/Velocidex/velociraptor) - Velociraptor es una herramienta para recolectar información de estado basada en el host utilizando consultas del Lenguaje de Consulta Velocidex (VQL).
- [WinTriage](https://www.securizame.com/wintriage-the-triage-tool-for-windows-dfirers/) - Wintriage es una herramienta de respuesta en vivo que extrae artefactos de Windows. Debe ejecutarse con privilegios de administrador local o de dominio y se recomienda hacerlo desde una unidad externa.

# Creación de Imágenes

- [dc3dd](https://sourceforge.net/projects/dc3dd/) - Versión mejorada de dd
- [dcfldd](https://sourceforge.net/projects/dcfldd/) - Diferente versión mejorada de dd (¡esta versión tiene algunos errores!, otra versión está en github [adulau/dcfldd](https://github.com/adulau/dcfldd))
- [FTK Imager](https://www.exterro.com/digital-forensics-software/ftk-imager) - Herramienta gratuita de creación de imágenes para Windows
- :star: [Guymager](https://sourceforge.net/projects/guymager/) - Versión de código abierto para la creación de imágenes de disco en sistemas Linux
- [4n6pi](https://github.com/plonxyz/4n6pi) - Creador de imágenes forenses de disco, diseñado para ejecutarse en una Raspberry Pi, impulsado por libewf

# Carving

- [bstrings](https://github.com/EricZimmerman/bstrings) - Utilidad de strings mejorada
- [bulk_extractor](https://github.com/simsong/bulk_extractor) - Extrae información como direcciones de correo electrónico, números de tarjetas de crédito e histogramas de imágenes de disco
- [floss](https://github.com/mandiant/flare-floss) - Herramienta de análisis estático para desofuscar automáticamente cadenas de binarios de malware
- :star: [photorec](https://www.cgsecurity.org/wiki/PhotoRec) - Herramienta de file carving
- [swap_digger](https://github.com/sevagas/swap_digger) - Un script bash utilizado para automatizar el análisis de swap de Linux, automatizando la extracción de swap y las búsquedas de credenciales de usuario de Linux, credenciales de formularios web, correos electrónicos de formularios web, etc.

# Análisis Forense de Memoria

- [inVtero.net](https://github.com/ShaneK2/inVtero.net) - Framework de análisis de memoria de alta velocidad desarrollado en .NET, compatible con todos los Windows x64, incluye integridad de código y soporte de escritura.
- [KeeFarce](https://github.com/denandz/KeeFarce) - Extrae contraseñas de KeePass de la memoria.
- [MemProcFS](https://github.com/ufrisk/MemProcFS) - Una forma fácil y conveniente de acceder a la memoria física como archivos, un sistema de archivos virtual.
- [Rekall](https://github.com/google/rekall) - Framework Forense de Memoria
- [volatility](https://github.com/volatilityfoundation/volatility) - El framework forense de memoria
- [VolUtility](https://github.com/kevthehermit/VolUtility) - Aplicación web para el framework Volatility

# Análisis Forense de Red

- [Kismet](https://github.com/kismetwireless/kismet) - Un sniffer inalámbrico pasivo
- [NetworkMiner](https://www.netresec.com/?page=Networkminer) - Herramienta de Análisis Forense de Red
- [Squey](https://squey.org) - Software de visualización de registros/PCAP diseñado para detectar anomalías y señales débiles en grandes cantidades de datos.
- :star: [WireShark](https://www.wireshark.org/) - Un analizador de protocolos de red

# Artefactos de Windows

- [Beagle](https://github.com/yampelo/beagle) - Transforma fuentes de datos y registros en gráficos
- [Blauhaunt](https://github.com/cgosec/Blauhaunt) - Una colección de herramientas para filtrar y visualizar eventos de inicio de sesión
- [FRED](https://www.pinguin.lu/fred) - Editor multiplataforma de hives del registro de Microsoft
- [Hayabusa](https://github.com/Yamato-Security/hayabusa) - Un generador de línea de tiempo forense rápido y de búsqueda de amenazas basado en sigma para los registros de eventos de Windows.
- [LastActivityView](https://www.nirsoft.net/utils/computer_activity_view.html) - LastActivityView de Nirsoft es una herramienta para el sistema operativo Windows que recopila información de varias fuentes en un sistema en ejecución y muestra un registro de las acciones realizadas por el usuario y los eventos ocurridos en esta computadora.
- [LogonTracer](https://github.com/JPCERTCC/LogonTracer) - Investiga inicios de sesión maliciosos de Windows visualizando y analizando el registro de eventos de Windows.
- [PyShadow](https://github.com/alicangnll/pyshadow) - Una biblioteca para Windows para leer copias sombra, eliminar copias sombra, crear enlaces simbólicos a copias sombra y crear copias sombra.
- [python-evt](https://github.com/williballenthin/python-evt) - Analizador Python puro para archivos de registro de eventos clásicos de Windows (.evt)
- [RegRipper3.0](https://github.com/keydet89/RegRipper3.0) - RegRipper es una herramienta Perl de código abierto para analizar el Registro y presentarlo para su análisis
- [RegRippy](https://github.com/airbus-cert/regrippy) - Un framework para leer y extraer datos forenses útiles de los hives del registro de Windows

 Procesamiento NTFS/MFT

- [MFT-Parsers](http://az4n6.blogspot.com/2015/09/whos-your-master-mft-parsers-reviewed.html) - Comparación de analizadores MFT
- [MFTEcmd](https://binaryforay.blogspot.com/2018/06/introducing-mftecmd.html) - Analizador MFT por Eric Zimmerman
- [MFTExtractor](ttps://github.com/aarsakian/FileSystemForensics) - Analizador MFT
- [MFTMactime](https://github.com/kero99/mftmactime) - Analizador de MFT y USN que permite la extracción directa en formato de línea de tiempo del sistema de archivos (mactime), volcar todos los archivos residentes en el MFT en su estructura de carpetas original y ejecutar reglas yara sobre todos ellos.
- [NTFS journal parser](http://strozfriedberg.github.io/ntfs-linker/)
- [NTFSTool](https://github.com/thewhiteninja/ntfstool) - Herramienta forense NTFS completa
- [NTFS USN Journal parser](https://github.com/PoorBillionaire/USN-Journal-Parser)
- [RecuperaBit](https://github.com/Lazza/RecuperaBit) - Reconstruye y recupera datos NTFS
- [python-ntfs](https://github.com/williballenthin/python-ntfs) - Análisis NTFS

# Análisis Forense de OS X

- [APFS Fuse](https://github.com/sgan81/apfs-fuse) - Un controlador FUSE de solo lectura para el nuevo sistema de archivos de Apple
- [mac_apt (macOS Artifact Parsing Tool)](https://github.com/ydkhatri/mac_apt) - Extrae artefactos forenses de imágenes de disco o máquinas en vivo
- [MacLocationsScraper](https://github.com/mac4n6/Mac-Locations-Scraper) - Vuelca el contenido de los archivos de la base de datos de ubicación en iOS y macOS
- [macMRUParser](https://github.com/mac4n6/macMRU-Parser) - Script de Python para analizar los archivos plist de los elementos más recientemente utilizados (MRU) en macOS en un formato más fácil de usar
- [OSXAuditor](https://github.com/jipegit/OSXAuditor)
- [OSX Collect](https://github.com/Yelp/osxcollector)

# Informática Forense Móvil

- [Andriller](https://github.com/den4uk/andriller) - Una utilidad de software con una colección de herramientas forenses para teléfonos inteligentes
- [ALEAPP](https://github.com/abrignoni/ALEAPP) - Un analizador de eventos y Protobuf de registros de Android
- [ArtEx](https://www.doubleblak.com/index.php) - Examinador de artefactos para extracciones completas del sistema de archivos de iOS
- [iLEAPP](https://github.com/abrignoni/iLEAPP) - Un analizador de registros, eventos y Plists de iOS
- [iOS Frequent Locations Dumper](https://github.com/mac4n6/iOS-Frequent-Locations-Dumper) - Volcar el contenido de los archivos StateModel#.archive ubicados en /private/var/mobile/Library/Caches/com.apple.routined/
- [MEAT](https://github.com/jfarley248/MEAT) - Realizar diferentes tipos de adquisiciones en dispositivos iOS
- [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) - Un marco automatizado todo en uno para pruebas de penetración, análisis de malware y evaluación de seguridad de aplicaciones móviles (Android/iOS/Windows) capaz de realizar análisis estáticos y dinámicos.
- [OpenBackupExtractor](https://github.com/vgmoose/OpenBackupExtractor) - Una aplicación para extraer datos de copias de seguridad de iPhone y iPad.

# Informática Forense de Docker

- [dof (Docker Forensics Toolkit)](https://github.com/docker-forensics-toolkit/toolkit) - Extrae e interpreta artefactos forenses de imágenes de disco de sistemas Docker Host
- [Docker Explorer](https://github.com/google/docker-explorer) Extrae e interpreta artefactos forenses de imágenes de disco de sistemas Docker Host

# Artefactos de Internet

- [ChromeCacheView](https://www.nirsoft.net/utils/chrome_cache_view.html) - Una pequeña utilidad que lee la carpeta de caché del navegador web Google Chrome y muestra la lista de todos los archivos almacenados actualmente en la caché.
- [chrome-url-dumper](https://github.com/eLoopWoo/chrome-url-dumper) - Volcar toda la información almacenada localmente recopilada por Chrome
- [hindsight](https://github.com/obsidianforensics/hindsight) - Informática forense del historial de Internet para Google Chrome/Chromium
- [IE10Analyzer](https://github.com/moaistory/IE10Analyzer) - Esta herramienta puede analizar registros normales y recuperar registros eliminados en WebCacheV01.dat.
- [unfurl](https://github.com/obsidianforensics/unfurl) - Extraer y visualizar datos de URLs
- [WinSearchDBAnalyzer](https://github.com/moaistory/WinSearchDBAnalyzer) - Esta herramienta puede analizar registros normales y recuperar registros eliminados en Windows.edb.

# Análisis de Línea de Tiempo

- [DFTimewolf](https://github.com/log2timeline/dftimewolf) - Marco para orquestar la recopilación forense, el procesamiento y la exportación de datos utilizando GRR y Rekall
- :star: [plaso](https://github.com/log2timeline/plaso) - Extraer marcas de tiempo de varios archivos y agregarlos
- [Timeline Explorer](https://binaryforay.blogspot.com/2017/04/introducing-timeline-explorer-v0400.html) - Herramienta de análisis de línea de tiempo para archivos CSV y Excel. Construido para estudiantes de SANS FOR508
- [timeliner](https://github.com/airbus-cert/timeliner) - Una reescritura de mactime, un lector de bodyfile
- [timesketch](https://github.com/google/timesketch) - Análisis colaborativo de líneas de tiempo forenses

# Manejo de imágenes de disco

- [Disk Arbitrator](https://github.com/aburgh/Disk-Arbitrator) - Una utilidad forense de Mac OS X diseñada para ayudar al usuario a garantizar que se sigan los procedimientos forenses correctos durante la creación de imágenes de un dispositivo de disco
- [imagemounter](https://github.com/ralphje/imagemounter) - Utilidad de línea de comandos y paquete de Python para facilitar el montaje (y desmontaje) de imágenes de disco forenses
- [libewf](https://github.com/libyal/libewf) - Libewf es una biblioteca y algunas herramientas para acceder al formato de compresión Expert Witness Compression Format (EWF, E01)
- [PancakeViewer](https://github.com/forensicmatt/PancakeViewer) - Visor de imágenes de disco basado en dfvfs, similar al visor FTK Imager
- [xmount](https://www.pinguin.lu/xmount) - Convertir entre diferentes formatos de imagen de disco

# Desencriptación

- [hashcat](https://hashcat.net/hashcat/) - Cracker de contraseñas rápido con soporte de GPU
- [John the Ripper](https://www.openwall.com/john/) - Cracker de contraseñas

# Gestión

- [Catalyst](https://github.com/SecurityBrewery/catalyst) - Catalyst es un sistema de automatización de seguridad y tickets de código abierto
- [dfirtrack](https://github.com/dfirtrack/dfirtrack) - Aplicación de seguimiento de respuesta a incidentes e informática forense digital, seguimiento de sistemas
- [Incidents](https://github.com/veeral-patel/incidents) - Aplicación web para organizar investigaciones de seguridad no triviales. Construido sobre la idea de que los incidentes son árboles de tickets, donde algunos tickets son pistas
- [iris](https://github.com/dfir-iris/iris-web) - Plataforma colaborativa de respuesta a incidentes

# Análisis de Imágenes

- [Ghiro](https://github.com/Ghirensics/ghiro) - Una herramienta totalmente automatizada diseñada para ejecutar análisis forenses sobre una gran cantidad de imágenes
- [sherloq](https://github.com/GuidoBartoli/sherloq) - Un conjunto de herramientas forenses de imágenes fotográficas digitales de código abierto
# Forense de Metadatos

- [ExifTool](https://exiftool.org/) por Phil Harvey
- [EXIF Editor](https://exifeditor.io/) En el navegador, herramienta de visor/editor/análisis EXIF con prioridad en la privacidad (sin necesidad de registrarse). Alberga The EXIF Guide y The EXIF Quiz.
- [FOCA](https://github.com/ElevenPaths/FOCA) - FOCA es una herramienta utilizada principalmente para encontrar metadatos e información oculta en los documentos

# Esteganografía

- [Sonicvisualizer](https://www.sonicvisualiser.org)
- [Steghide](https://github.com/StegHigh/steghide) - es un programa de esteganografía que oculta datos en varios tipos de archivos de imagen y audio
- [Wavsteg](https://github.com/samolds/wavsteg) - es un programa de esteganografía que oculta datos en varios tipos de archivos de imagen y audio
- [Zsteg](https://github.com/zed-0xff/zsteg) - Un codificador esteganográfico para archivos WAV

 Aprender Forense

- [Retos forenses](https://www.amanhardikar.com/mindmaps/ForensicChallenges.html) - Mapa mental de retos forenses
- [OpenLearn](https://www.open.edu/openlearn/science-maths-technology/digital-forensics/content-section-0?active-tab=description-tab) - Curso de informática forense digital

# CTFs y Retos

- [BelkaCTF](https://belkasoft.com/ctf) - CTFs por Belkasoft
- [CyberDefenders](https://cyberdefenders.org/blueteam-ctf-challenges/?type=ctf)
- [DefCon CTFs](https://archive.ooo) - archivo de retos DEF CON CTF.
- [Forensics CTFs](https://github.com/apsdehal/awesome-ctf/blob/master/README.md#forensics)
- [MagnetForensics CTF Challenge](https://www.magnetforensics.com/blog/magnet-weekly-ctf-challenge/)
- [MalwareTech Labs](https://malwaretech.com/labs/)
- [MemLabs](https://github.com/stuxnet999/MemLabs)
- [NW3C Chanllenges](https://nw3.ctfd.io)
- [Intrusión de Precision Widgets of North Dakota](https://betweentwodfirns.blogspot.com/2017/11/dfir-ctf-precision-widgets-of-north.html)
- [Retos de Ingeniería Inversa](https://challenges.re)

 Recursos

# Web

- [ForensicsFocus](https://www.forensicfocus.com/)
- [SANS Digital Forensics](https://www.sans.org/cybersecurity-focus-areas/digital-forensics-incident-response)

# Blogs
- [Netresec](https://www.netresec.com/index.ashx?page=Blog)
- [Blog de Informática Forense de SANS](https://www.sans.org/blog?focus-area=digital-forensics)
- [SecurityAffairs](https://securityaffairs.com/) - blog de Pierluigi Paganini
- [This Week In 4n6](https://thisweekin4n6.com/) - Actualizaciones semanales para informática forense
- [Zena Forensics](https://blog.digital-forensics.it/)

# Libros

*más en [Lecturas Recomendadas](http://dfir.org/?q=node/8) por Andrew Case*

- [Informática Forense de Redes: Rastreando Hackers a través del Ciberespacio](https://www.pearson.com/en-us/subject-catalog/p/Davidoff-Network-Forensics-Tracking-Hackers-through-Cyberspace/P200000009228) - Aprenda a reconocer las huellas de los hackers y a descubrir pruebas basadas en la red.
- [El Arte de la Informática Forense de la Memoria](https://memoryanalysis.net/amf/) - Detección de Malware y Amenazas en la Memoria de Windows, Linux y Mac
- [La Práctica de la Monitorización de la Seguridad de la Red](https://nostarch.com/nsm) - Entendiendo la Detección y Respuesta de Incidentes

# Corpora de Sistemas de Archivos

- [Imágenes del Desafío de Informática Forense Digital](https://www.ashemery.com/dfir.html) - Dos desafíos DFIR con imágenes
- [Imágenes de Prueba de Herramientas de Informática Forense Digital](https://sourceforge.net/projects/dftt/)
- [El Proyecto CFReDS](https://cfreds.nist.gov)
- [Caso de Hackeo (Imagen NTFS de 4.5 GB)](https://cfreds.nist.gov/Hacking_Case.html)

# Otros

- [/r/computerforensics/](https://www.reddit.com/r/computerforensics/) - Subreddit para informática forense
- [CybersecurityGuide – Carreras en Informática Forense Digital](https://cybersecurityguide.org/careers/digital-forensics/) - Guía sobre habilidades, certificaciones y trayectorias profesionales en informática forense cibernética.
- [ForensicPosters](https://github.com/Invoke-IR/ForensicPosters) - Posters de estructuras de sistemas de archivos
- [Posters de SANS](https://www.sans.org/posters) - Posters gratuitos proporcionados por SANS

# Laboratorios

- [BlueTeam.Lab](https://github.com/op7ic/BlueTeam.Lab) - Laboratorio de detección de Blue Team creado con Terraform y Ansible en Azure.

 Listas Impresionantes Relacionadas

- [Seguridad de Android](https://github.com/ashishb/android-security-awesome)
- [AppSec](https://github.com/paragonie/awesome-appsec)
- [CTFs](https://github.com/apsdehal/awesome-ctf)
- [Hacking](https://github.com/carpedm20/awesome-hacking)
- [Honeypots](https://github.com/paralax/awesome-honeypots)
- [Incident-Response](https://github.com/meirwah/awesome-incident-response)
- [Infosec](https://github.com/onlurking/awesome-infosec)
- [Análisis de Malware](https://github.com/rshipp/awesome-malware-analysis)
- [Pentesting](https://github.com/enaqx/awesome-pentest)
- [Seguridad](https://github.com/sbilly/awesome-security)
- [Ingeniería Social](https://github.com/giuliacassara/awesome-social-engineering)
- [YARA](https://github.com/InQuest/awesome-yara)

