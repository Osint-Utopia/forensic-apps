const preguntasRespuestas = [
    { pregunta: "¿Cómo saber si mi esposo(a) tiene problemas de adicción?", respuesta: "Si cambia mucho su humor, gasta dinero sin explicación o se aleja de ti, puede ser una señal." },
    { pregunta: "¿Qué hago si creo que mi hijo usa drogas?", respuesta: "Habla con él con calma y sin juzgar, pero busca ayuda profesional." },
    { pregunta: "¿Te gustaría saber cómo hablar con él o ella sobre esto?", respuesta: "Perfecto. Te proporciono el número donde te pueden dar la información necesaria: Llama al 3331962135, Psic. Tere Hernández." },
    { pregunta: "¿Te gustaría que te ayudemos a planear esa conversación?", respuesta: "Podemos apoyarte en hacer eso." },
    // Agrega más preguntas y respuestas aquí
];

function generarPreguntas() {
    const gridContainer = document.querySelector(".grid-container");
    gridContainer.innerHTML = ""; // Limpia el contenedor

    // Genera preguntas dinámicas
    preguntasRespuestas.sort(() => Math.random() - 0.5); // Mezclar preguntas
    preguntasRespuestas.slice(0, 10).forEach(({ pregunta, respuesta }, index) => {
        const gridItem = document.createElement("div");
        gridItem.classList.add("grid-item");
        gridItem.textContent = pregunta;

        gridItem.addEventListener("click", () => {
            gridItem.textContent = respuesta;
            setTimeout(() => mostrarPreguntaSeguimiento(gridItem, index), 5000);
        });

        gridContainer.appendChild(gridItem);
    });
}

function mostrarPreguntaSeguimiento(elemento, index) {
    elemento.innerHTML = `
        <p>¿Deseas más información personalizada?</p>
        <div class="buttons">
            <button class="yes" onclick="mostrarInformacion(${index})">Sí</button>
            <button class="no" onclick="mostrarGracias(${index})">No</button>
        </div>
    `;
}

function mostrarInformacion(index) {
    const rect = document.querySelectorAll(".grid-item")[index];
    rect.textContent = "Gracias por tu interés. Pronto recibirás más información.";
}

function mostrarGracias(index) {
    const rect = document.querySelectorAll(".grid-item")[index];
    rect.textContent = "Gracias. Para más preguntas, contacta al 3331962135.";
}

// Generar preguntas al cargar la página
document.addEventListener("DOMContentLoaded", ```javascript
generarPreguntas);