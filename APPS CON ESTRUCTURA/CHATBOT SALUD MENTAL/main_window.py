"""
Ventana principal del chatbot de salud mental
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from ui.chat_widget import ChatWidget
from core import DatasetProcessor, SemanticSearchEngine, ConversationManager
from utils.config import APP_CONFIG, UI_MESSAGES

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_components()
        self.setup_ui()
        self.initialize_chatbot()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['window_size'])
        self.root.minsize(*APP_CONFIG['min_window_size'])
        
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Centrar ventana
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_components(self):
        """Inicializa los componentes del chatbot"""
        self.dataset_processor = DatasetProcessor()
        self.search_engine = SemanticSearchEngine()
        self.conversation_manager = ConversationManager()
        self.is_initialized = False
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Barra de menú
        self.setup_menu()
        
        # Barra de herramientas
        self.setup_toolbar()
        
        # Widget de chat principal
        self.chat_widget = ChatWidget(
            self.root,
            on_message_callback=self.handle_user_message
        )
        self.chat_widget.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Barra de estado
        self.setup_status_bar()
    
    def setup_menu(self):
        """Configura la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Guardar conversación", command=self.save_conversation)
        file_menu.add_command(label="Cargar conversación", command=self.load_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar chat", command=self.export_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Limpiar chat", command=self.clear_chat)
        edit_menu.add_command(label="Configuraciones", command=self.show_settings)
        
        # Menú Idioma
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Idioma", menu=language_menu)
        language_menu.add_command(label="Español", command=lambda: self.change_language('es'))
        language_menu.add_command(label="English", command=lambda: self.change_language('en'))
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        help_menu.add_command(label="Estadísticas", command=self.show_statistics)
    
    def setup_toolbar(self):
        """Configura la barra de herramientas"""
        toolbar = ttk.Frame(self.root)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Botón de estado de conexión
        self.status_label = ttk.Label(toolbar, text="Inicializando...", foreground="orange")
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Selector de idioma
        ttk.Label(toolbar, text="Idioma:").pack(side=tk.LEFT, padx=(0, 5))
        self.language_var = tk.StringVar(value="es")
        language_combo = ttk.Combobox(
            toolbar,
            textvariable=self.language_var,
            values=["es", "en"],
            state="readonly",
            width=5
        )
        language_combo.pack(side=tk.LEFT, padx=(0, 10))
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Indicador de confianza
        ttk.Label(toolbar, text="Última confianza:").pack(side=tk.LEFT, padx=(10, 5))
        self.confidence_label = ttk.Label(toolbar, text="N/A", foreground="blue")
        self.confidence_label.pack(side=tk.LEFT)
    
    def setup_status_bar(self):
        """Configura la barra de estado"""
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        
        self.status_text = ttk.Label(status_frame, text="Listo", relief=tk.SUNKEN)
        self.status_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Contador de mensajes
        self.message_count_label = ttk.Label(status_frame, text="Mensajes: 0")
        self.message_count_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    def initialize_chatbot(self):
        """Inicializa el chatbot cargando los datasets"""
        def init_async():
            try:
                self.update_status("Cargando datasets...")
                
                # Cargar datasets
                conversations = self.dataset_processor.load_all_datasets()
                
                if not conversations:
                    raise Exception("No se pudieron cargar los datasets")
                
                self.update_status("Entrenando motor de búsqueda...")
                
                # Entrenar motor de búsqueda
                self.search_engine.train(conversations)
                
                self.update_status("Listo")
                self.status_label.configure(text="Conectado", foreground="green")
                self.is_initialized = True
                
                # Mostrar mensaje de bienvenida
                welcome_msg = self.conversation_manager.get_welcome_message()
                self.chat_widget.add_message(welcome_msg, "bot")
                
            except Exception as e:
                error_msg = f"Error inicializando: {e}"
                self.update_status(error_msg)
                self.status_label.configure(text="Error", foreground="red")
                messagebox.showerror("Error", error_msg)
        
        # Ejecutar inicialización en hilo separado
        import threading
        threading.Thread(target=init_async, daemon=True).start()
    
    def handle_user_message(self, message: str) -> dict:
        """
        Maneja un mensaje del usuario y retorna la respuesta del chatbot
        """
        if not self.is_initialized:
            return {
                'answer': 'El sistema aún se está inicializando. Por favor, espera un momento.',
                'similarity_score': 0.0
            }
        
        try:
            # Añadir mensaje al historial
            self.conversation_manager.add_message(message, 'user')
            
            # Buscar respuesta
            current_language = self.conversation_manager.current_language
            results = self.search_engine.search(message, language=current_language, max_results=1)
            
            if results:
                best_result = results[0]
                response_data = {
                    'answer': best_result['answer'],
                    'similarity_score': best_result['similarity_score'],
                    'source': best_result['source'],
                    'language': best_result['language']
                }
                
                # Añadir respuesta al historial
                self.conversation_manager.add_message(best_result['answer'], 'bot', response_data)
                
                # Actualizar indicadores
                self.confidence_label.configure(text=f"{best_result['similarity_score']:.1%}")
                self.update_message_count()
                
                return response_data
            else:
                # No se encontraron resultados
                no_results_msg = self.conversation_manager.get_ui_message('no_results')
                response_data = {
                    'answer': no_results_msg,
                    'similarity_score': 0.0
                }
                
                self.conversation_manager.add_message(no_results_msg, 'bot', response_data)
                self.update_message_count()
                
                return response_data
                
        except Exception as e:
            error_msg = f"Error procesando mensaje: {e}"
            self.update_status(error_msg)
            return {
                'answer': self.conversation_manager.get_ui_message('error'),
                'similarity_score': 0.0
            }
    
    def update_status(self, message: str):
        """Actualiza la barra de estado"""
        self.status_text.configure(text=message)
        self.root.update_idletasks()
    
    def update_message_count(self):
        """Actualiza el contador de mensajes"""
        count = len(self.conversation_manager.conversation_history)
        self.message_count_label.configure(text=f"Mensajes: {count}")
    
    def on_language_change(self, event=None):
        """Maneja el cambio de idioma"""
        new_language = self.language_var.get()
        self.change_language(new_language)
    
    def change_language(self, language: str):
        """Cambia el idioma de la aplicación"""
        self.conversation_manager.set_language(language)
        self.chat_widget.set_language(language)
        self.language_var.set(language)
        
        # Actualizar textos de la interfaz
        if language == 'en':
            self.root.title("Mental Health Chatbot - Uli")
        else:
            self.root.title("Chatbot de Salud Mental - Uli")
    
    def clear_chat(self):
        """Limpia el chat y reinicia la conversación"""
        self.conversation_manager.clear_history()
        self.chat_widget.clear_chat()
        
        # Mostrar nuevo mensaje de bienvenida
        welcome_msg = self.conversation_manager.get_welcome_message()
        self.chat_widget.add_message(welcome_msg, "bot")
        
        self.update_message_count()
    
    def save_conversation(self):
        """Guarda la conversación actual"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.conversation_manager.save_conversation(file_path):
                messagebox.showinfo("Éxito", "Conversación guardada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo guardar la conversación")
    
    def load_conversation(self):
        """Carga una conversación guardada"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.conversation_manager.load_conversation(file_path):
                # Reconstruir chat en la interfaz
                self.chat_widget.clear_chat()
                
                for msg in self.conversation_manager.conversation_history:
                    sender = msg['sender']
                    message = msg['message']
                    response_data = msg.get('response_data')
                    
                    self.chat_widget.add_message(message, sender, response_data)
                
                self.update_message_count()
                messagebox.showinfo("Éxito", "Conversación cargada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo cargar la conversación")
    
    def export_chat(self):
        """Exporta el chat como archivo de texto"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                chat_history = self.chat_widget.get_chat_history()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(chat_history)
                messagebox.showinfo("Éxito", "Chat exportado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el chat: {e}")
    
    def show_settings(self):
        """Muestra la ventana de configuraciones"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configuraciones")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Configuraciones básicas
        ttk.Label(settings_window, text="Configuraciones del Chatbot", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Umbral de confianza
        ttk.Label(settings_window, text="Umbral mínimo de confianza:").pack(pady=5)
        confidence_var = tk.DoubleVar(value=0.1)
        confidence_scale = ttk.Scale(
            settings_window,
            from_=0.0,
            to=1.0,
            variable=confidence_var,
            orient=tk.HORIZONTAL
        )
        confidence_scale.pack(pady=5, padx=20, fill=tk.X)
        
        # Número máximo de resultados
        ttk.Label(settings_window, text="Máximo número de resultados:").pack(pady=5)
        results_var = tk.IntVar(value=5)
        results_spinbox = ttk.Spinbox(
            settings_window,
            from_=1,
            to=10,
            textvariable=results_var,
            width=10
        )
        results_spinbox.pack(pady=5)
        
        # Botones
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Aplicar", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_statistics(self):
        """Muestra estadísticas del chatbot"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas")
        stats_window.geometry("500x400")
        stats_window.transient(self.root)
        
        # Obtener estadísticas
        dataset_stats = self.dataset_processor.get_statistics()
        conversation_stats = self.conversation_manager.get_conversation_stats()
        
        # Crear texto con estadísticas
        stats_text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats_content = f"""
ESTADÍSTICAS DEL CHATBOT DE SALUD MENTAL

=== DATASETS ===
Total de conversaciones: {dataset_stats.get('total_conversations', 0)}
Conversaciones en español: {dataset_stats.get('spanish_conversations', 0)}
Conversaciones en inglés: {dataset_stats.get('english_conversations', 0)}
Datasets cargados: {', '.join(dataset_stats.get('loaded_datasets', []))}
Longitud promedio de preguntas: {dataset_stats.get('avg_question_length', 0):.1f} palabras
Longitud promedio de respuestas: {dataset_stats.get('avg_answer_length', 0):.1f} palabras

=== SESIÓN ACTUAL ===
Duración de sesión: {conversation_stats.get('session_duration_minutes', 0):.1f} minutos
Total de mensajes: {conversation_stats.get('total_messages', 0)}
Mensajes del usuario: {conversation_stats.get('user_messages', 0)}
Respuestas del bot: {conversation_stats.get('bot_messages', 0)}
Idioma actual: {conversation_stats.get('current_language', 'N/A')}
Confianza promedio: {conversation_stats.get('avg_response_confidence', 0):.1%}

=== MOTOR DE BÚSQUEDA ===
Estado: {'Entrenado' if self.search_engine.is_trained else 'No entrenado'}
Idiomas disponibles: {', '.join(self.search_engine.vectorizers.keys())}
"""
        
        # Añadir estadísticas de vocabulario por idioma
        for lang in self.search_engine.vectorizers.keys():
            vocab_stats = self.search_engine.get_vocabulary_stats(lang)
            stats_content += f"\nVocabulario {lang}: {vocab_stats.get('vocabulary_size', 0)} términos"
        
        stats_text.insert(tk.END, stats_content)
        stats_text.configure(state=tk.DISABLED)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = f"""
{APP_CONFIG['title']}
Versión {APP_CONFIG['version']}

Un chatbot inteligente para apoyo en salud mental que utiliza
técnicas de procesamiento de lenguaje natural y búsqueda semántica
para proporcionar respuestas relevantes y útiles.

Características:
• Búsqueda semántica avanzada
• Soporte multiidioma (Español/Inglés)
• Interfaz conversacional intuitiva
• Historial de conversaciones
• Exportación de datos

Desarrollado con Python, tkinter, scikit-learn y NLTK.
        """
        
        messagebox.showinfo("Acerca de", about_text)
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
