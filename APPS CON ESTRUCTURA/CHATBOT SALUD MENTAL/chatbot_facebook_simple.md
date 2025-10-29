# Chatbot Facebook - Arquitectura Simple (HTML/JS/CSS)

## 🎯 **Diseño Específico para tu Equipo**

### ✅ **Tecnologías Familiares:**
- **HTML5** - Estructura conocida
- **CSS3** - Estilos modernos pero simples  
- **JavaScript ES6** - Sin frameworks, vanilla JS
- **Flask** - Python backend simple
- **Socket.IO** - WebSockets fáciles

### 🏗️ **Estructura del Proyecto:**

```
chatbot_facebook/
├── frontend/                    # Archivos estáticos
│   ├── index.html              # Página principal del chat
│   ├── embed.html              # Versión para iframe/embed
│   ├── css/
│   │   ├── style.css           # Estilos principales
│   │   ├── chat.css            # Estilos específicos del chat
│   │   └── responsive.css      # Responsive design
│   ├── js/
│   │   ├── chat.js             # Lógica principal del chat
│   │   ├── websocket.js        # Manejo de WebSockets
│   │   └── facebook.js         # Integración con Facebook
│   ├── assets/
│   │   ├── images/             # Iconos, avatares
│   │   └── sounds/             # Sonidos de notificación
│   └── manifest.json           # PWA manifest (opcional)
├── backend/                     # Python Flask
│   ├── app.py                  # Aplicación principal Flask
│   ├── hf_model.py             # Modelo Hugging Face
│   ├── facebook_webhook.py     # Webhook para Facebook
│   ├── chat_manager.py         # Gestión de conversaciones
│   ├── config.py               # Configuraciones
│   └── requirements.txt        # Dependencias Python
├── deploy/                      # Scripts de deployment
│   ├── nginx.conf              # Configuración Nginx
│   ├── supervisor.conf         # Supervisor para procesos
│   └── deploy.sh               # Script de deployment
└── docs/                       # Documentación
    ├── setup.md                # Guía de instalación
    ├── facebook_integration.md # Integración con Facebook
    └── customization.md        # Personalización
```

## 💻 **Frontend - HTML/CSS/JS Vanilla**

### 1. **HTML Principal (index.html)**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asistente de Salud Mental</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/chat.css">
    <link rel="stylesheet" href="css/responsive.css">
</head>
<body>
    <div class="chat-container">
        <!-- Header -->
        <div class="chat-header">
            <div class="avatar">
                <img src="assets/images/bot-avatar.png" alt="Asistente">
            </div>
            <div class="header-info">
                <h3>Asistente de Salud Mental</h3>
                <span class="status" id="connection-status">Conectando...</span>
            </div>
            <div class="header-actions">
                <button id="minimize-btn" class="btn-icon">−</button>
                <button id="close-btn" class="btn-icon">×</button>
            </div>
        </div>

        <!-- Messages Area -->
        <div class="chat-messages" id="chat-messages">
            <div class="message bot-message">
                <div class="message-avatar">
                    <img src="assets/images/bot-avatar.png" alt="Bot">
                </div>
                <div class="message-content">
                    <p>¡Hola! Soy tu asistente de salud mental. ¿En qué puedo ayudarte hoy?</p>
                    <span class="message-time">Ahora</span>
                </div>
            </div>
        </div>

        <!-- Typing Indicator -->
        <div class="typing-indicator" id="typing-indicator" style="display: none;">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span>El asistente está escribiendo...</span>
        </div>

        <!-- Input Area -->
        <div class="chat-input">
            <div class="input-container">
                <textarea 
                    id="message-input" 
                    placeholder="Escribe tu mensaje aquí..."
                    rows="1"
                    maxlength="500"
                ></textarea>
                <button id="send-btn" class="send-button">
                    <svg width="24" height="24" viewBox="0 0 24 24">
                        <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/>
                    </svg>
                </button>
            </div>
            <div class="input-footer">
                <span class="char-count">0/500</span>
                <span class="powered-by">Powered by AI</span>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <script src="js/websocket.js"></script>
    <script src="js/chat.js"></script>
</body>
</html>
```

### 2. **CSS Moderno pero Simple (css/chat.css)**
```css
/* Variables CSS para fácil personalización */
:root {
    --primary-color: #1877f2;
    --secondary-color: #42a5f5;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --error-color: #f44336;
    --text-primary: #1c1e21;
    --text-secondary: #65676b;
    --background-light: #f0f2f5;
    --background-white: #ffffff;
    --border-color: #dadde1;
    --shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
    --border-radius: 8px;
}

/* Chat Container */
.chat-container {
    width: 100%;
    max-width: 400px;
    height: 600px;
    background: var(--background-white);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header */
.chat-header {
    background: var(--primary-color);
    color: white;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

.header-info {
    flex: 1;
}

.header-info h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.status {
    font-size: 12px;
    opacity: 0.8;
}

.status.connected {
    color: var(--success-color);
}

.status.disconnected {
    color: var(--error-color);
}

/* Messages */
.chat-messages {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    background: var(--background-light);
}

.message {
    display: flex;
    margin-bottom: 16px;
    animation: fadeInUp 0.3s ease;
}

.message-avatar img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

.message-content {
    max-width: 70%;
    margin-left: 8px;
}

.user-message {
    flex-direction: row-reverse;
}

.user-message .message-content {
    margin-left: 0;
    margin-right: 8px;
    text-align: right;
}

.message-content p {
    background: var(--background-white);
    padding: 12px 16px;
    border-radius: 18px;
    margin: 0;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    line-height: 1.4;
}

.user-message .message-content p {
    background: var(--primary-color);
    color: white;
}

.message-time {
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 4px;
    display: block;
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    color: var(--text-secondary);
    font-size: 14px;
}

.typing-dots {
    display: flex;
    gap: 4px;
    margin-right: 8px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    background: var(--text-secondary);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

/* Input Area */
.chat-input {
    background: var(--background-white);
    border-top: 1px solid var(--border-color);
    padding: 16px;
}

.input-container {
    display: flex;
    align-items: flex-end;
    gap: 8px;
}

#message-input {
    flex: 1;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 12px 16px;
    resize: none;
    font-family: inherit;
    font-size: 14px;
    line-height: 1.4;
    max-height: 100px;
    outline: none;
    transition: border-color 0.2s;
}

#message-input:focus {
    border-color: var(--primary-color);
}

.send-button {
    width: 40px;
    height: 40px;
    border: none;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
}

.send-button:hover {
    background: var(--secondary-color);
}

.send-button:disabled {
    background: var(--border-color);
    cursor: not-allowed;
}

.input-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 12px;
    color: var(--text-secondary);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
    }
    30% {
        transform: translateY(-10px);
    }
}

/* Scrollbar personalizado */
.chat-messages::-webkit-scrollbar {
    width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
    background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}
```

### 3. **JavaScript Vanilla (js/chat.js)**
```javascript
class ChatBot {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-btn');
        this.messagesContainer = document.getElementById('chat-messages');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.connectionStatus = document.getElementById('connection-status');
        this.charCount = document.querySelector('.char-count');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.setupAutoResize();
    }
    
    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character count
        this.messageInput.addEventListener('input', () => {
            const length = this.messageInput.value.length;
            this.charCount.textContent = `${length}/500`;
            
            if (length > 450) {
                this.charCount.style.color = 'var(--warning-color)';
            } else if (length > 480) {
                this.charCount.style.color = 'var(--error-color)';
            } else {
                this.charCount.style.color = 'var(--text-secondary)';
            }
        });
        
        // Minimize/Close buttons
        document.getElementById('minimize-btn')?.addEventListener('click', () => {
            this.minimize();
        });
        
        document.getElementById('close-btn')?.addEventListener('click', () => {
            this.close();
        });
    }
    
    connectWebSocket() {
        try {
            this.socket = io('ws://localhost:5000', {
                transports: ['websocket', 'polling']
            });
            
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.updateConnectionStatus('Conectado', 'connected');
                console.log('Conectado al servidor');
            });
            
            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.updateConnectionStatus('Desconectado', 'disconnected');
                console.log('Desconectado del servidor');
            });
            
            this.socket.on('bot_response', (data) => {
                this.hideTypingIndicator();
                this.addMessage(data.message, 'bot');
            });
            
            this.socket.on('error', (error) => {
                console.error('Error de WebSocket:', error);
                this.updateConnectionStatus('Error de conexión', 'disconnected');
            });
            
        } catch (error) {
            console.error('Error conectando WebSocket:', error);
            this.updateConnectionStatus('Error de conexión', 'disconnected');
        }
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || !this.isConnected) {
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.charCount.textContent = '0/500';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Send to server
        this.socket.emit('user_message', {
            message: message,
            timestamp: new Date().toISOString()
        });
    }
    
    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        const avatar = document.createElement('img');
        avatar.src = type === 'bot' ? 'assets/images/bot-avatar.png' : 'assets/images/user-avatar.png';
        avatar.alt = type === 'bot' ? 'Bot' : 'Usuario';
        avatarDiv.appendChild(avatar);
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const messageP = document.createElement('p');
        messageP.textContent = content;
        
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = this.formatTime(new Date());
        
        contentDiv.appendChild(messageP);
        contentDiv.appendChild(timeSpan);
        
        if (type === 'user') {
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatarDiv);
        } else {
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(contentDiv);
        }
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    updateConnectionStatus(text, className) {
        this.connectionStatus.textContent = text;
        this.connectionStatus.className = `status ${className}`;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    formatTime(date) {
        return date.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    setupAutoResize() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 100) + 'px';
        });
    }
    
    minimize() {
        // Implementar lógica de minimizar
        console.log('Minimizar chat');
    }
    
    close() {
        // Implementar lógica de cerrar
        if (confirm('¿Estás seguro de que quieres cerrar el chat?')) {
            if (this.socket) {
                this.socket.disconnect();
            }
            // Ocultar o cerrar el widget
            console.log('Cerrar chat');
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.chatBot = new ChatBot();
});

// Funciones globales para integración con Facebook
window.ChatBotAPI = {
    sendMessage: (message) => {
        if (window.chatBot && window.chatBot.isConnected) {
            window.chatBot.addMessage(message, 'user');
            window.chatBot.socket.emit('user_message', { message });
        }
    },
    
    isConnected: () => {
        return window.chatBot ? window.chatBot.isConnected : false;
    },
    
    minimize: () => {
        if (window.chatBot) {
            window.chatBot.minimize();
        }
    },
    
    close: () => {
        if (window.chatBot) {
            window.chatBot.close();
        }
    }
};
```

## 🐍 **Backend Flask Simple**

### 1. **Aplicación Principal (app.py)**
```python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import logging
from datetime import datetime
from hf_model import HuggingFaceModel
from chat_manager import ChatManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask y SocketIO
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializar componentes
hf_model = HuggingFaceModel()
chat_manager = ChatManager()

@app.route('/')
def index():
    """Página principal del chat"""
    return render_template('index.html')

@app.route('/embed')
def embed():
    """Versión embebida para iframe"""
    return render_template('embed.html')

@app.route('/health')
def health():
    """Endpoint de salud para monitoreo"""
    return {
        'status': 'ok',
        'model_loaded': hf_model.is_loaded(),
        'timestamp': datetime.now().isoformat()
    }

@socketio.on('connect')
def handle_connect():
    """Maneja nuevas conexiones WebSocket"""
    logger.info(f"Cliente conectado: {request.sid}")
    emit('connection_status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Maneja desconexiones WebSocket"""
    logger.info(f"Cliente desconectado: {request.sid}")
    chat_manager.close_session(request.sid)

@socketio.on('user_message')
def handle_user_message(data):
    """Procesa mensajes del usuario"""
    try:
        user_message = data.get('message', '').strip()
        session_id = request.sid
        
        if not user_message:
            return
        
        logger.info(f"Mensaje recibido de {session_id}: {user_message}")
        
        # Guardar mensaje del usuario
        chat_manager.add_message(session_id, 'user', user_message)
        
        # Obtener historial de conversación
        history = chat_manager.get_conversation_history(session_id)
        
        # Generar respuesta con el modelo
        bot_response = hf_model.generate_response(user_message, history)
        
        # Guardar respuesta del bot
        chat_manager.add_message(session_id, 'assistant', bot_response)
        
        # Enviar respuesta al cliente
        emit('bot_response', {
            'message': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Respuesta enviada a {session_id}")
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        emit('bot_response', {
            'message': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    logger.info("Iniciando servidor...")
    
    # Cargar modelo en background
    logger.info("Cargando modelo de Hugging Face...")
    hf_model.load_model()
    
    # Iniciar servidor
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

## 📱 **Integración con Facebook**

### 1. **Webhook para Facebook Messenger (facebook_webhook.py)**
```python
from flask import Blueprint, request, jsonify
import hmac
import hashlib
import requests
from config import FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_VERIFY_TOKEN

facebook_bp = Blueprint('facebook', __name__)

@facebook_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificación del webhook de Facebook"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == FACEBOOK_VERIFY_TOKEN:
        return challenge
    else:
        return 'Error de verificación', 403

@facebook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Maneja mensajes entrantes de Facebook"""
    data = request.get_json()
    
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    handle_facebook_message(messaging_event)
    
    return 'OK', 200

def handle_facebook_message(messaging_event):
    """Procesa mensaje de Facebook Messenger"""
    sender_id = messaging_event['sender']['id']
    message_text = messaging_event['message'].get('text', '')
    
    if message_text:
        # Generar respuesta con el modelo
        response = hf_model.generate_response(message_text)
        
        # Enviar respuesta a Facebook
        send_facebook_message(sender_id, response)

def send_facebook_message(recipient_id, message_text):
    """Envía mensaje a Facebook Messenger"""
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={FACEBOOK_PAGE_ACCESS_TOKEN}"
    
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    
    response = requests.post(url, json=data)
    return response.json()
```

## 🚀 **Ventajas de esta Arquitectura:**

1. **✅ Familiar para tu equipo**: HTML, CSS, JS que ya conocen
2. **✅ Fácil mantenimiento**: Código simple y directo
3. **✅ Integración Facebook**: Webhook listo para Messenger
4. **✅ Responsive**: Funciona en móviles y desktop
5. **✅ Escalable**: Fácil agregar funcionalidades
6. **✅ Sin build tools**: No webpack, no compilación compleja

¿Te parece bien esta aproximación? ¿Empiezo a implementar mientras terminas con el .parquet?
