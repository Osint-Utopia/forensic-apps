"""
Widget de chat para el chatbot de salud mental
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import List, Dict, Callable

class ChatWidget(ttk.Frame):
    """Widget de chat conversacional"""
    
    def __init__(self, parent, on_message_callback: Callable = None):
        super().__init__(parent)
        self.on_message_callback = on_message_callback
        self.setup_ui()
        self.is_thinking = False
    
    def setup_ui(self):
        """Configura la interfaz del widget de chat"""
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Área de chat (ScrolledText)
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=('Arial', 10),
            state=tk.DISABLED,
            bg='#f8f9fa',
            fg='#212529'
        )
        self.chat_area.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Configurar tags para diferentes tipos de mensajes
        self.chat_area.tag_configure("user", foreground="#0066cc", font=('Arial', 10, 'bold'))
        self.chat_area.tag_configure("bot", foreground="#28a745", font=('Arial', 10, 'bold'))
        self.chat_area.tag_configure("system", foreground="#6c757d", font=('Arial', 9, 'italic'))
        self.chat_area.tag_configure("confidence", foreground="#ffc107", font=('Arial', 8))
        
        # Frame para entrada de texto
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Entrada de texto
        self.message_entry = tk.Text(
            input_frame,
            height=3,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='white',
            fg='#212529'
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Bind Enter para enviar mensaje
        self.message_entry.bind('<Control-Return>', self.send_message)
        self.message_entry.bind('<KeyRelease>', self.on_text_change)
        
        # Frame para botones
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1, sticky="ns")
        
        # Botón enviar
        self.send_button = ttk.Button(
            button_frame,
            text="Enviar",
            command=self.send_message,
            width=10
        )
        self.send_button.pack(pady=(0, 5))
        
        # Botón limpiar
        self.clear_button = ttk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_chat,
            width=10
        )
        self.clear_button.pack()
        
        # Placeholder en el área de entrada
        self.set_placeholder()
    
    def set_placeholder(self):
        """Establece el texto placeholder en la entrada"""
        self.message_entry.insert("1.0", "Escribe tu pregunta aquí...")
        self.message_entry.configure(fg='#6c757d')
        self.message_entry.bind('<FocusIn>', self.clear_placeholder)
    
    def clear_placeholder(self, event=None):
        """Limpia el placeholder cuando el usuario hace clic"""
        if self.message_entry.get("1.0", "end-1c") == "Escribe tu pregunta aquí...":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.configure(fg='#212529')
        self.message_entry.unbind('<FocusIn>')
    
    def on_text_change(self, event=None):
        """Maneja cambios en el texto de entrada"""
        text = self.message_entry.get("1.0", "end-1c").strip()
        self.send_button.configure(state="normal" if text and not self.is_thinking else "disabled")
    
    def send_message(self, event=None):
        """Envía un mensaje"""
        message = self.message_entry.get("1.0", "end-1c").strip()
        
        if not message or message == "Escribe tu pregunta aquí...":
            return
        
        if self.is_thinking:
            return
        
        # Limpiar entrada
        self.message_entry.delete("1.0", tk.END)
        self.send_button.configure(state="disabled")
        
        # Mostrar mensaje del usuario
        self.add_message(message, "user")
        
        # Mostrar indicador de "pensando"
        self.show_thinking()
        
        # Llamar callback en un hilo separado
        if self.on_message_callback:
            threading.Thread(
                target=self._process_message_async,
                args=(message,),
                daemon=True
            ).start()
    
    def _process_message_async(self, message: str):
        """Procesa el mensaje de forma asíncrona"""
        try:
            response_data = self.on_message_callback(message)
            self.after(0, self._handle_response, response_data)
        except Exception as e:
            self.after(0, self._handle_error, str(e))
    
    def _handle_response(self, response_data: Dict):
        """Maneja la respuesta del chatbot"""
        self.hide_thinking()
        
        if response_data and 'answer' in response_data:
            self.add_message(response_data['answer'], "bot", response_data)
        else:
            self.add_message("Lo siento, no pude encontrar una respuesta adecuada.", "bot")
    
    def _handle_error(self, error_message: str):
        """Maneja errores en el procesamiento"""
        self.hide_thinking()
        self.add_message(f"Error: {error_message}", "system")
    
    def add_message(self, message: str, sender: str, response_data: Dict = None):
        """
        Añade un mensaje al área de chat
        
        Args:
            message: Texto del mensaje
            sender: 'user', 'bot', o 'system'
            response_data: Datos adicionales de la respuesta
        """
        self.chat_area.configure(state=tk.NORMAL)
        
        # Añadir timestamp y etiqueta del remitente
        if sender == "user":
            self.chat_area.insert(tk.END, "Tú: ", "user")
        elif sender == "bot":
            self.chat_area.insert(tk.END, "Uli: ", "bot")
        else:
            self.chat_area.insert(tk.END, "Sistema: ", "system")
        
        # Añadir mensaje
        self.chat_area.insert(tk.END, message + "\n")
        
        # Añadir información de confianza si está disponible
        if response_data and 'similarity_score' in response_data:
            confidence = response_data['similarity_score']
            confidence_text = f"(Confianza: {confidence:.1%})\n"
            self.chat_area.insert(tk.END, confidence_text, "confidence")
        
        self.chat_area.insert(tk.END, "\n")
        
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def show_thinking(self):
        """Muestra el indicador de 'pensando'"""
        self.is_thinking = True
        self.thinking_message = "Uli está pensando..."
        
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "Uli: ", "bot")
        self.thinking_start = self.chat_area.index(tk.INSERT)
        self.chat_area.insert(tk.END, self.thinking_message + "\n\n")
        self.thinking_end = self.chat_area.index(tk.INSERT)
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
        # Animación de puntos
        self._animate_thinking()
    
    def _animate_thinking(self):
        """Anima el indicador de pensando"""
        if not self.is_thinking:
            return
        
        dots = [".", "..", "...", ""]
        current_dots = getattr(self, '_thinking_dots', 0)
        
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.delete(self.thinking_start, self.thinking_end)
        
        thinking_text = f"Uli está pensando{dots[current_dots]}\n\n"
        self.chat_area.insert(self.thinking_start, thinking_text)
        self.thinking_end = self.chat_area.index(tk.INSERT)
        
        self.chat_area.configure(state=tk.DISABLED)
        
        self._thinking_dots = (current_dots + 1) % len(dots)
        
        if self.is_thinking:
            self.after(500, self._animate_thinking)
    
    def hide_thinking(self):
        """Oculta el indicador de 'pensando'"""
        if not self.is_thinking:
            return
        
        self.is_thinking = False
        
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.delete(self.thinking_start, self.thinking_end)
        self.chat_area.configure(state=tk.DISABLED)
        
        self.send_button.configure(state="normal")
    
    def clear_chat(self):
        """Limpia el área de chat"""
        result = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que quieres limpiar el chat?"
        )
        
        if result:
            self.chat_area.configure(state=tk.NORMAL)
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.configure(state=tk.DISABLED)
    
    def set_language(self, language: str):
        """Cambia el idioma de la interfaz"""
        if language == 'en':
            self.send_button.configure(text="Send")
            self.clear_button.configure(text="Clear")
            placeholder = "Type your question here..."
        else:
            self.send_button.configure(text="Enviar")
            self.clear_button.configure(text="Limpiar")
            placeholder = "Escribe tu pregunta aquí..."
        
        # Actualizar placeholder si está activo
        current_text = self.message_entry.get("1.0", "end-1c")
        if current_text in ["Escribe tu pregunta aquí...", "Type your question here..."]:
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.insert("1.0", placeholder)
            self.message_entry.configure(fg='#6c757d')
    
    def get_chat_history(self) -> str:
        """Obtiene el historial del chat como texto"""
        return self.chat_area.get("1.0", tk.END)
