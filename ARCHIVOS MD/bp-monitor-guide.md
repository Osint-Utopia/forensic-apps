# GUÍA DE USUARIO
## Monitor de Presión Arterial - Sistema Integral de Salud

---

## TABLA DE CONTENIDOS

1. Introducción
2. Requisitos del Sistema
3. Características Principales
4. Guía de Uso por Sección
5. Gestión de Datos
6. Interpretación de Resultados
7. Recomendaciones de Uso
8. Preguntas Frecuentes
9. Soporte Técnico

---

## 1. INTRODUCCIÓN

El Monitor de Presión Arterial es una aplicación web integral diseñada para el seguimiento y control de la salud cardiovascular. Esta herramienta permite registrar, analizar y gestionar múltiples aspectos de la salud, incluyendo presión arterial, ejercicio, nutrición y tareas médicas.

### Propósito

- Monitoreo continuo de presión arterial
- Seguimiento de progreso en ejercicio físico
- Acceso a recetas saludables para diabéticos e hipertensos
- Gestión organizada de tareas de salud
- Generación de estadísticas y gráficas de evolución

### Beneficios

- Control integral de salud cardiovascular
- Datos almacenados localmente en su navegador
- Sin necesidad de registro o conexión a internet
- Visualización clara de tendencias y patrones
- Recomendaciones personalizadas según sus lecturas

---

## 2. REQUISITOS DEL SISTEMA

### Navegadores Compatibles

- Google Chrome versión 90 o superior
- Mozilla Firefox versión 88 o superior
- Microsoft Edge versión 90 o superior
- Safari versión 14 o superior

### Dispositivos

- Computadoras de escritorio
- Laptops
- Tablets
- Teléfonos móviles (diseño responsive)

### Almacenamiento

- Mínimo 10 MB de espacio en localStorage del navegador
- No requiere instalación de software adicional

---

## 3. CARACTERÍSTICAS PRINCIPALES

### 3.1 Gestión de Perfil

Permite registrar y mantener actualizada su información personal de salud:

- Nombre completo
- Fecha de nacimiento
- Peso y altura
- Género
- Condiciones médicas preexistentes
- Cálculo automático de edad e IMC (Índice de Masa Corporal)

### 3.2 Registro de Presión Arterial

Sistema completo para documentar mediciones:

- Fecha y hora de cada lectura
- Presión sistólica (mmHg)
- Presión diastólica (mmHg)
- Frecuencia cardíaca (latidos por minuto)
- Notas contextuales
- Categorización automática según estándares de la American Heart Association

### 3.3 Dashboard de Análisis

Visualización gráfica y estadística de sus datos:

- Promedios de presión sistólica, diastólica y pulso
- Contador total de mediciones
- Gráficas de evolución temporal
- Filtros por período (semana, mes, trimestre, todos)
- Recomendaciones personalizadas según sus promedios

### 3.4 Sección de Nutrición

Base de datos de recetas saludables:

- 8 recetas completas con instrucciones detalladas
- Filtros por condición (diabetes, hipertensión, ambas)
- Filtros por tipo de comida (desayuno, comida, cena, snack)
- Información nutricional: calorías, carbohidratos, sodio
- Tiempos de preparación
- Ingredientes medidos con precisión
- Pasos de preparación numerados

### 3.5 Plan de Ejercicio

Sistema de seguimiento de actividad física:

- Plan semanal completo (7 días)
- 2 ejercicios diarios con duración y calorías
- Checkbox para marcar ejercicios completados
- Estadísticas de progreso:
  - Porcentaje de cumplimiento semanal
  - Total de entrenamientos realizados
  - Racha de días consecutivos
  - Calorías totales quemadas
- Calendario visual de últimos 30 días
- Opción de reiniciar progreso

### 3.6 Sistema Kanban

Gestión de tareas relacionadas con salud:

- Tres columnas: Por Hacer, En Progreso, Completado
- Funcionalidad drag and drop para mover tareas
- Atributos de tareas:
  - Título y descripción
  - Prioridad (Alta, Media, Baja)
  - Categoría (Medicación, Cita, Ejercicio, Nutrición, Análisis, Otro)
  - Fecha límite opcional
- Contador de tareas por columna
- Eliminación individual de tareas

### 3.7 Historial Completo

Registro detallado de todas las mediciones:

- Tabla con todas las lecturas guardadas
- Filtros por fecha específica
- Filtros por nivel de riesgo
- Visualización de categoría de cada lectura
- Opción de eliminar mediciones individuales
- Botón para limpiar todos los datos

---

## 4. GUÍA DE USO POR SECCIÓN

### 4.1 CONFIGURACIÓN DE PERFIL

**Pasos para completar su perfil:**

1. Al abrir la aplicación, la pestaña "Perfil" está activa por defecto
2. Complete el formulario con su información:
   - Ingrese su nombre completo
   - Seleccione su fecha de nacimiento
   - Registre su peso en kilogramos (acepta decimales)
   - Ingrese su altura en centímetros (número entero)
   - Seleccione su género (Masculino/Femenino)
   - Describa sus condiciones médicas actuales si las tiene
3. Haga clic en el botón "Guardar Perfil"
4. El sistema calculará automáticamente:
   - Su edad actual
   - Su Índice de Masa Corporal (IMC)
   - Categoría de IMC (Bajo peso, Normal, Sobrepeso, Obesidad)
5. Un resumen visual aparecerá mostrando sus datos principales

**Nota importante:** Esta información se utiliza para personalizar las recomendaciones que recibe.

---

### 4.2 REGISTRO DE MEDICIONES

**Cómo registrar una nueva lectura:**

1. Navegue a la pestaña "Registrar"
2. Los campos de fecha y hora se completan automáticamente con la fecha/hora actual
3. Puede modificar la fecha y hora si la medición fue anterior
4. Ingrese los valores obtenidos de su monitor de presión:
   - Presión Sistólica: valor entre 70-300 mmHg
   - Presión Diastólica: valor entre 40-200 mmHg
   - Pulso: frecuencia cardíaca entre 30-200 latidos por minuto
5. Agregue notas relevantes (opcional):
   - Actividad realizada antes de la medición
   - Estado emocional
   - Síntomas experimentados
   - Medicamentos tomados
6. Haga clic en "Registrar Medición"
7. El sistema mostrará inmediatamente:
   - Resultado de la medición con categoría
   - Nivel de riesgo con código de color
   - Recomendaciones específicas según el resultado

**Interpretación de categorías:**

- **Normal:** Sistólica menor a 120 Y diastólica menor a 80
- **Elevada:** Sistólica 120-129 Y diastólica menor a 80
- **Hipertensión Etapa 1:** Sistólica 130-139 O diastólica 80-89
- **Hipertensión Etapa 2:** Sistólica 140 o mayor O diastólica 90 o mayor
- **Crisis Hipertensiva:** Sistólica mayor a 180 O diastólica mayor a 120

**Recomendaciones según categoría:**

El sistema proporciona consejos adaptados a cada nivel de presión arterial, incluyendo:
- Guías alimenticias locales
- Frecuencia de monitoreo recomendada
- Actividades físicas sugeridas
- Cuándo buscar atención médica
- Consideraciones especiales para adultos mayores

---

### 4.3 ANÁLISIS EN DASHBOARD

**Visualización de estadísticas:**

1. Acceda a la pestaña "Dashboard"
2. Observe las 4 tarjetas de estadísticas principales:
   - **Sistólica Promedio:** media de todas sus lecturas sistólicas
   - **Diastólica Promedio:** media de todas sus lecturas diastólicas
   - **Pulso Promedio:** frecuencia cardíaca promedio
   - **Total Mediciones:** cantidad de registros guardados

**Uso de filtros temporales:**

1. Seleccione el período deseado en el menú desplegable:
   - **Última Semana:** últimos 7 días
   - **Último Mes:** últimos 30 días
   - **Últimos 3 Meses:** últimos 90 días (opción por defecto)
   - **Todos los Registros:** sin límite temporal
2. Las gráficas se actualizarán automáticamente

**Interpretación de gráficas:**

**Gráfica 1: Evolución de la Presión Arterial**
- Línea roja: presión sistólica
- Línea azul: presión diastólica
- Eje horizontal: fechas y horas de medición
- Eje vertical: valores en mmHg
- Líneas punteadas: valores de referencia normales

**Gráfica 2: Evolución del Pulso**
- Línea verde: frecuencia cardíaca
- Muestra variaciones del pulso en el tiempo
- Útil para detectar patrones o anomalías

**Recomendaciones Personalizadas:**

Debajo de las gráficas encontrará:
- Evaluación de sus promedios
- Categoría promedio de su presión
- Consejos específicos según su historial
- Recomendaciones dietéticas locales
- Sugerencias de actividad física

---

### 4.4 SECCIÓN DE NUTRICIÓN

**Exploración de recetas:**

1. Navegue a la pestaña "Nutrición"
2. Use los filtros disponibles:
   
   **Filtro por condición:**
   - Todas las recetas
   - Para Diabéticos
   - Para Hipertensos
   - Diabetes e Hipertensión (ambas condiciones)
   
   **Filtro por tipo de comida:**
   - Todos
   - Desayuno
   - Comida
   - Cena
   - Snack

3. Las recetas se filtrarán automáticamente al cambiar cualquier selector

**Información de cada receta:**

Cada tarjeta de receta contiene:

**Encabezado:**
- Nombre del platillo
- Etiquetas de condición (para quién es apta)
- Tiempo de preparación en minutos

**Información nutricional:**
- Calorías totales
- Gramos de carbohidratos
- Miligramos de sodio
- Número de porciones

**Ingredientes:**
- Lista completa de ingredientes
- Cantidades específicas
- Indicaciones de preparación de ingredientes

**Instrucciones:**
- Pasos numerados
- Orden secuencial de preparación
- Técnicas de cocción
- Tiempos específicos cuando aplica

**Recetas disponibles:**

1. **Ensalada de Nopales con Atún**
   - Apta para diabetes e hipertensión
   - 180 calorías, 15 minutos
   - Tipo: Comida

2. **Agua de Jamaica sin Azúcar**
   - Apta para diabetes e hipertensión
   - 5 calorías, 20 minutos
   - Tipo: Snack

3. **Tacos de Pescado a la Plancha**
   - Apta para hipertensión
   - 320 calorías, 25 minutos
   - Tipo: Comida

4. **Licuado Verde Energético**
   - Apto para diabetes e hipertensión
   - 150 calorías, 10 minutos
   - Tipo: Desayuno

5. **Caldo de Pollo con Verduras**
   - Apto para diabetes e hipertensión
   - 220 calorías, 40 minutos
   - Tipo: Cena

6. **Avena con Frutos Rojos**
   - Apta para diabetes e hipertensión
   - 280 calorías, 15 minutos
   - Tipo: Desayuno

7. **Pechuga de Pollo con Vegetales al Vapor**
   - Apta para diabetes e hipertensión
   - 350 calorías, 30 minutos
   - Tipo: Comida

8. **Ensalada de Lentejas**
   - Apta para diabetes e hipertensión
   - 290 calorías, 35 minutos
   - Tipo: Comida

---

### 4.5 PLAN DE EJERCICIO

**Estructura del plan semanal:**

El sistema incluye un plan de ejercicio de 7 días diseñado para personas con hipertensión o diabetes. Cada día tiene ejercicios específicos con duración, calorías estimadas y tipo de actividad.

**Plan detallado por día:**

**LUNES:**
- Caminata ligera: 30 min, 150 cal, cardio
- Estiramientos: 10 min, 30 cal, flexibilidad

**MARTES:**
- Ejercicios de resistencia con banda: 20 min, 120 cal, fuerza
- Yoga suave: 15 min, 60 cal, flexibilidad

**MIÉRCOLES:**
- Natación o aqua aerobics: 30 min, 200 cal, cardio
- Ejercicios de respiración: 10 min, 20 cal, relajación

**JUEVES:**
- Bicicleta estática: 25 min, 180 cal, cardio
- Ejercicios de equilibrio: 15 min, 50 cal, equilibrio

**VIERNES:**
- Caminata rápida: 35 min, 180 cal, cardio
- Estiramientos: 10 min, 30 cal, flexibilidad

**SÁBADO:**
- Tai Chi o Qi Gong: 30 min, 100 cal, equilibrio
- Ejercicios de fuerza ligeros: 20 min, 110 cal, fuerza

**DOMINGO:**
- Descanso activo - Caminata suave: 20 min, 80 cal, cardio
- Meditación y respiración: 15 min, 20 cal, relajación

**Cómo usar el seguimiento:**

1. Acceda a la pestaña "Ejercicio"
2. Visualice el plan completo en el panel izquierdo
3. Después de completar un ejercicio:
   - Marque el checkbox junto al ejercicio realizado
   - El sistema registra automáticamente:
     - Fecha de completación
     - Calorías quemadas
     - Actualización del calendario
4. Observe el panel derecho con sus estadísticas:
   - **Progreso semanal:** porcentaje de ejercicios completados esta semana
   - **Total entrenamientos:** días en los que realizó al menos un ejercicio
   - **Racha actual:** días consecutivos con actividad
   - **Calorías quemadas:** suma total desde el inicio

**Calendario visual:**

- Muestra los últimos 30 días
- Código de colores:
  - Gris: día sin ejercicio
  - Naranja: ejercicio parcial (1 de 2)
  - Verde: día completo (2 de 2 ejercicios)
- Pase el cursor sobre un día para ver detalles

**Reinicio de progreso:**

Si desea comenzar desde cero:
1. Haga clic en "Reiniciar Progreso"
2. Confirme la acción (se borrarán todos los registros de ejercicio)
3. El calendario y estadísticas volverán a cero

---

### 4.6 SISTEMA KANBAN

**Estructura del tablero:**

El tablero Kanban está dividido en tres columnas:

1. **Por Hacer:** tareas pendientes
2. **En Progreso:** tareas que está realizando actualmente
3. **Completado:** tareas finalizadas

**Crear una nueva tarea:**

1. Haga clic en "Nueva Tarea" o en "+ Agregar tarea" en cualquier columna
2. Complete el formulario:
   - **Título:** descripción breve de la tarea (requerido)
   - **Descripción:** detalles adicionales (opcional)
   - **Prioridad:** seleccione Alta, Media o Baja (requerido)
   - **Categoría:** tipo de tarea (requerido):
     - Medicación: recordatorios de tomar medicamentos
     - Cita Médica: consultas programadas
     - Ejercicio: metas de actividad física
     - Nutrición: objetivos alimenticios
     - Análisis: estudios o exámenes médicos
     - Otro: cualquier otra tarea de salud
   - **Fecha Límite:** cuándo debe completarse (opcional)
3. Haga clic en "Guardar Tarea"
4. La tarea aparecerá en la columna correspondiente

**Mover tareas entre columnas:**

Método 1 - Arrastrar y soltar:
1. Haga clic sobre una tarjeta de tarea
2. Mantenga presionado el botón del mouse
3. Arrastre la tarjeta a la columna deseada
4. Suelte el botón del mouse
5. La tarea se moverá automáticamente

Método 2 - En dispositivos táctiles:
1. Mantenga presionado sobre la tarjeta
2. Arrastre hacia la columna deseada
3. Suelte

**Interpretar las tarjetas:**

Cada tarjeta muestra:
- Icono según categoría en el título
- Nombre de la tarea
- Descripción (si se proporcionó)
- Etiqueta de prioridad con color:
  - Rojo: prioridad alta
  - Amarillo: prioridad media
  - Verde: prioridad baja
- Fecha límite (si se estableció)
- Botón de eliminar

**Eliminar tareas:**

1. Haga clic en el botón de eliminar (icono de basura) en la tarjeta
2. Confirme la eliminación
3. La tarea se eliminará permanentemente

**Contador de tareas:**

Cada columna muestra en su encabezado el número total de tareas que contiene.

---

### 4.7 HISTORIAL DE MEDICIONES

**Visualización del historial:**

1. Navegue a la pestaña "Historial"
2. Verá una tabla con todas sus mediciones registradas
3. Las columnas muestran:
   - Fecha de la medición
   - Hora de la medición
   - Presión sistólica
   - Presión diastólica
   - Frecuencia cardíaca (pulso)
   - Categoría de riesgo
   - Notas asociadas
   - Botón de acciones

**Uso de filtros:**

**Filtro por fecha:**
1. Seleccione una fecha específica en el selector
2. Solo se mostrarán las mediciones de ese día
3. Limpie el campo para ver todas las fechas

**Filtro por nivel de riesgo:**
1. Seleccione la categoría deseada:
   - Normal
   - Elevada
   - Hipertensión Etapa 1
   - Hipertensión Etapa 2
   - Crisis Hipertensiva
2. Solo se mostrarán mediciones de esa categoría
3. Seleccione "Todos los niveles" para ver todas

**Eliminar mediciones:**

Para eliminar una medición individual:
1. Haga clic en el botón "Eliminar" en la fila correspondiente
2. Confirme la acción
3. La medición se eliminará permanentemente

Para limpiar todos los datos:
1. Haga clic en "Limpiar Datos" en la parte superior
2. Confirme dos veces (seguridad adicional)
3. Se eliminarán:
   - Todos los datos del perfil
   - Todas las mediciones de presión
   - Todo el progreso de ejercicio
   - Todas las tareas del Kanban

---

## 5. GESTIÓN DE DATOS

### 5.1 Almacenamiento Local

**Cómo funciona:**

- Todos los datos se guardan en el localStorage de su navegador
- El almacenamiento es automático después de cada acción
- No se envía información a servidores externos
- Los datos persisten entre sesiones

**Datos almacenados:**

1. **Perfil del usuario:**
   - Información personal
   - Cálculos de IMC y edad

2. **Mediciones de presión arterial:**
   - Todas las lecturas históricas
   - Fechas, horas y valores
   - Notas y categorías

3. **Progreso de ejercicio:**
   - Ejercicios completados por fecha
   - Calendario de actividad
   - Estadísticas acumuladas

4. **Tareas Kanban:**
   - Todas las tareas en las tres columnas
   - Detalles y estado de cada tarea

### 5.2 Exportación de Datos

**Para exportar sus datos:**

1. Vaya a la pestaña "Historial"
2. Desplácese hacia abajo hasta la sección "Gestión de Datos"
3. Haga clic en "Exportar Datos"
4. Se descargará un archivo JSON con nombre:
   `presion_arterial_YYYY-MM-DD.json`
5. Guarde este archivo en un lugar seguro

**Contenido del archivo exportado:**

- Versión del formato de datos
- Fecha y hora de exportación
- Información completa del perfil
- Todas las mediciones de presión
- Todo el progreso de ejercicio
- Todas las tareas Kanban

**Usos recomendados:**

- Respaldo de seguridad regular
- Compartir datos con su médico
- Transferir datos a otro dispositivo
- Archivo histórico de su salud

### 5.3 Importación de Datos

**Para importar datos previamente exportados:**

1. Vaya a la pestaña "Historial"
2. En la sección "Gestión de Datos", haga clic en "Importar Datos"
3. Seleccione el archivo JSON previamente exportado
4. El sistema validará el formato
5. Si es válido, los datos se cargarán automáticamente
6. Se sobrescribirán los datos actuales con los importados

**Precauciones:**

- Solo importe archivos exportados por esta aplicación
- Los datos actuales serán reemplazados completamente
- Exporte sus datos actuales antes de importar si desea conservarlos
- Verifique que el archivo no esté corrupto

### 5.4 Privacidad y Seguridad

**Medidas de seguridad:**

- Los datos nunca salen de su dispositivo
- No hay conexión con servidores externos
- No se requiere registro ni credenciales
- El almacenamiento está protegido por el navegador

**Limitaciones:**

- Si borra los datos del navegador, perderá la información
- Los datos no se sincronizan entre dispositivos automáticamente
- No hay recuperación automática de datos eliminados

**Recomendaciones:**

- Exporte sus datos regularmente (semanal o mensualmente)
- Guarde los archivos exportados en múltiples ubicaciones
- No comparta archivos exportados sin encriptar si contienen información sensible
- Use un navegador actualizado con medidas de seguridad activas

---

## 6. INTERPRETACIÓN DE RESULTADOS

### 6.1 Categorías de Presión Arterial

**Según la American Heart Association adaptado para México:**

**NORMAL:**
- Sistólica: menos de 120 mmHg
- Diastólica: menos de 80 mmHg
- Acción: Mantener estilo de vida saludable
- Frecuencia de monitoreo: cada 6-12 meses

**ELEVADA:**
- Sistólica: 120-129 mmHg
- Diastólica: menos de 80 mmHg
- Acción: Modificaciones en estilo de vida
- Frecuencia de monitoreo: semanal

**HIPERTENSIÓN ETAPA 1:**
- Sistólica: 130-139 mmHg O
- Diastólica: 80-89 mmHg
- Acción: Consulta médica recomendada
- Posible necesidad de medicamentos
- Frecuencia de monitoreo: 2-3 veces por semana

**HIPERTENSIÓN ETAPA 2:**
- Sistólica: 140 mmHg o mayor O
- Diastólica: 90 mmHg o mayor
- Acción: Atención médica inmediata (48 horas)
- Probable necesidad de medicamentos
- Frecuencia de monitoreo: diario

**CRISIS HIPERTENSIVA:**
- Sistólica: mayor a 180 mmHg O
- Diastólica: mayor a 120 mmHg
- Acción: EMERGENCIA MÉDICA
- Ir inmediatamente a urgencias
- Llamar a servicios de emergencia

### 6.2 Interpretación de Gráficas

**Tendencias a observar:**

**Tendencia ascendente:**
- La presión aumenta con el tiempo
- Puede indicar descontrol
- Revisar adherencia a tratamiento
- Consultar con médico

**Tendencia descendente:**
- La presión disminuye con el tiempo
- Puede indicar mejora
- Continuar con tratamiento actual
- Mantener estilo de vida saludable

**Variabilidad alta:**
- Grandes diferencias entre mediciones
- Puede indicar:
  - Mediciones en momentos muy diferentes del día
  - Estrés variable
  - Problemas con la técnica de medición
  - Efectividad inconsistente del tratamiento

**Estabilidad:**
- Lecturas consistentes en el tiempo
- Indica buen control
- Tratamiento efectivo

### 6.3 Frecuencia Cardíaca Normal

**Rangos por edad (en reposo):**

- Adultos (18-64 años): 60-100 lpm
- Adultos mayores (65+): 60-100 lpm
- Atletas: 40-60 lpm

**Bradicardia (pulso bajo):**
- Menor a 60 lpm en adultos no atletas
- Puede ser normal en atletas
- Consultar si hay síntomas (mareos, fatiga)

**Taquicardia (pulso alto):**
- Mayor a 100 lpm en reposo
- Puede indicar:
  - Estrés o ansiedad
  - Fiebre
  - Deshidratación
  - Problemas cardíacos
- Consultar con médico si es persistente

### 6.4 Índice de Masa Corporal (IMC)

**Categorías según OMS:**

- Bajo peso: IMC menor a 18.5
- Normal: IMC 18.5 - 24.9
- Sobrepeso: IMC 25.0 - 29.9
- Obesidad grado 1: IMC 30.0 - 34.9
- Obesidad grado 2: IMC 35.0 - 39.9
- Obesidad grado 3: IMC 40.0 o mayor

**Relación con presión arterial:**

- El sobrepeso y obesidad aumentan el riesgo de hipertensión
- Reducción de 5-10% del peso puede disminuir significativamente la presión
- El IMC es solo un indicador, consulte con profesional de salud

---

## 7. RECOMENDACIONES DE USO

### 7.1 Mejores Prácticas para Medición

**Preparación antes de medir:**

- No consuma cafeína 30 minutos antes
- Evite fumar 30 minutos antes
- Vacíe su vejiga
- Siéntese tranquilamente 5 minutos antes
- No hable durante la medición
- Apoye su espalda y pies en el suelo
- Coloque el brazo a la altura del corazón

**Momento de las mediciones:**

- Mida a la misma hora cada día
- Idealmente por la mañana (antes de medicamentos)
- Y por la noche (antes de acostarse)
- Tome 2-3 mediciones con 1 minuto de intervalo
- Registre el promedio

**Frecuencia recomendada:**

- Presión normal: mensual o según indicación médica
- Presión elevada: semanal
- Hipertensión: diario (mañana y noche)
- Durante cambio de medicamento: según indicación médica

### 7.2 Uso del Plan de Ejercicio

**Antes de comenzar:**

- Consulte con su médico antes de iniciar cualquier programa de ejercicio
- Comience gradualmente
- Escuche a su cuerpo
- Detenga el ejercicio si siente:
  - Dolor en el pecho
  - Dificultad severa para respirar
  - Mareos o náuseas
  - Palpitaciones irregulares

**Durante el ejercicio:**

- Manténgase hidratado
- Use ropa cómoda y calzado adecuado
- Evite ejercicio en clima extremo
- No haga ejercicio si no se siente bien
- Caliente antes y enfríe después

**Progresión segura:**

- Aumente intensidad gradualmente
- Respete los días de descanso
- Varíe los tipos de ejercicio
- Escuche las señales de su cuerpo

### 7.3 Implementación de Recetas

**Sustituciones permitidas:**

- Use ingredientes frescos locales de temporada
- Puede sustituir vegetales por similares
- Ajuste especias según tolerancia
- Reduzca porciones si está en control de peso

**Control de sodio:**

- No agregue sal adicional
- Use hierbas y especias para dar sabor
- Lea etiquetas de ingredientes procesados
- Enjuague alimentos enlatados antes de usar

**Control de carbohidratos (diabéticos):**

- Respete las porciones indicadas
- No agregue azúcares o endulzantes no especificados
- Combine con verduras no almidonadas
- Distribuya carbohidratos a lo largo del día

### 7.4 Gestión del Kanban

**Organización efectiva:**

- Cree tareas específicas y medibles