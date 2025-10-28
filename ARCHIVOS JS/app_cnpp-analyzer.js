        options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Análisis de Elementos CNPP por Calidad',
                            font: {
                                size: 16,
                                weight: 'bold'
                            }
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Elementos CNPP'
                            }
                        },
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Porcentaje de Cumplimiento'
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        }

        // Función para exportar resultados a PDF
        function exportToPDF() {
            const content = document.getElementById('resultsSection');
            const printWindow = window.open('', '_blank');
            
            printWindow.document.write(`
                <html>
                <head>
                    <title>Análisis CNPP - Reporte Ejecutivo</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        h1, h2 { color: #2c3e50; }
                        .summary-item { margin: 10px 0; padding: 10px; border-left: 4px solid #3498db; }
                        .present { background-color: #d4edda; border-left-color: #28a745; }
                        .partial { background-color: #fff3cd; border-left-color: #ffc107; }
                        .missing { background-color: #f8d7da; border-left-color: #dc3545; }
                        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                        @media print { .no-print { display: none; } }
                    </style>
                </head>
                <body>
                    <h1>Análisis de Carpeta de Investigación CNPP</h1>
                    <h2>Fecha de Análisis: ${new Date().toLocaleDateString('es-MX')}</h2>
                    ${document.getElementById('summaryContent').innerHTML}
                    ${document.getElementById('checklistContent').innerHTML}
                    <h2>Marco Legal Aplicable</h2>
                    ${document.getElementById('legalContent').innerHTML}
                </body>
                </html>
            `);
            
            printWindow.document.close();
            printWindow.print();
        }

        // Función para exportar resultados a HTML
        function exportToHTML() {
            const htmlContent = `
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Análisis CNPP - Reporte Completo</title>
                    <style>
                        body { 
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            margin: 0; 
                            padding: 20px; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            min-height: 100vh;
                        }
                        .container { 
                            max-width: 1200px; 
                            margin: 0 auto; 
                            background: white; 
                            border-radius: 15px; 
                            padding: 30px; 
                            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        }
                        h1, h2 { color: #2c3e50; margin-bottom: 20px; }
                        h1 { border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
                        .summary-card { padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                        .present { background: linear-gradient(135deg, #d4edda, #c3e6cb); border-left: 5px solid #28a745; }
                        .partial { background: linear-gradient(135deg, #fff3cd, #ffeaa7); border-left: 5px solid #ffc107; }
                        .missing { background: linear-gradient(135deg, #f8d7da, #f5c6cb); border-left: 5px solid #dc3545; }
                        table { width: 100%; border-collapse: collapse; margin: 20px 0; border-radius: 8px; overflow: hidden; }
                        th { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px; }
                        td { padding: 12px; border-bottom: 1px solid #eee; }
                        tr:nth-child(even) { background-color: #f8f9fa; }
                        .score-display { font-size: 2em; font-weight: bold; text-align: center; margin: 20px 0; }
                        .recommendations { background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Análisis Completo de Carpeta de Investigación CNPP</h1>
                        <p><strong>Fecha de Análisis:</strong> ${new Date().toLocaleDateString('es-MX', { 
                            year: 'numeric', 
                            month: 'long', 
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}</p>
                        <p><strong>Archivos Analizados:</strong> ${uploadedFiles.length}</p>
                        
                        <h2>Resumen Ejecutivo</h2>
                        ${document.getElementById('summaryContent').innerHTML}
                        
                        <h2>Lista de Verificación CNPP</h2>
                        ${document.getElementById('checklistContent').innerHTML}
                        
                        <h2>Análisis Detallado</h2>
                        ${document.getElementById('detailedContent').innerHTML}
                        
                        <h2>Marco Legal Aplicable</h2>
                        ${document.getElementById('legalContent').innerHTML}
                        
                        <div class="recommendations">
                            <h3>Recomendaciones para Mejora</h3>
                            <p>Este análisis se basa en los elementos mínimos requeridos por el Art. 131 y demás disposiciones del CNPP. 
                            Se recomienda revisar los elementos marcados como faltantes o parciales para completar la integración de la carpeta.</p>
                        </div>
                    </div>
                </body>
                </html>
            `;
            
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analisis_cnpp_${new Date().toISOString().split('T')[0]}.html`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        // Función para exportar resultados a JSON
        function exportToJSON() {
            const analysisData = {
                metadata: {
                    fechaAnalisis: new Date().toISOString(),
                    archivosAnalizados: uploadedFiles.length,
                    nombreArchivos: uploadedFiles.map(f => f.name),
                    version: "1.0",
                    sistema: "Analizador CNPP"
                },
                resultados: {
                    puntajeGeneral: globalAnalysisResults.overallScore || 0,
                    nivelJudicializacion: globalAnalysisResults.judicializationLevel || "No determinado",
                    elementosPresentes: globalAnalysisResults.presentElements || 0,
                    elementosParciales: globalAnalysisResults.partialElements || 0,
                    elementosFaltantes: globalAnalysisResults.missingElements || 0
                },
                elementos: globalAnalysisResults.elements || {},
                documentosAnalizados: globalAnalysisResults.documents || [],
                recomendaciones: generateRecommendations(),
                marcoLegal: {
                    articuloPrincipal: "Artículo 131 CNPP",
                    articulosRelacionados: [
                        "Art. 212 - Deber de investigación penal",
                        "Art. 213 - Objeto de la investigación", 
                        "Art. 217 - Registro de los actos de investigación",
                        "Art. 227 - Cadena de custodia",
                        "Art. 360-387 - Medios de prueba"
                    ]
                },
                cumplimientoNormativo: calculateNormativeCompliance()
            };
            
            const blob = new Blob([JSON.stringify(analysisData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analisis_cnpp_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        // Función para generar recomendaciones específicas
        function generateRecommendations() {
            const recommendations = [];
            
            if (!globalAnalysisResults.elements) return recommendations;
            
            Object.keys(globalAnalysisResults.elements).forEach(key => {
                const element = globalAnalysisResults.elements[key];
                if (element.status === 'missing') {
                    recommendations.push({
                        elemento: element.name,
                        prioridad: element.weight > 8 ? 'Alta' : element.weight > 5 ? 'Media' : 'Baja',
                        accion: `Integrar ${element.name} a la carpeta de investigación`,
                        fundamentoLegal: element.legalBasis || 'Art. 131 CNPP',
                        impacto: element.weight > 8 ? 'Crítico para judicialización' : 'Necesario para completar integración'
                    });
                } else if (element.status === 'partial') {
                    recommendations.push({
                        elemento: element.name,
                        prioridad: 'Media',
                        accion: `Completar y mejorar la calidad de ${element.name}`,
                        fundamentoLegal: element.legalBasis || 'Art. 131 CNPP',
                        impacto: 'Mejora la solidez probatoria del caso'
                    });
                }
            });
            
            return recommendations;
        }

        // Función para calcular cumplimiento normativo
        function calculateNormativeCompliance() {
            if (!globalAnalysisResults.elements) return {};
            
            const compliance = {
                investigacion: 0,
                mediosPrueba: 0,
                cadenasCustodia: 0,
                procedimiento: 0
            };
            
            // Clasificar elementos por categoría normativa
            Object.keys(globalAnalysisResults.elements).forEach(key => {
                const element = globalAnalysisResults.elements[key];
                const score = element.status === 'present' ? 100 : element.status === 'partial' ? 50 : 0;
                
                if (['denuncia', 'entrevistas', 'declaraciones'].includes(key)) {
                    compliance.investigacion += score / 3;
                } else if (['dictamenes', 'testimonios', 'documentales'].includes(key)) {
                    compliance.mediosPrueba += score / 3;
                } else if (['cadenasCustodia', 'aseguramientos'].includes(key)) {
                    compliance.cadenasCustodia += score / 2;
                } else {
                    compliance.procedimiento += score / 4;
                }
            });
            
            return compliance;
        }

        // Función para imprimir resumen ejecutivo
        function printExecutiveSummary() {
            const printContent = `
                <html>
                <head>
                    <title>Resumen Ejecutivo - Análisis CNPP</title>
                    <style>
                        @page { margin: 2cm; }
                        body { font-family: Arial, sans-serif; line-height: 1.6; }
                        .header { text-align: center; border-bottom: 2px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px; }
                        .score-box { background: #f8f9fa; border: 2px solid #dee2e6; padding: 20px; text-align: center; margin: 20px 0; }
                        .recommendations { background: #e8f4f8; padding: 15px; border-left: 4px solid #17a2b8; }
                        .element-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }
                        .present { color: #28a745; font-weight: bold; }
                        .partial { color: #ffc107; font-weight: bold; }
                        .missing { color: #dc3545; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>RESUMEN EJECUTIVO</h1>
                        <h2>Análisis de Carpeta de Investigación CNPP</h2>
                        <p>Fecha: ${new Date().toLocaleDateString('es-MX')}</p>
                    </div>
                    
                    <div class="score-box">
                        <h3>Puntaje General: ${globalAnalysisResults.overallScore || 0}%</h3>
                        <p><strong>Nivel de Judicialización:</strong> ${globalAnalysisResults.judicializationLevel || 'No determinado'}</p>
                    </div>
                    
                    ${document.getElementById('summaryContent').innerHTML}
                    
                    <div class="recommendations">
                        <h3>Acciones Prioritarias</h3>
                        <ul>
                            <li>Revisar elementos marcados como faltantes</li>
                            <li>Completar documentación parcial</li>
                            <li>Verificar cumplimiento de cadenas de custodia</li>
                            <li>Actualizar registro de actos de investigación</li>
                        </ul>
                    </div>
                    
                    <p style="margin-top: 40px; font-size: 0.9em; color: #666;">
                        <strong>Nota:</strong> Este análisis se basa en los elementos mínimos establecidos en el Art. 131 CNPP y demás disposiciones aplicables. 
                        Se recomienda revisión por personal jurídico especializado antes de la judicialización.
                    </p>
                </body>
                </html>
            `;
            
            const printWindow = window.open('', '_blank');
            printWindow.document.write(printContent);
            printWindow.document.close();
            printWindow.print();
        }

        // Función para mostrar ayuda contextual
        function showHelp(topic) {
            const helpContent = {
                upload: "Arrastre archivos o haga clic para seleccionar. Se aceptan PDF, DOC, DOCX y TXT relacionados con la carpeta de investigación.",
                analysis: "El análisis evalúa automáticamente los elementos requeridos por el Art. 131 CNPP y genera un puntaje de viabilidad para judicialización.",
                results: "Los resultados se organizan en pestañas: Resumen Ejecutivo, Lista de Verificación, Análisis Detallado y Marco Legal.",
                export: "Puede exportar los resultados en formato PDF (para impresión), HTML (archivo web), JSON (datos estructurados) o imprimir el resumen ejecutivo."
            };
            
            if (helpContent[topic]) {
                alert(helpContent[topic]);
            }
        }

        // Función para reiniciar el análisis
        function resetAnalysis() {
            if (confirm('¿Está seguro de que desea reiniciar el análisis? Se perderán todos los datos actuales.')) {
                uploadedFiles = [];
                globalAnalysisResults = {};
                
                // Limpiar interface
                document.getElementById('fileList').innerHTML = '';
                document.getElementById('debugFileList').innerHTML = '';
                document.getElementById('analyzeBtn').disabled = true;
                document.getElementById('resultsSection').style.display = 'none';
                
                // Resetear progreso
                updateProgress(0);
                
                // Limpiar gráfico si existe
                if (window.cnppChart) {
                    window.cnppChart.destroy();
                }
                
                console.log('Análisis reiniciado exitosamente');
            }
        }

        // Función para validar integridad de archivos
        function validateFileIntegrity(file) {
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const content = e.target.result;
                    const validation = {
                        isValid: true,
                        size: file.size,
                        type: file.type,
                        readable: content && content.length > 0,
                        encoding: 'UTF-8'
                    };
                    
                    // Validaciones adicionales según tipo de archivo
                    if (file.type === 'application/pdf') {
                        validation.isPDF = content.startsWith('%PDF');
                    } else if (file.type.includes('word')) {
                        validation.isWord = content.includes('word/') || content.includes('Microsoft');
                    }
                    
                    resolve(validation);
                };
                reader.onerror = () => resolve({ isValid: false, error: 'No se pudo leer el archivo' });
                reader.readAsText(file);
            });
        }

        // Inicialización de eventos adicionales
        document.addEventListener('DOMContentLoaded', function() {
            // Configurar tooltips
            const tooltipElements = document.querySelectorAll('[data-tooltip]');
            tooltipElements.forEach(element => {
                element.addEventListener('mouseenter', function() {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'tooltip';
                    tooltip.textContent = this.getAttribute('data-tooltip');
                    tooltip.style.cssText = `
                        position: absolute;
                        background: rgba(0,0,0,0.8);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-size: 12px;
                        z-index: 1000;
                        pointer-events: none;
                        white-space: nowrap;
                    `;
                    document.body.appendChild(tooltip);
                    
                    const rect = this.getBoundingClientRect();
                    tooltip.style.left = rect.left + 'px';
                    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
                    
                    this._tooltip = tooltip;
                });
                
                element.addEventListener('mouseleave', function() {
                    if (this._tooltip) {
                        document.body.removeChild(this._tooltip);
                        this._tooltip = null;
                    }
                });
            });

            // Configurar atajos de teclado
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    switch(e.key) {
                        case 'o':
                            e.preventDefault();
                            document.getElementById('fileInput').click();
                            break;
                        case 's':
                            e.preventDefault();
                            if (globalAnalysisResults.overallScore !== undefined) {
                                exportToJSON();
                            }
                            break;
                        case 'p':
                            e.preventDefault();
                            if (globalAnalysisResults.overallScore !== undefined) {
                                printExecutiveSummary();
                            }
                            break;
                    }
                }
            });

            console.log('Sistema de Análisis CNPP inicializado correctamente');
            console.log('Versión: 1.0 | Fecha: ' + new Date().toISOString());
        });