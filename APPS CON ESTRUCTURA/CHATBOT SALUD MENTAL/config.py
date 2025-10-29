UI_MESSAGES = {
    'es': {
        'welcome': '¡Hola! Soy Uli, tu asistente de salud mental. ¿En qué puedo ayudarte hoy?',
        'thinking': 'Pensando...',
        'no_results': 'Lo siento, no encontré información específica sobre tu consulta. ¿Podrías reformular tu pregunta?',
        'error': 'Ha ocurrido un error. Por favor, intenta de nuevo.',
        'placeholder': 'Escribe tu pregunta aquí...',
        'send_button': 'Enviar',
        'clear_button': 'Limpiar Chat',
        'confidence': 'Confianza: {:.1%}'
    },
    'en': {
        'welcome': 'Hello! I\'m Uli, your mental health assistant. How can I help you today?',
        'thinking': 'Thinking...',
        'no_results': 'Sorry, I couldn\'t find specific information about your query. Could you rephrase your question?',
        'error': 'An error occurred. Please try again.',
        'placeholder': 'Type your question here...',
        'send_button': 'Send',
        'clear_button': 'Clear Chat',
        'confidence': 'Confidence: {:.1%}'
    }
}

# Stop words para diferentes idiomas
STOP_WORDS = {
    'es': [
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son',
        'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'me', 'ya', 'muy', 'mi', 'sin',
        'sobre', 'este', 'ser', 'tiene', 'todo', 'esta', 'era', 'cuando', 'él', 'más', 'si', 'puede', 'o', 'qué',
        'cómo', 'cuál', 'cuáles', 'dónde', 'cuándo', 'por qué', 'porque'
    ],
    'en': [
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'what', 'how', 'when',
        'where', 'why', 'which', 'who', 'whom'
    ]
}
