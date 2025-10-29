import React, { useState } from 'react';
import { Calendar, Plus, Edit2, Trash2, Eye, Users, Shield, Scale, BookOpen, AlertTriangle } from 'lucide-react';

const CalendarioContenido = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [showModal, setShowModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [newContent, setNewContent] = useState({
    title: '',
    type: 'educativo',
    service: 'legal',
    platform: 'linkedin',
    description: '',
    status: 'planificado'
  });

  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  const [contentData, setContentData] = useState({
    // Contenido pre-cargado como ejemplos
    '2025-9-25': [
      {
        id: 1,
        title: '¿Qué es la investigación OSINT?',
        type: 'educativo',
        service: 'legal',
        platform: 'linkedin',
        description: 'Post educativo sobre investigación en fuentes abiertas',
        status: 'planificado'
      }
    ],
    '2025-9-26': [
      {
        id: 2,
        title: 'Herramientas XIPHOS en acción',
        type: 'promocional',
        service: 'cyber',
        platform: 'instagram',
        description: 'Demo visual de nuestras herramientas',
        status: 'planificado'
      }
    ],
    '2025-9-28': [
      {
        id: 3,
        title: 'Caso de éxito: Falsificación documental',
        type: 'caso_estudio',
        service: 'legal',
        platform: 'blog',
        description: 'Historia de un caso real resuelto',
        status: 'borrador'
      }
    ]
  });

  const contentTypes = {
    educativo: { icon: BookOpen, color: 'bg-blue-500', label: 'Educativo' },
    promocional: { icon: Users, color: 'bg-green-500', label: 'Promocional' },
    caso_estudio: { icon: Eye, color: 'bg-purple-500', label: 'Caso de Estudio' },
    tips: { icon: AlertTriangle, color: 'bg-yellow-500', label: 'Tips/Consejos' }
  };

  const serviceTypes = {
    legal: { icon: Scale, color: 'text-blue-600', label: 'Legal Forense' },
    cyber: { icon: Shield, color: 'text-green-600', label: 'Ciberseguridad' }
  };

  const platforms = {
    linkedin: { label: 'LinkedIn', color: 'bg-blue-700' },
    instagram: { label: 'Instagram', color: 'bg-pink-500' },
    facebook: { label: 'Facebook', color: 'bg-blue-600' },
    whatsapp: { label: 'WhatsApp', color: 'bg-green-600' },
    blog: { label: 'Blog/Web', color: 'bg-gray-700' },
    youtube: { label: 'YouTube', color: 'bg-red-600' },
    email: { label: 'Email', color: 'bg-gray-600' }
  };

  const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month, 1).getDay();
  };

  const formatDate = (year, month, day) => {
    return `${year}-${month + 1}-${day}`;
  };

  const handleDateClick = (day) => {
    setSelectedDate(formatDate(currentYear, currentMonth, day));
    setShowModal(true);
  };

  const handleSaveContent = () => {
    if (!selectedDate || !newContent.title) return;

    const contentId = Date.now();
    const newContentItem = {
      ...newContent,
      id: contentId
    };

    setContentData(prev => ({
      ...prev,
      [selectedDate]: [...(prev[selectedDate] || []), newContentItem]
    }));

    setNewContent({
      title: '',
      type: 'educativo',
      service: 'legal',
      platform: 'linkedin',
      description: '',
      status: 'planificado'
    });
    setShowModal(false);
  };

  const deleteContent = (date, contentId) => {
    setContentData(prev => ({
      ...prev,
      [date]: prev[date].filter(item => item.id !== contentId)
    }));
  };

  const renderCalendarDays = () => {
    const daysInMonth = getDaysInMonth(currentMonth, currentYear);
    const firstDay = getFirstDayOfMonth(currentMonth, currentYear);
    const days = [];

    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="h-20 bg-gray-50"></div>);
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const dateKey = formatDate(currentYear, currentMonth, day);
      const dayContent = contentData[dateKey] || [];
      const isToday = new Date().toDateString() === new Date(currentYear, currentMonth, day).toDateString();

      days.push(
        <div
          key={day}
          className={`h-20 border border-gray-200 p-1 cursor-pointer hover:bg-gray-50 ${
            isToday ? 'bg-blue-50 border-blue-300' : ''
          }`}
          onClick={() => handleDateClick(day)}
        >
          <div className={`font-semibold text-sm mb-1 ${isToday ? 'text-blue-600' : ''}`}>
            {day}
          </div>
          <div className="space-y-1">
            {dayContent.slice(0, 2).map((content, index) => {
              const TypeIcon = contentTypes[content.type].icon;
              const ServiceIcon = serviceTypes[content.service].icon;
              return (
                <div
                  key={content.id}
                  className={`text-xs p-1 rounded ${contentTypes[content.type].color} text-white flex items-center gap-1`}
                >
                  <TypeIcon size={10} />
                  <ServiceIcon size={10} />
                  <span className="truncate">{content.title.substring(0, 15)}...</span>
                </div>
              );
            })}
            {dayContent.length > 2 && (
              <div className="text-xs text-gray-500">+{dayContent.length - 2} más</div>
            )}
          </div>
        </div>
      );
    }

    return days;
  };

  // Ideas de contenido predefinidas
  const contentIdeas = {
    legal: [
      'Análisis forense digital paso a paso',
      'Diferencias entre perito y abogado tradicional',
      'Casos de falsificación más comunes',
      'Investigación OSINT en casos legales',
      'Violencia de género: análisis objetivo',
      'Recuperación de datos eliminados'
    ],
    cyber: [
      'Demo de herramienta XIPHOS',
      'Vulnerabilidades más peligrosas 2024',
      'AKONTIA: rastreo avanzado explicado',
      'Falsos positivos vs amenazas reales',
      'Mapeo de superficie de ataque',
      'Ciberseguridad para pymes'
    ]
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Calendar className="text-blue-600" size={32} />
          <h1 className="text-3xl font-bold text-gray-800">Calendario de Contenido</h1>
        </div>
        <p className="text-gray-600">Planifica tu estrategia de contenido para Servicios Legales Forenses y Ciberseguridad</p>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => setCurrentMonth(prev => prev === 0 ? 11 : prev - 1)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          ← Anterior
        </button>
        <h2 className="text-2xl font-semibold text-gray-800">
          {months[currentMonth]} {currentYear}
        </h2>
        <button
          onClick={() => setCurrentMonth(prev => prev === 11 ? 0 : prev + 1)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          Siguiente →
        </button>
      </div>

      {/* Legend */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
        <div>
          <h4 className="font-semibold mb-2">Tipos de Contenido:</h4>
          {Object.entries(contentTypes).map(([key, type]) => {
            const Icon = type.icon;
            return (
              <div key={key} className="flex items-center gap-2 mb-1">
                <div className={`w-4 h-4 rounded ${type.color}`}></div>
                <Icon size={14} />
                <span className="text-sm">{type.label}</span>
              </div>
            );
          })}
        </div>
        <div>
          <h4 className="font-semibold mb-2">Servicios:</h4>
          {Object.entries(serviceTypes).map(([key, service]) => {
            const Icon = service.icon;
            return (
              <div key={key} className="flex items-center gap-2 mb-1">
                <Icon size={16} className={service.color} />
                <span className="text-sm">{service.label}</span>
              </div>
            );
          })}
        </div>
        <div>
          <h4 className="font-semibold mb-2">Plataformas:</h4>
          {Object.entries(platforms).slice(0, 3).map(([key, platform]) => (
            <div key={key} className="flex items-center gap-2 mb-1">
              <div className={`w-4 h-4 rounded ${platform.color}`}></div>
              <span className="text-sm">{platform.label}</span>
            </div>
          ))}
        </div>
        <div>
          <h4 className="font-semibold mb-2">Ideas Rápidas:</h4>
          <button 
            onClick={() => {
              const ideas = [...contentIdeas.legal, ...contentIdeas.cyber];
              const randomIdea = ideas[Math.floor(Math.random() * ideas.length)];
              setNewContent(prev => ({...prev, title: randomIdea}));
              setShowModal(true);
            }}
            className="px-3 py-1 bg-yellow-500 text-white rounded text-sm hover:bg-yellow-600 transition-colors"
          >
            💡 Generar Idea
          </button>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-6">
        <div className="grid grid-cols-7 bg-gray-100">
          {['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'].map(day => (
            <div key={day} className="p-3 text-center font-semibold text-gray-700">
              {day}
            </div>
          ))}
        </div>
        <div className="grid grid-cols-7">
          {renderCalendarDays()}
        </div>
      </div>

      {/* Content Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 p-6 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">Contenido Legal</h3>
          <p className="text-2xl font-bold text-blue-600">
            {Object.values(contentData).flat().filter(c => c.service === 'legal').length}
          </p>
          <p className="text-sm text-blue-600">Posts planificados</p>
        </div>
        <div className="bg-green-50 p-6 rounded-lg">
          <h3 className="font-semibold text-green-800 mb-2">Contenido Cyber</h3>
          <p className="text-2xl font-bold text-green-600">
            {Object.values(contentData).flat().filter(c => c.service === 'cyber').length}
          </p>
          <p className="text-sm text-green-600">Posts planificados</p>
        </div>
        <div className="bg-purple-50 p-6 rounded-lg">
          <h3 className="font-semibold text-purple-800 mb-2">Total del Mes</h3>
          <p className="text-2xl font-bold text-purple-600">
            {Object.values(contentData).flat().length}
          </p>
          <p className="text-sm text-purple-600">Posts planificados</p>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">
              Agregar Contenido - {selectedDate}
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Título</label>
                <input
                  type="text"
                  value={newContent.title}
                  onChange={(e) => setNewContent({...newContent, title: e.target.value})}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Título del contenido"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Tipo</label>
                  <select
                    value={newContent.type}
                    onChange={(e) => setNewContent({...newContent, type: e.target.value})}
                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  >
                    {Object.entries(contentTypes).map(([key, type]) => (
                      <option key={key} value={key}>{type.label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Servicio</label>
                  <select
                    value={newContent.service}
                    onChange={(e) => setNewContent({...newContent, service: e.target.value})}
                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  >
                    {Object.entries(serviceTypes).map(([key, service]) => (
                      <option key={key} value={key}>{service.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Plataforma</label>
                <select
                  value={newContent.platform}
                  onChange={(e) => setNewContent({...newContent, platform: e.target.value})}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                >
                  {Object.entries(platforms).map(([key, platform]) => (
                    <option key={key} value={key}>{platform.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Descripción</label>
                <textarea
                  value={newContent.description}
                  onChange={(e) => setNewContent({...newContent, description: e.target.value})}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Descripción breve del contenido"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleSaveContent}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                Guardar
              </button>
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Selected Date Content */}
      {selectedDate && contentData[selectedDate] && (
        <div className="mt-6 bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Contenido para {selectedDate}:</h4>
          <div className="space-y-2">
            {contentData[selectedDate].map(content => (
              <div key={content.id} className="flex items-center justify-between bg-white p-3 rounded">
                <div className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded ${contentTypes[content.type].color}`}></div>
                  <div>
                    <div className="font-medium">{content.title}</div>
                    <div className="text-sm text-gray-600">
                      {serviceTypes[content.service].label} • {platforms[content.platform].label}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => deleteContent(selectedDate, content.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CalendarioContenido;