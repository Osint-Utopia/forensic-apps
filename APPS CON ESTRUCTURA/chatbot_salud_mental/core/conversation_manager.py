"""
Gestor de conversaciones para el chatbot de salud mental
"""

import json
import datetime
from typing import List, Dict, Optional
from utils.config import UI_MESSAGES, LANGUAGE_CONFIG

class ConversationManager:
    """Gestiona el historial y contexto de conversaciones"""
    
    def __init__(self):
        self.conversation_history = []
        self.current_language = LANGUAGE_CONFIG['default_language']
        self.session_start = datetime.datetime.now()
        self.user_preferences = {}
    
    def add_message(self, message: str, sender: str, response_data: Dict = None):
        """
        Añade un mensaje al historial de conversación
        
        Args:
            message: El texto del mensaje
            sender: 'user' o 'bot'
            response_data: Datos adicionales sobre la respuesta (similitud, fuente, etc.)
        """
        message_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'sender': sender,
            'message': message,
            'language': self.current_language
        }
        
        if response_data:
            message_entry['response_data'] = response_data
        
        self.conversation_history.append(message_entry)
    
    def get_conversation_history(self, limit: int = None) -> List[Dict]:
        """
        Obtiene el historial de conversación
        
        Args:
            limit: Número máximo de mensajes a retornar
        """
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def get_recent_context(self, num_messages: int = 6) -> str:
        """
        Obtiene el contexto reciente de la conversación como texto
        """
        recent_messages = self.conversation_history[-num_messages:]
        context_parts = []
        
        for msg in recent_messages:
            sender_label = "Usuario" if msg['sender'] == 'user' else "Uli"
            context_parts.append(f"{sender_label}: {msg['message']}")
        
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
        self.session_start = datetime.datetime.now()
    
    def set_language(self, language: str):
        """Establece el idioma de la conversación"""
        if language in LANGUAGE_CONFIG['supported_languages']:
            self.current_language = language
    
    def get_welcome_message(self) -> str:
        """Obtiene el mensaje de bienvenida en el idioma actual"""
        return UI_MESSAGES[self.current_language]['welcome']
    
    def get_ui_message(self, key: str, **kwargs) -> str:
        """
        Obtiene un mensaje de la interfaz en el idioma actual
        
        Args:
            key: Clave del mensaje
            **kwargs: Parámetros para formatear el mensaje
        """
        message = UI_MESSAGES[self.current_language].get(key, key)
        if kwargs:
            try:
                return message.format(**kwargs)
            except:
                return message
        return message
    
    def save_conversation(self, file_path: str):
        """
        Guarda la conversación en un archivo JSON
        """
        conversation_data = {
            'session_start': self.session_start.isoformat(),
            'session_end': datetime.datetime.now().isoformat(),
            'language': self.current_language,
            'total_messages': len(self.conversation_history),
            'messages': self.conversation_history,
            'user_preferences': self.user_preferences
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando conversación: {e}")
            return False
    
    def load_conversation(self, file_path: str):
        """
        Carga una conversación desde un archivo JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            self.conversation_history = conversation_data.get('messages', [])
            self.current_language = conversation_data.get('language', LANGUAGE_CONFIG['default_language'])
            self.user_preferences = conversation_data.get('user_preferences', {})
            
            if 'session_start' in conversation_data:
                self.session_start = datetime.datetime.fromisoformat(conversation_data['session_start'])
            
            return True
        except Exception as e:
            print(f"Error cargando conversación: {e}")
            return False
    
    def get_conversation_stats(self) -> Dict:
        """
        Obtiene estadísticas de la conversación actual
        """
        if not self.conversation_history:
            return {}
        
        user_messages = [msg for msg in self.conversation_history if msg['sender'] == 'user']
        bot_messages = [msg for msg in self.conversation_history if msg['sender'] == 'bot']
        
        session_duration = datetime.datetime.now() - self.session_start
        
        stats = {
            'session_duration_minutes': session_duration.total_seconds() / 60,
            'total_messages': len(self.conversation_history),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'current_language': self.current_language,
            'session_start': self.session_start.isoformat(),
            'avg_response_confidence': 0
        }
        
        # Calcular confianza promedio de respuestas
        confidences = []
        for msg in bot_messages:
            if 'response_data' in msg and 'similarity_score' in msg['response_data']:
                confidences.append(msg['response_data']['similarity_score'])
        
        if confidences:
            stats['avg_response_confidence'] = sum(confidences) / len(confidences)
        
        return stats
    
    def suggest_follow_up_questions(self, last_response_data: Dict = None) -> List[str]:
        """
        Sugiere preguntas de seguimiento basadas en el contexto
        """
        suggestions = []
        
        # Sugerencias genéricas por idioma
        if self.current_language == 'es':
            generic_suggestions = [
                "¿Puedes darme más información sobre esto?",
                "¿Qué técnicas me recomiendas?",
                "¿Cómo puedo aplicar esto en mi vida diaria?",
                "¿Hay algo más que deba saber?"
            ]
        else:
            generic_suggestions = [
                "Can you give me more information about this?",
                "What techniques do you recommend?",
                "How can I apply this in my daily life?",
                "Is there anything else I should know?"
            ]
        
        # Si hay datos de respuesta, generar sugerencias más específicas
        if last_response_data and 'source' in last_response_data:
            if 'ansiedad' in str(last_response_data).lower() or 'anxiety' in str(last_response_data).lower():
                if self.current_language == 'es':
                    suggestions.extend([
                        "¿Cómo puedo manejar un ataque de ansiedad?",
                        "¿Qué ejercicios de respiración me ayudan?"
                    ])
                else:
                    suggestions.extend([
                        "How can I manage an anxiety attack?",
                        "What breathing exercises can help me?"
                    ])
            
            elif 'depresión' in str(last_response_data).lower() or 'depression' in str(last_response_data).lower():
                if self.current_language == 'es':
                    suggestions.extend([
                        "¿Cómo puedo mejorar mi estado de ánimo?",
                        "¿Qué actividades me pueden ayudar?"
                    ])
                else:
                    suggestions.extend([
                        "How can I improve my mood?",
                        "What activities can help me?"
                    ])
        
        # Combinar y limitar sugerencias
        all_suggestions = suggestions + generic_suggestions
        return all_suggestions[:4]  # Máximo 4 sugerencias
    
    def update_user_preferences(self, preferences: Dict):
        """
        Actualiza las preferencias del usuario
        """
        self.user_preferences.update(preferences)
    
    def get_personalized_greeting(self) -> str:
        """
        Obtiene un saludo personalizado basado en el historial
        """
        if not self.conversation_history:
            return self.get_welcome_message()
        
        # Si es una conversación continuada
        if self.current_language == 'es':
            return "¡Hola de nuevo! ¿En qué más puedo ayudarte?"
        else:
            return "Hello again! How else can I help you?"
