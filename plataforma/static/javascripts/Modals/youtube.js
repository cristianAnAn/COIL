document.addEventListener("DOMContentLoaded", function() {
    // Tu código aquí
    const youtubeUrlInput = document.querySelectorAll(".youtubeUrl");
    const iframe = document.querySelectorAll(".youtubeMedia");
    
    for (a in youtubeUrlInput){ 
        const youtubeUrl = youtubeUrlInput[a].value;
        // Extraer el ID del video
        const videoIdbyUrl = youtubeUrl.match(/v=([^&]+)/)[1];
        // Actualizar el atributo src del iframe
        iframe[a].src = `https://www.youtube.com/embed/${videoIdbyUrl}`;
    }

    
});



