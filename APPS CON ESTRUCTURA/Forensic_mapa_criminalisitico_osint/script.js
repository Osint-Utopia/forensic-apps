
let mapa = L.map('map').setView([23.6345, -102.5528], 5); // Centro de México

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(mapa);

let puntos = JSON.parse(localStorage.getItem("casos") || "[]");

function mostrarPuntos() {
    puntos.forEach(p => {
        L.marker([p.lat, p.lon]).addTo(mapa)
            .bindPopup(`<strong>${p.nombre}</strong><br>${p.fecha}<br>${p.descripcion}`);
    });
}

function agregarPunto() {
    let nombre = document.getElementById("nombre").value;
    let fecha = document.getElementById("fecha").value;
    let lat = parseFloat(document.getElementById("lat").value);
    let lon = parseFloat(document.getElementById("lon").value);
    let descripcion = document.getElementById("descripcion").value;

    if (!nombre || isNaN(lat) || isNaN(lon)) {
        alert("Nombre y coordenadas válidas son requeridas.");
        return;
    }

    let punto = { nombre, fecha, lat, lon, descripcion };
    puntos.push(punto);
    localStorage.setItem("casos", JSON.stringify(puntos));
    location.reload();
}

function exportarJSON() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(puntos, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "casos_exportados.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
}

mostrarPuntos();
