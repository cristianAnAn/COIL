    $(document).ready(function(){

        $('input[type="file"]').on('change', function(){
            var reader = new FileReader();
            reader.onload = function(e){
                $('#imagenPreview').attr('src', e.target.result);
                $('#imagenCard').show();
            }
            reader.readAsDataURL(this.files[0]);
        });
    });

