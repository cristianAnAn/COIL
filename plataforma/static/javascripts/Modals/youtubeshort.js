function extractVideoIdFromYouTubeUrl(url) {
    videoId= url.match(/youtu\.be\/([a-zA-Z0-9_-]+)/i)[1];
    return videoId;
}
document.addEventListener("DOMContentLoaded", function() {
    //*Forma con youtu.be
    const youtubeUrlInputShort = document.querySelectorAll(".youtubeShort");
    const iframeShort = document.querySelectorAll(".youtubeMediaShort");
    for (c in youtubeUrlInputShort){ 
        const youtubeUrlShort = youtubeUrlInputShort[c].value;
        // Extraer el ID del video
        const videoId = extractVideoIdFromYouTubeUrl(youtubeUrlShort);
        console.log("Video ID:", videoId);
        // Actualizar el atributo src del iframe
        iframeShort[c].src = `https://www.youtube.com/embed/${videoId}`;
    }
});