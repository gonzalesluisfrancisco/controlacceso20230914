function EliminarUsuario() {
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
    var Usuario = $("#usuario").val();
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            Comando: "EliminarUsuario",
            Usuario: Usuario,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
            }
            else {
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload();
                    }
                });
            }
            return
        },
        error: function (xhr, status, error) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error
            });
        }
    });
}

function ActualizarValores() {
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
    var Usuario = $("#usuario").val();
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            Comando: "ConsultarDatos",
            Usuario: Usuario,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                document.getElementsByName("nuevousuario")[0].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[1].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[2].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[3].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[4].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[5].placeholder = "No hay datos"
                document.getElementsByName("nuevousuario")[6].placeholder = "No hay datos"
            }
            else {
                document.getElementsByName("nuevousuario")[0].placeholder = response.Nombre
                document.getElementsByName("nuevousuario")[1].placeholder = response.PrimerApellido
                document.getElementsByName("nuevousuario")[2].placeholder = response.SegundoApellido
                document.getElementsByName("nuevousuario")[3].placeholder = response.DNI
                document.getElementsByName("nuevousuario")[4].placeholder = response.Correo
                document.getElementsByName("nuevousuario")[5].placeholder = response.Telefono
                document.getElementsByName("nuevousuario")[6].placeholder = response.Rol
            }
            return
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
