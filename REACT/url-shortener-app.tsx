import React, { useState } from 'react';
import { Link, Copy, Check, Scissors } from 'lucide-react';

export default function URLShortener() {
  const [inputUrls, setInputUrls] = useState('');
  const [shortenedUrls, setShortenedUrls] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);

  // Función para generar código basado en las primeras 3 letras de palabras significativas
  const generateLawCode = (url) => {
    try {
      // Extraer el nombre de la ley de la URL
      const urlParts = url.split('/');
      const lawName = urlParts[urlParts.length - 1];
      
      // Palabras vacías a eliminar
      const stopWords = [
        'A', 'AL', 'ANTE', 'BAJO', 'CON', 'CONTRA', 'DE', 'DEL', 'DESDE', 'DURANTE', 
        'EN', 'ENTRE', 'HACIA', 'HASTA', 'MEDIANTE', 'PARA', 'POR', 'SEGÚN', 'SIN', 
        'SO', 'SOBRE', 'TRAS', 'VERSUS', 'VÍA', 'Y', 'E', 'NI', 'O', 'U', 'PERO',
        'MAS', 'AUNQUE', 'SINO', 'SIQUIERA', 'LA', 'LAS', 'EL', 'LOS', 'UN', 'UNA',
        'UNOS', 'UNAS', 'QUE', 'QUIEN', 'QUIENES', 'CUAL', 'CUALES', 'CUYO', 'CUYA',
        'CUYOS', 'CUYAS', 'APARTADO', 'ARTÍCULO', 'FRACCIÓN', 'INCISO', 'PÁRRAFO',
        'CONSTITUCIÓN', 'POLÍTICA', 'ESTADOS', 'UNIDOS', 'MEXICANOS'
      ];
      
      // Limpiar y procesar el nombre
      const cleanName = lawName
        .replace(/-/g, ' ')
        .replace(/,/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .toUpperCase();

      // Dividir en palabras y filtrar palabras vacías
      const words = cleanName.split(' ').filter(word => 
        word.length > 0 && !stopWords.includes(word)
      );
      
      // Tomar las primeras 3 letras de cada palabra significativa
      const codeParts = words.map(word => word.substring(0, 3));
      
      // Unir con guiones
      return codeParts.join('-');
      
    } catch (error) {
      return 'LEY-SIN-NOM';
    }
  };

  // Función para validar si una URL es válida
  const isValidUrl = (string) => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  // Función para extraer el título de la ley
  const extractLawTitle = (url) => {
    try {
      const urlParts = url.split('/');
      const lawName = urlParts[urlParts.length - 1];
      return lawName.replace(/-/g, ' ').replace(/\s+/g, ' ').trim();
    } catch (error) {
      return 'Ley sin título';
    }
  };

  // Función para procesar las URLs
  const processUrls = async () => {
    if (!inputUrls.trim()) return;

    setIsProcessing(true);
    
    // Dividir las URLs por líneas y filtrar las vacías
    const urlList = inputUrls.split('\n').filter(url => url.trim());
    
    // Simular el procesamiento
    const processed = urlList.map(url => {
      const trimmedUrl = url.trim();
      if (isValidUrl(trimmedUrl)) {
        const lawCode = generateLawCode(trimmedUrl);
        const lawTitle = extractLawTitle(trimmedUrl);
        return {
          original: trimmedUrl,
          shortened: `https://short.ly/lic_azua/${lawCode}`,
          lawTitle: lawTitle,
          lawCode: lawCode,
          status: 'success'
        };
      } else {
        return {
          original: trimmedUrl,
          shortened: null,
          lawTitle: null,
          lawCode: null,
          status: 'error'
        };
      }
    });

    // Simular delay de procesamiento
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setShortenedUrls(processed);
    setIsProcessing(false);
  };

  // Función para copiar URL individual
  const copyUrl = async (url, index) => {
    try {
      await navigator.clipboard.writeText(url);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  // Función para copiar todas las URLs acortadas
  const copyAllShortened = async () => {
    const successfulUrls = shortenedUrls
      .filter(item => item.status === 'success')
      .map(item => item.shortened)
      .join('\n');
    
    try {
      await navigator.clipboard.writeText(successfulUrls);
      setCopiedIndex('all');
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Error al copiar todas las URLs:', err);
    }
  };

  const clearAll = () => {
    setInputUrls('');
    setShortenedUrls([]);
    setCopiedIndex(null);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white min-h-screen">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-2 mb-4">
          <Scissors className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Acortador de URLs</h1>
        </div>
        <p className="text-gray-600">Acorta múltiples URLs de una vez para facilitar tu trabajo</p>
      </div>

      {/* Input Section */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Pega tus URLs aquí (una por línea):
        </label>
        <textarea
          value={inputUrls}
          onChange={(e) => setInputUrls(e.target.value)}
          placeholder="https://levime.com.mx/documento/ver/105/LEY-ORGÁNICA-DEL-TRIBUNAL-FEDERAL-DE-JUSTICIA-ADMINISTRATIVA&#10;https://levime.com.mx/documento/ver/106/LEY-REGLAMENTARIA-DE-LA-FRACCIÓN-XIII-BIS&#10;https://levime.com.mx/documento/ver/107/LEY-REGLAMENTARIA-DE-LAS-FRACCIONES-I-Y-II"
          className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
        <div className="flex gap-3 mt-4">
          <button
            onClick={processUrls}
            disabled={isProcessing || !inputUrls.trim()}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <Link className="w-4 h-4" />
            {isProcessing ? 'Procesando...' : 'Acortar URLs'}
          </button>
          <button
            onClick={clearAll}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Limpiar
          </button>
        </div>
      </div>

      {/* Results Section */}
      {shortenedUrls.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Resultados ({shortenedUrls.filter(url => url.status === 'success').length} exitosas)
            </h2>
            <button
              onClick={copyAllShortened}
              className="flex items-center gap-2 px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm"
            >
              {copiedIndex === 'all' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              Copiar todas
            </button>
          </div>

          <div className="space-y-4">
            {shortenedUrls.map((item, index) => (
              <div key={index} className="bg-white rounded-lg p-4 border border-gray-200">
                {item.status === 'success' ? (
                  <div>
                    <div className="mb-2">
                      <span className="text-xs font-medium text-gray-500 uppercase">Original:</span>
                      <p className="text-sm text-gray-600 break-all">{item.original}</p>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <span className="text-xs font-medium text-green-600 uppercase">Acortada:</span>
                        <p className="text-sm font-mono text-blue-600 break-all">{item.shortened}</p>
                      </div>
                      <button
                        onClick={() => copyUrl(item.shortened, index)}
                        className="ml-3 p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
                        title="Copiar URL"
                      >
                        {copiedIndex === index ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-medium text-red-600 uppercase">Error:</span>
                      <span className="text-xs text-red-600">URL inválida</span>
                    </div>
                    <p className="text-sm text-gray-600 break-all">{item.original}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info Section */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-sm font-medium text-blue-900 mb-2">💡 Sistema de codificación:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• <strong>Formato:</strong> https://short.ly/lic_azua/LEY-REG-FRA-ART-105</li>
          <li>• <strong>Método:</strong> Primeras 3 letras de cada palabra significativa</li>
          <li>• <strong>Filtros:</strong> Elimina palabras vacías (DE, LA, EL, Y, etc.)</li>
          <li>• <strong>Identificación:</strong> Incluye tu apellido para rastrear el origen</li>
          <li>• <strong>Resultado:</strong> URL corta pero completamente identificable</li>
        </ul>
      </div>
    </div>
  );
}