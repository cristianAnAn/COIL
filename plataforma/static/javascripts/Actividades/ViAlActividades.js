document.getElementById("toggleSeccionComentarioClase").addEventListener("click", function(event) {
    event.preventDefault();
    var seccionComentarioClase = document.getElementById("seccionComentarioClase");
    seccionComentarioClase.style.display = seccionComentarioClase.style.display === "none" ? "block" : "none";
});

document.getElementById("enlaceComentarioPrivado").addEventListener("click", function(event) {
    event.preventDefault();
    var cajaComentarioPrivado = document.getElementById("cajaComentarioPrivado");
    cajaComentarioPrivado.style.display = cajaComentarioPrivado.style.display === "none" ? "block" : "none";
});

document.getElementById("botonEnviarComentarioPrivado").addEventListener("click", function(event) {
    event.preventDefault();
    var comentarioPrivado = document.getElementById("entradaComentarioPrivado").value;
    if (comentarioPrivado.trim() !== "") {
        var seccionComentarioPrivado = document.getElementById("seccionComentarioPrivado");
        var nuevoComentario = document.createElement("p");
        nuevoComentario.textContent = comentarioPrivado;
        seccionComentarioPrivado.appendChild(nuevoComentario);
        document.getElementById("entradaComentarioPrivado").value = "";
    }
});

document.getElementById("botonAgregarArchivo").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("entradaArchivo").click();
});

document.getElementById("entradaArchivo").addEventListener("change", function(event) {
    var archivo = event.target.files[0];
    if (archivo) {
        var archivoAdjunto = document.getElementById("archivoAdjunto");
        archivoAdjunto.innerHTML = "Archivo adjunto: " + archivo.name;
    }
});

document.getElementById("botonEntregar").addEventListener("click", function(event) {
    event.preventDefault();
    var archivoAdjunto = document.getElementById("archivoAdjunto").textContent;
    if (archivoAdjunto) {
        alert("Entrega realizada con el archivo: " + archivoAdjunto);
    } else {
        alert("No se ha adjuntado ningún archivo.");
    }
});

document.getElementById("botonAnularEntrega").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("archivoAdjunto").innerHTML = "";
    alert("Entrega anulada.");
});