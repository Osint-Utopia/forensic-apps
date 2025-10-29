---
dataset_info:
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_examples: 172
license: mit
task_categories:
- text-generation
language:
- en
tags:
- medical
pretty_name: Conjunto de Datos de Chatbot de Salud Mental
size_categories:
- n<1K
---

# Tarjeta del Conjunto de Datos para "heliosbrahma/mental_health_chatbot_dataset"

## Tabla de Contenidos
- [Descripción del Conjunto de Datos](#dataset-description)
  - [Resumen del Conjunto de Datos](#dataset-summary)
  - [Idiomas](#languages)
- [Estructura del Conjunto de Datos](#dataset-structure)
  - [Instancias de Datos](#data-instances)
  - [Campos de Datos](#data-instances)
- [Creación del Conjunto de Datos](#dataset-creation)
  - [Justificación de la Curación](#curation-rationale)
  - [Datos de Origen](#source-data)
  - [Información Personal y Sensible](#personal-and-sensitive-information)

## Descripción del Conjunto de Datos

### Resumen del Conjunto de Datos

Este conjunto de datos contiene pares conversacionales de preguntas y respuestas en un único texto relacionado con la Salud Mental. El conjunto de datos fue curado de blogs populares de atención médica como WebMD, Mayo Clinic y HeatlhLine, preguntas frecuentes en línea, etc. Todas las preguntas y respuestas se han anonimizado para eliminar cualquier dato PII y se han preprocesado para eliminar cualquier carácter no deseado.

### Idiomas

El texto del conjunto de datos está en inglés.

## Estructura del Conjunto de Datos

### Instancias de Datos

Una instancia de datos incluye una columna de texto que es un par conversacional de preguntas y respuestas. Las preguntas fueron formuladas por los pacientes y las respuestas fueron dadas por los proveedores de atención médica.

### Campos de Datos

- 'text': par conversacional de preguntas y respuestas entre el paciente y el proveedor de atención médica.

## Creación del Conjunto de Datos

### Justificación de la Curación

Los chatbots ofrecen una plataforma fácilmente disponible y accesible para las personas que buscan apoyo. Se puede acceder a ellos en cualquier momento y en cualquier lugar, brindando asistencia inmediata a quienes lo necesitan. Los chatbots pueden ofrecer respuestas empáticas y sin prejuicios, brindando apoyo emocional a los usuarios. Si bien no pueden reemplazar por completo la interacción humana, pueden ser un complemento útil, especialmente en momentos de angustia.
Por lo tanto, este conjunto de datos fue curado para ayudar a ajustar un bot de IA conversacional utilizando este conjunto de datos personalizado que luego se puede implementar y proporcionar al paciente final como un chatbot.

### Datos de Origen

Este conjunto de datos fue curado de blogs populares de atención médica como WebMD, Mayo Clinic y HeatlhLine, preguntas frecuentes en línea, etc.

### Información Personal y Sensible

El conjunto de datos puede contener información sensible relacionada con la salud mental. Todas las preguntas y respuestas se han anonimizado para eliminar cualquier dato PII.