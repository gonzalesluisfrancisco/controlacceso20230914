function actualizarPersonal() {
    console.log("Actualizar personal")
    id = document.getElementById("id").value
    n_persona = document.getElementById("n_persona").value
    nombre = document.getElementById("nombre").value
    ap_paterno = document.getElementById("ap_paterno").value
    ap_materno = document.getElementById("ap_materno").value
    dni = document.getElementById("dni").value
    f_nac = document.getElementById("f_nac").value
    proyecto = document.getElementById("proyecto").value
    centro_coste = document.getElementById("centro_coste").value
    tipo_trabajador = document.getElementById("tipo_trabajador").value
    radioButtons = document.getElementsByName("clave_sexo")
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            valorSeleccionado = radioButtons[i].value;
            break;
        }
    }
    clave_sexo = valorSeleccionado
    f_alta = document.getElementById("f_alta").value
    motivo_cese = document.getElementById("motivo_cese").value
    cargo = document.getElementById("cargo").value
    card_id = document.getElementById("card_id").value
    area = document.getElementById("area").value
    servicio = document.getElementById("servicio").value
    supervision = document.getElementById("supervision").value
    radioButtons = document.getElementsByName("guardia")
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            valorSeleccionado = radioButtons[i].value;
            break;
        }
    }
    guardia = valorSeleccionado
    correo = document.getElementById("correo").value
    telefono = document.getElementById("telefono").value
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
        url: '',
        method: 'POST',
        data: {
            comando: "actualizarPersonal",
            csrfmiddlewaretoken: csrfToken,
            id: id,
            n_persona: n_persona,
            nombre: nombre,
            ap_paterno: ap_paterno,
            ap_materno: ap_materno,
            dni: dni,
            f_nac: f_nac,
            proyecto: proyecto,
            centro_coste: centro_coste,
            tipo_trabajador: tipo_trabajador,
            clave_sexo: clave_sexo,
            f_alta: f_alta,
            motivo_cese: motivo_cese,
            cargo: cargo,
            card_id: card_id,
            area: area,
            servicio: servicio,
            supervision: supervision,
            guardia: guardia,
            correo: correo,
            telefono: telefono
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
            else {
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then(() => {
                    window.location.reload()
                });
            }
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