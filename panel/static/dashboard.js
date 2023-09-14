var area = ""
var servicio = ""
var fecha = ""
var cargo = ""

var datosTabla1 = [['Personal', 'Ingreso/Salidas', { role: 'style' }], ["---", 10, 'red'], ["---", 10, 'blue']]
var datosTabla2 = [
  ['Dia', 'Cantidad Ingresos', 'Cantidad Salidas'],
  ['Lunes', 11, 11],
  ['Martes', 12, 12],
  ['Miercoles', 13, 13],
  ['Jueves', 14, 14],
  ['Viernes', 15, 15],
  ['Sabado', 16, 16],
  ['Domingo', 17, 17]
]
var datosTabla3 = [
  ['Dia', 'Hora Ingreso', 'Hora Salida'],
  ['Lunes', [11, 11, 11], [11, 11, 11]],
  ['Martes', [12, 12, 12], [12, 12, 12]],
  ['Miercoles', [13, 13, 13], [13, 13, 13]],
  ['Jueves', [13, 13, 13], [13, 13, 13]],
  ['Viernes', [14, 14, 14], [14, 14, 14]],
  ['Sabado', [15, 15, 15], [15, 15, 15]],
  ['Domingo', [16, 16, 16], [16, 16, 16]]
]

function armaData() {
  var values = document.getElementById("values")
  console.log(values.innerHTML);
  var cabecera = [['Personal', 'Ingreso/Salidas', { role: 'style' }], ["---", 10, 'red'], ["---", 10, 'blue']]
  console.log(cabecera);
  return cabecera
}

function armaDataFiltro(arregloEntrada, tabla) {
  if (tabla == 1) var cabecera2 = [['Personal', 'Ingreso/Salidas', { role: 'style' }]]
  else if (tabla == 2) var cabecera2 = [['Dia', 'Cantidad Ingresos', 'Cantidad Salidas']]
  else if (tabla == 3) var cabecera2 = [['Dia', 'Hora Ingreso', 'Hora Salida']]

  console.log(arregloEntrada.length);
  var data2 = JSON.parse(arregloEntrada)
  for (var i = 0; i < data2.length; i++)
    cabecera2.push(data2[i]);
  console.log(cabecera2);
  return cabecera2
}

function filtroArea() {
  area = document.getElementById("filtroArea").value
  if (area == "NINGUNO") area = ""
  recibeDatos()
}

function filtroServicio() {
  servicio = document.getElementById("filtroServicio").value
  if (servicio == "NINGUNO") servicio = ""
  recibeDatos()
}

function filtroMesAnho() {
  fecha = document.getElementById("datepicker").value
  recibeDatos()
}

function filtroCargo() {
  cargo = document.getElementById("filtroCargo").value
  if (cargo == "NINGUNO") cargo = ""
  recibeDatos()
}

function recibeDatos() {
  console.log(area)
  console.log(servicio)
  console.log(fecha)
  console.log(cargo)
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
      comando: 'filtrarDatos',
      area: area,
      servicio: servicio,
      fecha: fecha,
      cargo: cargo,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
    },

    success: function (response) {
      Swal.close();
      console.log(response)
      if (response.Estado == "OK") {
        console.log("Se recibio datos filtrados")
        datosTabla1 = armaDataFiltro(response.valuesTabla1, 1)
        drawChartBar()
        datosTabla2 = armaDataFiltro(response.valuesTabla2, 2)
        drawChartColumn1()
        datosTabla3 = armaDataFiltro(response.valuesTabla3, 3)
        drawChartColumn2()
        return
      }
      Swal.close();
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: "No se recibio datos filtrados"
      });
      console.log("No se recibio datos filtrados")
    },
    error: function (error) {
      Swal.close();
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: "Hubo error al comunicarse con el servidor"
      });
      console.log("Hubo error al recibir ajax")
    }
  });
}

/////////////////////////////////////////
$("#datepicker").datepicker({
  format: "yyyy-mm",
  startView: "months",
  minViewMode: "months"
});

/////////////////////////////////////////

google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChartBar);
google.charts.setOnLoadCallback(drawChartColumn1);
google.charts.setOnLoadCallback(drawChartColumn2);

function drawChartBar() {
  //var data = google.visualization.arrayToDataTable([["Personal", "Ingreso/Salidas"], ["PERSONAL QUE INGRESO", 5], ["PERSONAL QUE SALIO", 22]]);
  //var data = google.visualization.arrayToDataTable(data2);
  var data = google.visualization.arrayToDataTable(datosTabla1);
  const optionsBar = {
    //title:'Resumen de Ingresos y Salidas por turno',
    hAxis: {
      title: 'Cantidad de personas',
      minValue: 0,
      viewWindow: {
        min: 0
      }
    },
    legend: 'none',
  };
  const chart = new google.visualization.BarChart(document.getElementById('myChartBar'));
  chart.draw(data, optionsBar);
};
function drawChartColumn1() {
  var dataColumn1 = google.visualization.arrayToDataTable(datosTabla2);
  const optionsColumn1 = {
    title: 'Resumen de cantidad entradas y Salidas por semana',
    hAxis: {
      title: 'Dia de semana',
    },
    vAxis: {
      title: 'Cantidad de personas',
      minValue: 0,
      viewWindow: {
        min: 0
      }
    },
    legend: 'none',
  };
  const chart2 = new google.visualization.ColumnChart(document.getElementById('myChartColumn1'));
  chart2.draw(dataColumn1, optionsColumn1);
};

function drawChartColumn2() {
  var dataColumn2 = google.visualization.arrayToDataTable(datosTabla3);
  const optionsColumn2 = {
    title: 'Promedio de horas entradas y Salidas por semana',
    hAxis: {
      title: 'Dia Semana',
    },
    vAxis: {
      title: 'Hora promedio',
      minValue: 0,
      viewWindow: {
        min: 0
      }
    },
    legend: 'none',
  };
  const chart3 = new google.visualization.ColumnChart(document.getElementById('myChartColumn2'));
  chart3.draw(dataColumn2, optionsColumn2);
};

window.onload = function () {
  var fechaActual = new Date();
  var mes = (fechaActual.getMonth() + 1).toString().padStart(2, '0');
  var año = fechaActual.getFullYear().toString();
  var mesYYear = año + '-' + mes;
  document.getElementById("datepicker").value = mesYYear
  console.log(mesYYear);
  filtroMesAnho();
}