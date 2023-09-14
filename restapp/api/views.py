from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from restapp.models import PostCardIDEvent
from restapp.api.serializers import restappSerializer
# from rest_framework.decorators import action
# from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import viewsets
from panel.models import PersonalRegistrado
from panel.models import LiveData
from panel.models import Historial
from panel.models import NoRegistrados
from panel.models import deviceID

from django.http.response import HttpResponse

from datetime import datetime
# from django.utils import timezone
from zoneinfo import ZoneInfo
import pytz
from django.http import JsonResponse
import json
import re

from panel.Funciones import debugPrint


##########################################

def cardIDValido(cardIDs):
    N = len(cardIDs)
    if N < 1:
        debugPrint("cantidad de cardIDs no valido")
        return 0

    for cardID in cardIDs:
        cardID = cardID.upper()
        if (len(cardID) != 8):
            debugPrint("Longitud de cardID no valido")
            return 0
        for c in cardID:
            if not ((c >= '0' and c <= '9') or (c >= 'A' and c <= 'F')):
                debugPrint("cardID no valido")
                return 0

    return N


def f_eventoValido(f_eventos):
    N = len(f_eventos)
    if N < 1:
        debugPrint("cantidad de f_eventos no valido")
        return 0

    for f_evento in f_eventos:
        if len(f_evento) != 10:
            debugPrint("Longitud de f_evento no valido")
            return 0
        try:
            datetime.strptime(f_evento, '%Y-%m-%d')
        except:
            debugPrint("Formato de f_evento no valido")
            return 0

    return N


def h_eventoValido(h_eventos):
    N = len(h_eventos)
    if N < 1:
        debugPrint("cantidad de h_eventos no valido")
        return 0

    for h_evento in h_eventos:
        if len(h_evento) != 8:
            debugPrint("Longitud de f_evento no valido")
            return 0
        try:
            datetime.strptime(h_evento, '%H:%M:%S')
        except:
            debugPrint("Formato de h_evento no valido")
            return 0

    return N


def eventoValido(eventos):
    N = len(eventos)
    if N < 1:
        debugPrint("cantidad de eventos no valido")
        return 0

    for evento in eventos:
        if evento != "Ingreso" and evento != "Salida":
            debugPrint("Evento no valido")
            return 0

    return N


def validar_hora(hora_str):
    """Valida el formato de la hora y lo ajusta si es necesario."""
    debugPrint("Validar hora")
    # debugPrint(hora_str)
    hora_patron = re.compile(r'^\d{1,2}:\d{1,2}(:\d{1,2})?$')
    if not hora_patron.match(hora_str):
        raise ValueError('La hora debe tener el formato "H:m:s" o "H:m".')
    partes = hora_str.split(':')
    # debugPrint(partes)
    if len(partes) == 2:
        hora_str += ':00'
    # debugPrint(hora_str)
    return hora_str


def validacionDataJson1(dataJson):
    try:
        dataJson = dict(dataJson)
    except:
        debugPrint("dataJson vacio o incorrecta")
        return [[], [], [], [], []]

    deviceID = dataJson.pop('deviceID', None)
    if deviceID is None:
        debugPrint("No hay deviceID")
        return [[], [], [], [], []]
    if len(deviceID) != 1:
        debugPrint("No device ID valido")
        return [[], [], [], [], []]

    cardID = dataJson.pop('cardID', None)
    if cardID is None:
        debugPrint("No hay cardID")
        return [[], [], [], [], []]
    N = cardIDValido(cardID)
    if N == 0:
        return [[], [], [], [], []]

    f_evento = dataJson.pop('f_evento', None)
    if f_evento is None:
        debugPrint("No hay f_evento")
        return [[], [], [], [], []]
    if f_eventoValido(f_evento) != N:
        return [[], [], [], [], []]

    h_evento = dataJson.pop('h_evento', None)
    if h_evento is None:
        debugPrint("No hay h_evento")
        return [[], [], [], [], []]
    if h_eventoValido(h_evento) != N:
        return [[], [], [], [], []]

    evento = dataJson.pop('evento', None)
    if evento is None:
        debugPrint("No hay evento")
        return [[], [], [], [], []]
    if eventoValido(evento) != N:
        return [[], [], [], [], []]

    return [deviceID, cardID, f_evento, h_evento, evento]


def validacionDataJson(dataJson):
    try:
        dataJson = dict(dataJson)
    except:
        debugPrint("dataJson vacio o incorrecta")
        return []

    deviceID = dataJson.pop('deviceID', None)
    if deviceID is None:
        debugPrint("No hay deviceID")
        return []
    if len(deviceID) != 1:
        debugPrint("No device ID valido")
        return []

    cardID = dataJson.pop('cardID', None)
    if cardID is None:
        debugPrint("No hay cardID")
        return []
    N = cardIDValido(cardID)
    if N == 0:
        return []

    f_evento = dataJson.pop('f_evento', None)
    if f_evento is None:
        debugPrint("No hay f_evento")
        return []
    if f_eventoValido(f_evento) != N:
        return []

    h_evento = dataJson.pop('h_evento', None)
    if h_evento is None:
        debugPrint("No hay h_evento")
        return []
    if h_eventoValido(h_evento) != N:
        return []

    evento = dataJson.pop('evento', None)
    if evento is None:
        debugPrint("No hay evento")
        return []
    if eventoValido(evento) != N:
        return []

    datavalidada = []
    for i in range(N):
        datavalidada.append(
            [deviceID[0], cardID[i], f_evento[i], h_evento[i], evento[i]])

    return datavalidada

    # Elimina la clave 'querySet' si existe
    if 'querySet' in dataJson:
        del dataJson['querySet']
    debugPrint("Segunda a json dumps conversion")
    dataJson = json.dumps(dataJson)
    debugPrint(dataJson)

    try:
        # debugPrint("1")
        dataJson = json.loads(dataJson)
    except:
        # debugPrint("2")
        return False
    debugPrint("Tercera a json dumps conversion")
    debugPrint(dataJson)

    # dataJson.pop('csrfmiddlewaretoken',None)
    # cardid = models.IntegerField(null=False)
    # f_evento = models.DateField(null=True)
    # h_evento = models.TimeField(null=True)
    # evento = models.CharField(max_length=50, null=True)

    # debugPrint(dataJson)

    campos_esperados = ['cardid', 'f_evento', 'h_evento', 'evento']
    # debugPrint(set(dataJson.keys()))
    # debugPrint(set(campos_esperados))
    if set(dataJson.keys()) != set(campos_esperados):
        # debugPrint("3")
        return False
    # debugPrint("3.1")
    for campo in campos_esperados:
        if campo not in dataJson:
            # debugPrint("4")
            # debugPrint(f"Falta el campo {campo} en el objeto JSON")
            return False
    # debugPrint("4.1")
    # Otra opcion es implementarlo
    # if not all(campo in data for campo in campos_esperados):
    #    False
    # debugPrint(dataJson['cardid'][0])
    if int(dataJson['cardid'][0]) < 0 or int(dataJson['cardid'][0]) > 5000000:
        # debugPrint("5")
        return False
    # debugPrint("5.1")
    if dataJson['evento'][0] not in ["Ingreso", "Salida"]:
        # debugPrint("6")
        return False
    # debugPrint("6.1")
    # debugPrint(dataJson['f_evento'][0])
    try:
        datetime.strptime(dataJson['f_evento'][0], '%Y-%m-%d')
    except:
        # debugPrint("7")
        return False
    # debugPrint("7.1")
    try:
        hora_valida = validar_hora(dataJson['h_evento'][0])
    except ValueError as err:
        # debugPrint("8")
        # debugPrint("Error" + err)
        return False
    # debugPrint(dataJson['h_evento'])
    # debugPrint(dataJson['h_evento'][0])
    dataJson['h_evento'][0] = hora_valida
    # debugPrint("Se modifica hora")
    # debugPrint(dataJson['h_evento'])
    # debugPrint(dataJson['h_evento'][0])
    # debugPrint(dataJson)
    return True


def actualizarLiveDataNoRegistrado(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        debugPrint("Ubicacion LiveNoRegistrados")
        debugPrint(rubicacion)
        if (rubicacion is None):
            debugPrint("Ubicacion no encontrada en Live Data No Registrados")
            rubicacion = "No registrado"
    except:
        debugPrint(
            "Error en encontrar la ubicacion del deviceID en LiveData No Registrados.")
        rubicacion = "No registrado"

    if (revento == "Ingreso"):
        debugPrint("Ingreso registrado en LiveData No Registrados")
        existenteLiveData = LiveData.objects.filter(card_id=rcardID).first()
        while existenteLiveData is not None:
            existenteLiveData = LiveData.objects.filter(
                card_id=rcardID).first()
            if existenteLiveData is not None:
                existenteLiveData.delete()

        # usersLiveData = LiveData.objects.all()
        # cantidadactualRegistrada = usersLiveData.count()

        nuevoLiveData = LiveData()
        # nuevoLiveData.id = cantidadactualRegistrada+1
        nuevoLiveData.ubicacion       = rubicacion
        nuevoLiveData.n_persona       = "---"
        nuevoLiveData.ap_paterno      = "No Registrado"
        nuevoLiveData.ap_materno      = "No Registrado"
        nuevoLiveData.nombre          = "No Registrado"
        nuevoLiveData.dni             = "---"
        nuevoLiveData.proyecto        = "No Registrado"
        nuevoLiveData.centro_coste    = "---"
        nuevoLiveData.tipo_trabajador = "No Registrado"
        nuevoLiveData.clave_sexo      = "-"
        nuevoLiveData.cargo           = "No Registrado"
        nuevoLiveData.card_id         = rcardID
        nuevoLiveData.area            = "No Registrado"
        nuevoLiveData.servicio        = "No Registrado"
        nuevoLiveData.supervision     = "No Registrado"
        nuevoLiveData.guardia         = "-"
        f_evento                      = rfecha_evento
        h_evento                      = rhora_evento
        fecha_datetime = datetime.strptime(
            f_evento+' '+h_evento, '%Y-%m-%d %H:%M:%S')
        debugPrint(fecha_datetime)
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
        nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
        nuevoLiveData.f_nac = fecha_y_hora_con_zona_horaria.date()
        nuevoLiveData.f_alta = fecha_y_hora_con_zona_horaria.date()
        debugPrint(nuevoLiveData)
        nuevoLiveData.save()
        debugPrint("Guardado como ingreso en LiveData exitoso.")
        return
    elif (revento == "Salida"):
        debugPrint("Salida en LiveData No Registrado")
        try:
            datosUserLiveData = LiveData.objects.get(card_id=rcardID)
            if (datosUserLiveData is not None):
                debugPrint("Intenta borrar en LiveData No Registrados")
                datosUserLiveData.delete()
                return
            else:
                debugPrint("No está en la tabla de LiveData No registrados")
                return
        except:
            debugPrint(
                "Except luego de intentar borrar o encontrar. Puede ser porque no encuentra en LiveData.")
            return
    else:
        debugPrint("Evento desconocido en LiveData No Registrados")
        return


def actualizarLiveDataRegistrados(reg):

    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        datosUserLiveData = PersonalRegistrado.objects.get(card_id=rcardID)
        if (datosUserLiveData is None):
            debugPrint("Usuario no encontrado en Live Data Registrados")
            return
    except:
        debugPrint("Error en encontrar el usuario en Live Data Registrados.")
        return

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if (rdeviceID is None):
            debugPrint("Ubicacion no encontrada")
            rubicacion = "No registrado"
    except:
        debugPrint("Error en encontrar la ubicacion del deviceID.")
        rubicacion = "No registrado"

    if (revento == "Ingreso"):
        debugPrint("Ingreso registrado en LiveData")
        existenteLiveData = LiveData.objects.filter(card_id=rcardID).first()
        while existenteLiveData is not None:
            existenteLiveData = LiveData.objects.filter(
                card_id=rcardID).first()
            if existenteLiveData is not None:
                existenteLiveData.delete()

        # usersLiveData = LiveData.objects.all()
        # cantidadactualRegistrada = usersLiveData.count()

        nuevoLiveData = LiveData()
        # nuevoLiveData.id = cantidadactualRegistrada+1
        nuevoLiveData.ubicacion = rubicacion
        nuevoLiveData.n_persona = datosUserLiveData.n_persona
        nuevoLiveData.ap_paterno = datosUserLiveData.ap_paterno
        nuevoLiveData.ap_materno = datosUserLiveData.ap_materno
        nuevoLiveData.nombre = datosUserLiveData.nombre
        nuevoLiveData.dni = datosUserLiveData.dni
        nuevoLiveData.f_nac = datosUserLiveData.f_nac
        nuevoLiveData.proyecto = datosUserLiveData.proyecto
        nuevoLiveData.centro_coste = datosUserLiveData.centro_coste
        nuevoLiveData.tipo_trabajador = datosUserLiveData.tipo_trabajador
        nuevoLiveData.clave_sexo = datosUserLiveData.clave_sexo
        nuevoLiveData.f_alta = datosUserLiveData.f_alta
        nuevoLiveData.f_baja = datosUserLiveData.f_baja
        nuevoLiveData.motivo_cese = datosUserLiveData.motivo_cese
        nuevoLiveData.cargo = datosUserLiveData.cargo
        nuevoLiveData.card_id = datosUserLiveData.card_id
        nuevoLiveData.area = datosUserLiveData.area
        nuevoLiveData.servicio = datosUserLiveData.servicio
        nuevoLiveData.supervision = datosUserLiveData.supervision
        nuevoLiveData.guardia = datosUserLiveData.guardia
        nuevoLiveData.correo = datosUserLiveData.correo
        nuevoLiveData.n_celular = datosUserLiveData.n_celular
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(
            f_evento+' '+h_evento, '%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoLiveData.f_ingreso = fecha_y_hora_con_zona_horaria.date()
        nuevoLiveData.h_ingreso = fecha_y_hora_con_zona_horaria.time()
        nuevoLiveData.save()
        debugPrint("Guardado como ingreso en LiveData exitoso.")
        return
    elif (revento == "Salida"):
        debugPrint("Salida en LiveData")
        try:
            datosUserLiveData = LiveData.objects.get(card_id=rcardID)
            if (datosUserLiveData is not None):
                debugPrint("Intenta borrar")
                datosUserLiveData.delete()
                return
            else:
                debugPrint("No está en la tabla de LiveData")
                return
        except:
            debugPrint(
                "Except luego de intentar borrar. Puede ser porque no encuentra en LiveData.")
            return
    else:
        debugPrint("Evento desconocido en LiveData")
        return


def guardarHistorialRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if (rdeviceID is None):
            debugPrint("Ubicacion no encontrada en Historial Registrados")
            rubicacion = "No registrado"
    except:
        debugPrint(
            "Error en encontrar la ubicacion del deviceID en Historial Registrados.")
        rubicacion = "No registrado"

    try:
        datosUserHistorial = PersonalRegistrado.objects.get(card_id=rcardID)
        if (datosUserHistorial is None):
            debugPrint("Usuario no encontrado en historial Registrados")
            return

        usersHistorial = Historial.objects.all()
        cantidadactualRegistrada = usersHistorial.count()
        nuevoHistorial = Historial()
        nuevoHistorial.id = cantidadactualRegistrada+1
        nuevoHistorial.ubicacion = rubicacion
        nuevoHistorial.n_persona = datosUserHistorial.n_persona
        nuevoHistorial.ap_paterno = datosUserHistorial.ap_paterno
        nuevoHistorial.ap_materno = datosUserHistorial.ap_materno
        nuevoHistorial.nombre = datosUserHistorial.nombre
        nuevoHistorial.dni = datosUserHistorial.dni
        nuevoHistorial.f_nac = datosUserHistorial.f_nac
        nuevoHistorial.proyecto = datosUserHistorial.proyecto
        nuevoHistorial.centro_coste = datosUserHistorial.centro_coste
        nuevoHistorial.tipo_trabajador = datosUserHistorial.tipo_trabajador
        nuevoHistorial.clave_sexo = datosUserHistorial.clave_sexo
        nuevoHistorial.f_alta = datosUserHistorial.f_alta
        nuevoHistorial.f_baja = datosUserHistorial.f_baja
        nuevoHistorial.motivo_cese = datosUserHistorial.motivo_cese
        nuevoHistorial.cargo = datosUserHistorial.cargo
        nuevoHistorial.card_id = datosUserHistorial.card_id
        nuevoHistorial.area = datosUserHistorial.area
        nuevoHistorial.servicio = datosUserHistorial.servicio
        nuevoHistorial.supervision = datosUserHistorial.supervision
        nuevoHistorial.guardia = datosUserHistorial.guardia
        nuevoHistorial.correo = datosUserHistorial.correo
        nuevoHistorial.n_celular = datosUserHistorial.n_celular
        f_evento = rfecha_evento
        h_evento = rhora_evento
        fecha_datetime = datetime.strptime(
            f_evento+' '+h_evento, '%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        debugPrint(zona_horaria)
        # fecha_datetime_utc = fecha_datetime.replace(tzinfo=timezone.utc)
        # fecha_y_hora_con_zona_horaria = fecha_datetime.astimezone(zona_horaria)
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoHistorial.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoHistorial.evento = revento
        nuevoHistorial.save()
        return

    except:
        debugPrint("Error al guardar en Historial Registrados.")
        return


def guardarHistorialNoRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]

    try:
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        if (rdeviceID is None):
            debugPrint("Ubicacion no encontrada en Historial No Registrados")
            rubicacion = "No registrado"
    except:
        debugPrint(
            "Error en encontrar la ubicacion del deviceID en Historial No registrados.")
        rubicacion = "No registrado"

    try:

        usersHistorial                 = Historial.objects.all()
        cantidadactualRegistrada       = usersHistorial.count()
        nuevoHistorial                 = Historial()
        nuevoHistorial.id              = cantidadactualRegistrada+1
        nuevoHistorial.ubicacion       = rubicacion
        nuevoHistorial.n_persona       = "---"
        nuevoHistorial.ap_paterno      = "No Registrado"
        nuevoHistorial.ap_materno      = "No Registrado"
        nuevoHistorial.nombre          = "No Registrado"
        nuevoHistorial.dni             = "---"
        nuevoHistorial.proyecto        = "No Registrado"
        nuevoHistorial.centro_coste    = "---"
        nuevoHistorial.tipo_trabajador = "No Registrado"
        nuevoHistorial.clave_sexo      = "-"
        #nuevoHistorial.f_alta esta abajo          
        nuevoHistorial.cargo           = "No Registrado"
        nuevoHistorial.card_id         = rcardID
        nuevoHistorial.area            = "No Registrado"
        nuevoHistorial.servicio        = "No Registrado"
        nuevoHistorial.supervision     = "No Registrado"
        nuevoHistorial.guardia         = "-"
        f_evento                       = rfecha_evento
        h_evento                       = rhora_evento
        fecha_datetime = datetime.strptime(
            f_evento+' '+h_evento, '%Y-%m-%d %H:%M:%S')
        zona_horaria = pytz.timezone('America/Lima')
        fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
        nuevoHistorial.f_evento = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.h_evento = fecha_y_hora_con_zona_horaria.time()
        nuevoHistorial.evento = revento
        nuevoHistorial.f_nac = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.f_alta = fecha_y_hora_con_zona_horaria.date()
        nuevoHistorial.save()
        return

    except Exception as ex:
        debugPrint("Error al guardar en Historial No Registrados.")
        debugPrint(str(ex))
        return


def guardarNoRegistrados(reg):
    rdeviceID = reg[0]
    rcardID = reg[1]
    rfecha_evento = reg[2]
    rhora_evento = reg[3]
    revento = reg[4]
    debugPrint("Inicio evento en No Registrados")
    debugPrint(reg)
    try:
        debugPrint("rdeviceID")
        debugPrint(rdeviceID)
        rdeviceID = deviceID.objects.get(deviceID=rdeviceID)
        rubicacion = rdeviceID.ubicacion
        debugPrint("Ubicacion")
        debugPrint(rubicacion)
        if (rdeviceID is None):
            debugPrint("Ubicacion no encontrada en No Registrados")
            rubicacion = "Ubicacion No registrada"
    except:
        debugPrint(
            "Error en encontrar la ubicacion del deviceID en No Registrados.")
        rubicacion = "Ubicacion No registrada"

    # usersNoRegistrados = NoRegistrados.objects.all()
    # cantidadactualRegistrada = usersNoRegistrados.count()
    # debugPrint("Cantidad actual")
    # debugPrint(cantidadactualRegistrada)
    nuevoNoRegistrados = NoRegistrados()
    # nuevoNoRegistrados.id = cantidadactualRegistrada+1
    nuevoNoRegistrados.ubicacion = rubicacion
    nuevoNoRegistrados.card_id = rcardID
    f_evento = rfecha_evento
    h_evento = rhora_evento
    fecha_datetime = datetime.strptime(
        f_evento+' '+h_evento, '%Y-%m-%d %H:%M:%S')
    zona_horaria = pytz.timezone('America/Lima')
    fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
    nuevoNoRegistrados.f_evento = fecha_y_hora_con_zona_horaria.date()
    nuevoNoRegistrados.h_evento = fecha_y_hora_con_zona_horaria.time()
    nuevoNoRegistrados.evento = revento
    nuevoNoRegistrados.save()
    debugPrint("Evento guardado en No Registrados exitoso.")
    return


DEBUG = False


class restappViewSet(ModelViewSet):
    serializer_class = restappSerializer
    queryset = PostCardIDEvent.objects.all()

    # Token ad6f62d1732f261807694c3385ec9030af572d779
    # Basic YWRtaW5kaWFjc2E6MTdEaWFjc2E=

    # authentication_classes = [TokenAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        # Validacion de datos
        try:
        
            # debugPrint('DATA QUE LLEGA A LA VISTA CREATE POR DEFECTO')
            # debugPrint(data)
            registros = validacionDataJson(data)
            N = len(registros)
            if N == 0:
                return JsonResponse({'error': 'Verificar campos'}, status=400)
        except:
            return JsonResponse({'error': 'Error inesperado en campos'}, status=400)

        for i in range(N):
            reg = registros[i]
            rcardID = reg[1]
            if DEBUG:
                debugPrint("-------------")
            try:
                t0 = datetime.now()
                user = PersonalRegistrado.objects.get(card_id=rcardID)
                t1 = datetime.now()
                print(t1-t0)
                if (user is None):
                    debugPrint("Usuario no encontrado")
            except:
                debugPrint("Usuario no encontrado except")
                debugPrint("1")
                debugPrint("2")
                debugPrint("3")
                guardarHistorialNoRegistrados(reg)
                actualizarLiveDataNoRegistrado(reg)
                guardarNoRegistrados(reg)
                continue

            #####################################
            try:
                debugPrint(
                    "Usuario encontrado. Se registrará en 'Live Data' e 'Historial'")
                actualizarLiveDataRegistrados(reg)
                guardarHistorialRegistrados(reg)

            except:
                debugPrint(
                    "Error en actualizar en base de datos. Se registrará en 'No Registrados' e 'Historial'.")
                continue
        # super().create(request)

        
        return JsonResponse({'envio': 'OK'}, status=200)
