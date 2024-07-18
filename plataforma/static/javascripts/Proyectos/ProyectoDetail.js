const utcTimeElement = document.getElementById('utc-time');
const utcTimeString = utcTimeElement.textContent; // Obtén la hora UTC como cadena
const utcDate = new Date(utcTimeString); // Crea un objeto Date desde la cadena UTC

// Convierte la hora UTC a la hora local
const localTimeString = utcDate.toLocaleString('es-MX', { timeZone: 'America/Mexico_City' });

// Actualiza el contenido de la etiqueta con la hora local
utcTimeElement.textContent = localTimeString;

