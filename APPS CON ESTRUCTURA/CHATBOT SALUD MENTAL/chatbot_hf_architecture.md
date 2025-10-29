# Arquitectura Chatbot con Modelo Hugging Face

## 🏗️ Diseño del Sistema

### Stack Tecnológico Propuesto

#### Opción A: Aplicación Web Moderna
```
Frontend:
├── React 18 + TypeScript
├── Tailwind CSS + Shadcn/ui
├── Socket.io (tiempo real)
└── Vite (build tool)

Backend:
├── FastAPI + Python 3.11
├── WebSockets para chat en tiempo real
├── Transformers + PEFT
├── SQLite/PostgreSQL
└── Redis (cache opcional)

Deployment:
├── Docker containers
├── Nginx (reverse proxy)
└── Cloud deployment ready
```

#### Opción B: Aplicación Desktop Híbrida
```
Frontend:
├── Electron + React
├── Tailwind CSS
└── IPC communication

Backend:
├── Python subprocess
├── Transformers + PEFT
├── Local SQLite
└── File-based cache
```

## 🤖 Integración del Modelo

### Modelo: zementalist/llama-3-8B-chat-psychotherapist

**Características:**
- **Tamaño**: 4.65B parámetros
- **Tipo**: PEFT (Parameter Efficient Fine-Tuning)
- **Especialización**: Salud mental y psicoterapia
- **Licencia**: MIT (uso libre)

### Implementación Técnica

```python
# core/hf_model_manager.py
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch

class HuggingFaceModelManager:
    def __init__(self, model_id="zementalist/llama-3-8B-chat-psychotherapist"):
        self.model_id = model_id
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_model(self):
        """Carga el modelo PEFT optimizado"""
        config = PeftConfig.from_pretrained(self.model_id)
        
        # Cargar modelo base
        base_model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
        
        # Aplicar adaptadores PEFT
        self.model = PeftModel.from_pretrained(base_model, self.model_id)
        
        # Cargar tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
        
        return True
    
    def generate_response(self, user_message: str, conversation_history: list = None):
        """Genera respuesta usando el modelo"""
        messages = [
            {"role": "system", "content": "Eres un asistente especializado en salud mental. Proporciona apoyo empático y profesional."},
            {"role": "user", "content": user_message}
        ]
        
        # Agregar historial si existe
        if conversation_history:
            messages = conversation_history + messages[-1:]
        
        # Aplicar template de chat
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generar respuesta
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decodificar respuesta
        response = outputs[0][input_ids.shape[-1]:]
        decoded_response = self.tokenizer.decode(response, skip_special_tokens=True)
        
        return decoded_response.strip()
```

## 🌐 Arquitectura Web (Opción A)

### Estructura del Proyecto
```
chatbot_hf_web/
├── frontend/                 # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── TypingIndicator.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── useChat.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── core/
│   │   │   ├── hf_model_manager.py
│   │   │   ├── conversation_manager.py
│   │   │   └── config.py
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   └── websocket.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### API Endpoints

```python
# backend/app/api/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.hf_model_manager import HuggingFaceModelManager
from app.core.conversation_manager import ConversationManager

router = APIRouter()
model_manager = HuggingFaceModelManager()
conversation_manager = ConversationManager()

@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    try:
        while True:
            # Recibir mensaje del usuario
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            
            # Obtener historial de conversación
            history = conversation_manager.get_history(session_id)
            
            # Generar respuesta con el modelo
            response = model_manager.generate_response(user_message, history)
            
            # Guardar en historial
            conversation_manager.add_message(session_id, "user", user_message)
            conversation_manager.add_message(session_id, "assistant", response)
            
            # Enviar respuesta
            await websocket.send_json({
                "type": "response",
                "message": response,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        conversation_manager.close_session(session_id)
```

### Frontend React

```tsx
// frontend/src/components/ChatInterface.tsx
import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  const { sendMessage, lastMessage, connectionStatus } = useWebSocket();
  
  useEffect(() => {
    if (lastMessage) {
      const data = JSON.parse(lastMessage.data);
      if (data.type === 'response') {
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          type: 'assistant',
          content: data.message,
          timestamp: data.timestamp
        }]);
        setIsTyping(false);
      }
    }
  }, [lastMessage]);
  
  const handleSendMessage = () => {
    if (inputValue.trim()) {
      // Agregar mensaje del usuario
      const userMessage = {
        id: Date.now().toString(),
        type: 'user' as const,
        content: inputValue,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, userMessage]);
      setIsTyping(true);
      
      // Enviar al backend
      sendMessage({ message: inputValue });
      setInputValue('');
    }
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4">
        <h1 className="text-xl font-semibold">Asistente de Salud Mental</h1>
        <p className="text-blue-100">
          Estado: {connectionStatus === 'Open' ? 'Conectado' : 'Desconectado'}
        </p>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isTyping && <TypingIndicator />}
      </div>
      
      {/* Input */}
      <div className="border-t bg-white p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Escribe tu mensaje..."
            className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || connectionStatus !== 'Open'}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>
  );
};
```

## 🖥️ Arquitectura Desktop (Opción B)

### Estructura del Proyecto
```
chatbot_hf_desktop/
├── electron/                 # Electron main process
│   ├── main.js
│   ├── preload.js
│   └── package.json
├── frontend/                 # React renderer
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   └── package.json
├── backend/                  # Python backend
│   ├── main.py
│   ├── hf_model_manager.py
│   └── requirements.txt
├── build/                    # Build scripts
│   ├── build.js
│   └── package.py
└── dist/                     # Distribution files
```

### Comunicación IPC

```javascript
// electron/main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');

let pythonProcess;

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  
  // Iniciar proceso Python
  pythonProcess = spawn('python', ['backend/main.py']);
  
  mainWindow.loadFile('frontend/dist/index.html');
}

ipcMain.handle('send-message', async (event, message) => {
  return new Promise((resolve) => {
    // Comunicación con Python backend
    pythonProcess.stdin.write(JSON.stringify({ message }) + '\n');
    
    pythonProcess.stdout.once('data', (data) => {
      const response = JSON.parse(data.toString());
      resolve(response);
    });
  });
});
```

## ⚡ Optimizaciones de Rendimiento

### 1. Carga Lazy del Modelo
```python
class LazyModelManager:
    def __init__(self):
        self._model = None
        self._tokenizer = None
    
    @property
    def model(self):
        if self._model is None:
            self._load_model()
        return self._model
    
    def _load_model(self):
        # Carga el modelo solo cuando se necesita
        pass
```

### 2. Cache de Respuestas
```python
import hashlib
import json
from functools import lru_cache

class ResponseCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
    
    def get_cache_key(self, message: str, context: list = None):
        content = message + str(context or [])
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, message: str, context: list = None):
        key = self.get_cache_key(message, context)
        return self.cache.get(key)
    
    def set(self, message: str, response: str, context: list = None):
        key = self.get_cache_key(message, context)
        if len(self.cache) >= self.max_size:
            # Eliminar entrada más antigua
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = response
```

### 3. Cuantización del Modelo
```python
from transformers import BitsAndBytesConfig

# Configuración para 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
```

## 📊 Comparación de Opciones

| Característica | Web App | Desktop App |
|----------------|---------|-------------|
| **Accesibilidad** | ✅ Cualquier navegador | ❌ Instalación requerida |
| **Rendimiento** | ⚠️ Depende de servidor | ✅ Local, más rápido |
| **Escalabilidad** | ✅ Múltiples usuarios | ❌ Un usuario por instalación |
| **Mantenimiento** | ✅ Actualizaciones centralizadas | ❌ Actualizaciones manuales |
| **Recursos** | ✅ Servidor compartido | ❌ Recursos locales |
| **Privacidad** | ⚠️ Datos en servidor | ✅ Todo local |
| **Distribución** | ✅ URL simple | ❌ Ejecutables por OS |

## 🚀 Plan de Implementación

### Fase 1: Preparación (1-2 días)
1. ✅ Análisis del modelo HF completado
2. 🔄 Corrección del dataset JSON (en progreso)
3. ⏳ Decisión de arquitectura (web vs desktop)

### Fase 2: Desarrollo Core (3-5 días)
1. Implementar HuggingFaceModelManager
2. Crear sistema de conversaciones
3. Desarrollar API/IPC según arquitectura elegida

### Fase 3: Frontend (2-3 días)
1. Diseñar interfaz moderna
2. Implementar chat en tiempo real
3. Agregar funcionalidades avanzadas

### Fase 4: Integración y Testing (1-2 días)
1. Pruebas de rendimiento
2. Optimizaciones
3. Documentación

## 🎯 Próximos Pasos

1. **Decidir arquitectura**: ¿Web o Desktop?
2. **Configurar entorno**: Instalar dependencias HF
3. **Implementar modelo manager**: Código base para el modelo
4. **Crear interfaz básica**: Chat funcional mínimo

¿Qué arquitectura prefieres para empezar?
