

	Primero, necesitas obtener tu API key de OpenRouter:

Ve a https://openrouter.ai/
Crea una cuenta y obtén tu API key
OpenRouter te dará créditos gratuitos para empezar

Aquí te creo un ejemplo de implementación para tu app:Integración Claude API - Laboratorio ForenseArtefacto interactivo ¡Listo! Te he creado una integración completa de Claude API para tu aplicación forense. Aquí tienes los puntos clave:
🔑 Pasos para usar:

Obtén tu API Key:

Ve a https://openrouter.ai/
Crea cuenta (gratis)
Obtén tu API key
OpenRouter te da créditos gratis para empezar


Características incluidas:

✅ Interfaz especializada para análisis forense
✅ Prompts predefinidos para casos comunes
✅ Historial de conversación
✅ Guardado automático de API key
✅ Contexto especializado en criminalística



🔬 Funciones específicas para tu app:

Análisis de evidencias fotográficas
Interpretación de metadatos EXIF
Procedimientos forenses estándar
Análisis entomológico
Generación de reportes criminalísticos
Patrones geoespaciales

💡 Para integrar en tu app existente:

*//------------------------------------------------------------//*
javascript// Función básica para llamar a Claude
async function callClaude(prompt, apiKey) {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'anthropic/claude-3.7-sonnet',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 1000
        })
    });
    
    const data = await response.json();
    return data.choices[0].message.content;
}
*//---------------------------------------------------------//*

💰 Costos:

Claude 3.7 Sonnet: GRATIS hasta cierto límite
Claude 3 Haiku: ~$0.25 por millón de tokens (muy barato)
OpenRouter te da créditos iniciales gratuitos

	// Función básica para llamar a Claude
	
	*//---------------------------------------------------------//*
async function callClaude(prompt, apiKey) {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'anthropic/claude-3.7-sonnet',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 1000
        })
    });
    
    const data = await response.json();
    return data.choices[0].message.content;
}
	*//---------------------------------------------------------//*

