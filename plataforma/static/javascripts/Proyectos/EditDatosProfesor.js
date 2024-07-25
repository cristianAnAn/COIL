document.getElementById('editButton').addEventListener('click', function() {
    document.querySelectorAll('#profesorForm textarea, #profesorForm input').forEach(function(element) {
        element.removeAttribute('disabled');
        element.classList.add('form-control');
    });
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline-block';
    document.getElementById('cancelButton').style.display = 'inline-block';
});

document.getElementById('cancelButton').addEventListener('click', function() {
    document.querySelectorAll('#profesorForm textarea, #profesorForm input').forEach(function(element) {
        element.setAttribute('disabled', 'true');
        element.classList.add('form-control');
    });
    document.getElementById('editButton').style.display = 'inline-block';
    document.getElementById('saveButton').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
});

document.getElementById('id_imagen').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function(){
        var output = document.getElementById('imagenPreview');
        output.src = reader.result;
        document.getElementById('previewCard').style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
});
