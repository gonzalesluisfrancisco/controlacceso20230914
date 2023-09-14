function AgregarDatos() {
    console.log("Entra a agregardatos")
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
    dni = document.getElementById("dni").value
    f_ingreso = document.getElementById("f_ingreso").value
    h_ingreso = document.getElementById("h_ingreso").value
    evento = document.getElementById("evento").value
    $.ajax({
        url: '',
        method: 'POST',
        data: {
            comando: "agregarLivedata",
            dni: dni,
            f_ingreso: f_ingreso,
            h_ingreso: h_ingreso,
            evento: evento,
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
                return
            }
            Swal.fire({
                icon: 'success',
                title: 'Correcto',
                text: response.Mensaje
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload()
                }
            });
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

function BusquedaDatos() {
    dni = document.getElementById("dni").value
    if (dni.length != 8) return;
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
    console.log(dni)
    $.ajax({
        url: '',
        method: 'POST',
        data: {
            dni: dni,
            csrfmiddlewaretoken: csrfToken,
            comando: "consultaDatos"
        },
        success: function (response) {
            Swal.close();
            if (response.Estado == "Invalido") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
                return
            }
            document.getElementById("card_id").value = response.card_id
            document.getElementById("nombre").value = response.nombre
            document.getElementById("apellido").value = response.apellido
            document.getElementById("cargo").value = response.cargo
            document.getElementById("guardia").value = response.guardia
            document.getElementById("f_ingreso").value = response.f_ingreso
            document.getElementById("h_ingreso").value = response.h_ingreso
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