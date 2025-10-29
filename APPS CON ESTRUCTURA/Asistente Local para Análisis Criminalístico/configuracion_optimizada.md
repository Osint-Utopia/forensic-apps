# Configuración Optimizada para Mistral-7B-Instruct

## PARÁMETROS ACTUALES vs RECOMENDADOS

### Longitud de Contexto
**Actual**: 2048 tokens entrada/salida  
**Recomendado**: 4096-8192 tokens  
**Justificación**: Para consultas jurídico-forenses complejas necesitas más contexto para citar normatividad, jurisprudencia y metodología técnica.

### Longitud Máxima de Salida
**Actual**: 4096 tokens  
**Recomendado**: 2048-3072 tokens  
**Justificación**: Respuestas más concisas y enfocadas. Para peritajes largos, mejor dividir en secciones.

### Temperatura
**Actual**: >0.7  
**Recomendado**: 0.3-0.5  
**Justificación**: Contenido técnico-legal requiere mayor precisión y menor creatividad. Temperatura alta puede generar imprecisiones.

### Top-P (Nucleus Sampling)
**Actual**: 0.4  
**Recomendado**: 0.8-0.9  
**Justificación**: Valor actual muy restrictivo. Para terminología técnica necesitas mayor diversidad léxica.

### Top-K
**Actual**: 40  
**Recomendado**: 50-80  
**Justificación**: Ampliar vocabulario técnico disponible, especialmente importante para términos jurídicos especializados.

### Min-P
**Actual**: 0  
**Recomendado**: 0.05-0.1  
**Justificación**: Filtrar tokens con probabilidad muy baja mejora coherencia técnica.

## CONFIGURACIÓN OPTIMIZADA SUGERIDA

```yaml
# Configuración para Contenido Técnico-Legal
context_length: 6144          # Contexto ampliado
max_output_length: 2560       # Respuestas más concisas
batch_size: 64               # Reducir para mayor estabilidad
temperature: 0.4             # Más determinista
top_p: 0.85                  # Mejor balance
top_k: 60                    # Vocabulario técnico ampliado
min_p: 0.08                  # Filtro de calidad
repetition_penalty: 1.15     # Ligeramente menor
repetition_penalty_tokens: 128  # Ventana ampliada
gpu_layers: 64               # Mantener (depende de VRAM)
```

## CONFIGURACIONES ALTERNATIVAS

### Para Consultas Jurídicas Complejas
```yaml
temperature: 0.2-0.3         # Máxima precisión legal
top_p: 0.9                   # Vocabulario jurídico completo
context_length: 8192         # Para citar múltiples artículos
```

### Para Peritajes Técnicos
```yaml
temperature: 0.3-0.4         # Balance precisión/fluidez
top_k: 80                    # Terminología científica amplia
min_p: 0.1                   # Filtro estricto
```

### Para Redacción de Documentos
```yaml
temperature: 0.5             # Mayor fluidez narrativa
repetition_penalty: 1.1     # Menor para documentos largos
max_output_length: 3072     # Documentos más extensos
```

## CONSIDERACIONES ADICIONALES

**Monitoreo de Rendimiento**:
- Observa coherencia en citas legales
- Verifica precisión en terminología técnica
- Evalúa fluidez en redacción de peritajes

**Ajustes Dinámicos**:
- Consultas simples: Temperatura +0.1
- Casos complejos: Temperatura -0.1
- Documentos largos: Reducir repetition_penalty

**Limitaciones de Hardware**:
Si experimentas problemas de memoria:
- Reducir context_length a 4096
- Bajar batch_size a 32
- Ajustar gpu_layers según VRAM disponible