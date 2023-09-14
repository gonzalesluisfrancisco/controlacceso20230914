function EnviarExcel(Comando, index) {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false,
        showCancelButton: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    var fileInput = document.getElementsByName('excelFile')[index - 1];
    var file = fileInput.files[0];
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(Comando)
    if (file) {
        var formData = new FormData();
        formData.append('excelFile', file);
        formData.append('Comando', Comando);
        $.ajax({
            type: 'POST',
            url: '',
            data: formData,
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function (response) {
                Swal.close();
                if (response.Estado == "Invalido") {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.Mensaje
                    }).then(() => {
                        window.location.reload()
                    });

                }
                else {
                    console.log(response.Mensaje)
                    Swal.fire({
                        icon: 'success',
                        title: 'Correcto',
                        html: response.Mensaje
                    }).then(() => {
                        window.location.reload()
                    });
                }
                return response;
            },
            error: function (xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error
                }).then(() => {
                    window.location.reload()
                });
            }
        });
    }
}

function eliminarTodo() {
    Swal.close();
    Swal.fire({
        icon: 'question',
        text: "¿Esta seguro que desea eliminar toda la planilla?",
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Si',
        denyButtonText: `No`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isDenied) {
            return;
        }
        else {
            Swal.fire({
                title: 'Cargando...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                },
                showConfirmButton: false,
                showCancelButton: false,
                allowEscapeKey: false,
                allowEnterKey: false,
            });
            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                type: "POST",
                url: "",
                data: {
                    csrfmiddlewaretoken: csrfToken,
                    Comando: "eliminarPlantilla",
                },
                success: function (response) {
                    if (response.Estado == "Valido") {
                        Swal.fire({
                            icon: 'success',
                            title: 'Correcto',
                            text: response.Mensaje
                        });
                        window.location.reload()
                        return
                    }
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.Mensaje
                    });
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error
                    });
                }
            });
        }
    });
}