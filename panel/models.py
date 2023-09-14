from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PersonalRegistrado(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_persona = models.CharField(max_length=8, null=False)
    ap_paterno = models.CharField(max_length=50, null=False)
    ap_materno = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    dni = models.CharField(max_length=8, null=False)
    f_nac = models.DateField(null=True)
    proyecto = models.CharField(max_length=50, null=False)
    centro_coste = models.CharField(max_length=50, null=False)
    tipo_trabajador = models.CharField(max_length=50, null=False)
    clave_sexo = models.CharField(max_length=1, null=False)
    f_alta = models.DateField(null=False)
    f_baja = models.DateField(null=True)
    motivo_cese = models.CharField(max_length=50, null=True, default="")
    cargo = models.CharField(max_length=50, null=False)
    card_id = models.CharField(max_length=8, null=False)
    area = models.CharField(max_length=50, null=False)
    servicio = models.CharField(max_length=50, null=False)
    supervision = models.CharField(max_length=50, null=False)
    guardia = models.CharField(max_length=1, null=False)
    correo = models.CharField(max_length=50, null=True, default="")
    n_celular = models.CharField(max_length=50, null=True, default="")

    class Meta:
        db_table = 'PersonalRegistrado'


class LiveData(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    f_ingreso = models.DateField(null=True)
    h_ingreso = models.TimeField(null=True)
    n_persona = models.CharField(max_length=8, null=False)
    ap_paterno = models.CharField(max_length=50, null=False)
    ap_materno = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    dni = models.CharField(max_length=8, null=False)
    f_nac = models.DateField(null=True)
    proyecto = models.CharField(max_length=50, null=False)
    centro_coste = models.CharField(max_length=50, null=False)
    tipo_trabajador = models.CharField(max_length=50, null=False)
    clave_sexo = models.CharField(max_length=1, null=False)
    f_alta = models.DateField(null=False)
    f_baja = models.DateField(null=True, blank=True)
    motivo_cese = models.CharField(max_length=50, null=True, default="", blank=True)
    cargo = models.CharField(max_length=50, null=False)
    card_id = models.CharField(max_length=8, null=False)
    area = models.CharField(max_length=50, null=False)
    servicio = models.CharField(max_length=50, null=False)
    supervision = models.CharField(max_length=50, null=False)
    guardia = models.CharField(max_length=1, null=False)
    correo = models.CharField(max_length=50, null=True, default="", blank=True)
    n_celular = models.CharField(max_length=50, null=True, default="", blank=True)

    def __str__(self):
        return str(self.card_id)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'LiveData'


class Historial(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=2, null=False, default='0')
    n_persona = models.CharField(max_length=8, null=False)
    ap_paterno = models.CharField(max_length=50, null=False)
    ap_materno = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    dni = models.CharField(max_length=8, null=False)
    f_nac = models.DateField(null=True)
    proyecto = models.CharField(max_length=50, null=False)
    centro_coste = models.CharField(max_length=50, null=False)
    tipo_trabajador = models.CharField(max_length=50, null=False)
    clave_sexo = models.CharField(max_length=1, null=False)
    f_alta = models.DateField(null=False)
    f_baja = models.DateField(null=True)
    motivo_cese = models.CharField(max_length=50, null=True, default="")
    cargo = models.CharField(max_length=50, null=False)
    card_id = models.CharField(max_length=8, null=False)
    area = models.CharField(max_length=50, null=False)
    servicio = models.CharField(max_length=50, null=False)
    supervision = models.CharField(max_length=50, null=False)
    guardia = models.CharField(max_length=1, null=False)
    
    correo = models.CharField(max_length=50, null=True, default="")
    n_celular = models.CharField(max_length=50, null=True, default="")

    def __str__(self):
        return str(self.card_id)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'Historial'


class NoRegistrados(models.Model):
    id = models.BigAutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50, null=True)
    cardidHex = models.CharField(max_length=8, null=True)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.cardidHex)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'NoRegistrados'


class deviceID(models.Model):
    id = models.IntegerField(primary_key=True)
    deviceID = models.CharField(max_length=8, null=True)
    ubicacion = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.deviceID)+" "+str(self.ubicacion)

    class Meta:
        db_table = 'deviceID'


class UserInfo(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    DNI = models.CharField(max_length=8)
    Telefono = models.CharField(max_length=9)
    SegundoApellido = models.CharField(max_length=50)

    class Meta:
        db_table = 'userInfo'

#######################
