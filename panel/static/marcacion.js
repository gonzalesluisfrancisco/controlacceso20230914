var tabla;
var searchValue
$(document).ready(function () {
    tabla = $('#Marcacion').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '',  // Ruta URL de tu vista Django
            type: "POST",
            data: function (d) {
                d.Comando = "TablaMarcacion"
                d.min = $('#min').val();
                d.max = $('#max').val();
                d.csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
            },
        },
        "order": [[0, "desc"]],
        columns: [
            { data: "primarykey", visible: false },
            { data: "id" },
            { data: "card_id" },
            { data: "ap_paterno" },
            { data: "ap_materno" },
            { data: "nombre" },
            { data: "dni" },
            { data: "proyecto" },
            { data: "cargo" },
            { data: "area" },
            { data: "servicio" },
            { data: "supervision" },
            { data: "guardia" },
            { data: "f_evento" },
            { data: "h_evento" },
            { data: "evento" },
            { data: "status" },
            {
                data: null, // Utiliza null como marcador para la nueva columna
                render: function (data, type, row) {
                    // En esta función, puedes construir el contenido de la celda de "Borrar Registro"
                    return '<button class="btn btn-danger" type="button" onclick="borrarRegistro(\'' + row.primarykey + '\')">Borrar</button>';
                }
            },
        ],
    });
    $('#Marcacion thead input').on('input', function () {
        searchValue = $(this).val();
    });
});


$(document).ready(function () {
    $("#min, #max").datepicker({
        dateFormat: 'yy-mm-dd',  // Formato de fecha
        onSelect: function (dateText, inst) {
            // Capturar la fecha seleccionada y realizar acciones adicionales si es necesario
            var selectedDate = $(this).val();
            console.log("Fecha seleccionada: " + selectedDate);
            tabla.draw();
            // Ocultar la tabla del calendario
            $("#calendar").hide();
        }
    });

    // Mostrar la tabla del calendario cuando se hace clic en los campos de entrada
    $("#min, #max").click(function () {
        $("#calendar").show();
    });
});

// Definir el filtro personalizado para las fechas
$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        var minDate = $("#min").val();
        var maxDate = $("#max").val();
        var currentDate = moment(data[6], 'YYYY-MM-DD').format('YYYY-MM-DD');
        if ((minDate === '' || currentDate >= minDate) && (maxDate === '' || currentDate <= maxDate)) {
            console.log("A")
            return true;
        }
        console.log("B")
        return false;
    }
);

function DescargarExcel() {
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

    var searchValue = '';


    $.ajax({
        url: '',
        method: 'GET',
        data: {
            Comando: "DescargarExcel",
            FechaInicial: $('#min').val(),
            FechaFinal: $('#max').val(),
            Search: document.getElementsByClassName("form-control form-control-sm")[0].value,
        },
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            Swal.close()
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'Historial_ingresos_salidas.xlsx';
            a.click();
            window.URL.revokeObjectURL(url);
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

function borrarRegistro(primarykey) {
    console.log(primarykey)
    Swal.close();
    Swal.fire({
        icon: 'question',
        text: "¿Esta seguro que desea eliminar el registro?",
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Si!',
        denyButtonText: `No!`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isDenied) {
            return;
        }
        else {
            console.log("Continua a eliminar")
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
            $.ajax({
                url: '',
                type: 'POST',
                data: {
                    comando: 'eliminarRegistro',
                    primarykey: primarykey,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    if (response.Estado == "noExitoso") {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: response.Mensaje
                        });
                        window.location.reload()
                        return
                    }
                    Swal.close();
                    Swal.fire({
                        icon: 'success',
                        title: 'Correcto',
                        text: response.Mensaje
                    });
                    window.location.reload()
                },
                error: function (error) {
                    Swal.close();
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