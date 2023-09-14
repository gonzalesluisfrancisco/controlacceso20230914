function RegistrarUsuario() {
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
    var Nombre = document.getElementsByName("nuevousuario")[0].value
    var PrimerApellido = document.getElementsByName("nuevousuario")[1].value
    var SegundoApellido = document.getElementsByName("nuevousuario")[2].value
    var DNI = document.getElementsByName("nuevousuario")[3].value
    var Correo = document.getElementsByName("nuevousuario")[4].value
    var Telefono = document.getElementsByName("nuevousuario")[5].value
    var Rol = document.getElementsByName("nuevousuario")[6].value
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "RegistrarUsuario",
            Nombre: Nombre,
            PrimerApellido: PrimerApellido,
            SegundoApellido: SegundoApellido,
            DNI: DNI,
            Correo: Correo,
            Telefono: Telefono,
            Rol: Rol
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
            return response;
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