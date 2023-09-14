from django.contrib.auth import authenticate
import pytz
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import random
import re
import hashlib


def FormatoLoginValidos(Usuario, Contrasena, Captcha):
    Resultado = False
    Mensaje = ""
    if len(Usuario) == 0:
        Mensaje = "El usuario debe tener 6 caracteres como mínimo."
    elif len(Contrasena) == 0:
        Mensaje = "La contraseña debe tener 8 caracteres como mínimo."
    elif len(Captcha) < 10:
        Mensaje = "El captcha no ha sido resuelto."
    else:
        Resultado = True
    return Resultado, Mensaje


def DatosLoginValidos(request, Usuario, Contrasena):
    User = authenticate(request, username=Usuario, password=Contrasena)
    if User is None:
        return False, "El usuario o contraseña no es correcto"
    else:
        return True, "El usuario y contraseña son correctos"


def EnviarToken(Usuario, Contrasena, request):
    FechaHora = datetime.now(pytz.timezone(
        'America/Lima')).strftime("%Y%m%d%H%M%S")
    Key = "4DM1ND14CSAK3Y"  # Cambia esto por tu clave secreta
    combined_string = FechaHora + Key
    hash_object = hashlib.sha256(combined_string.encode())
    hash_hex = hash_object.hexdigest()
    Token = hash_hex[:6].upper()
    print(Token)
    User = authenticate(request, username=Usuario, password=Contrasena)
    Asunto = "Codigo de acceso - DIACSA"
    MensajeHTML = f"""\
    <html>
    <head></head>
    <body>
        <p>Hola, <span style="font-size: larger;">{User.first_name}</span>!</p>
        <p>Este es tu token de verificación: <span style="font-size: larger;"><b>{Token}</b></span></p>
    </body>
    </html>
    """
    EnviaCorreo(User.email, Asunto, MensajeHTML)
    Correo = User.email
    Direccion, Dominio = Correo.split('@')
    DireccionOculta = Direccion[:2] + '*' * \
        (len(Direccion) - 3) + Direccion[-1]
    return DireccionOculta + '@' + Dominio


def EnviaCorreo(Destino, Asunto, MensajeHTML):
    email_subject = Asunto
    sender_email_address = "pruebapythonenvioemail@gmail.com"
    receiver_email_address = Destino
    email_smtp = "smtp.gmail.com"
    email_password = "nxolslszfpecabmd"
    message = EmailMessage()
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    html_content = MensajeHTML
    message.add_alternative(html_content, subtype='html')
    server = smtplib.SMTP(email_smtp, '587')
    server.ehlo()
    server.starttls()
    server.login(sender_email_address, email_password)
    server.send_message(message)
    server.quit()


def VerificarToken(TokenIngresado):
    FechaHora_dt = datetime.now(pytz.timezone('America/Lima'))
    for i in range(120):
        FechaHora = (FechaHora_dt - timedelta(seconds=i)
                     ).strftime("%Y%m%d%H%M%S")
        Key = "4DM1ND14CSAK3Y"
        combined_string = FechaHora + Key
        hash_object = hashlib.sha256(combined_string.encode())
        hash_hex = hash_object.hexdigest()
        TokenCalculado = hash_hex[:6].upper()
        if TokenCalculado == TokenIngresado.upper():
            return True
    return False


def ContrasenaEsFuerte(contrasena):
    tiene_mayuscula = bool(re.search(r'[A-Z]', contrasena))
    tiene_minuscula = bool(re.search(r'[a-z]', contrasena))
    tiene_numero = bool(re.search(r'[0-9]', contrasena))
    no_contiene_secuencias = not re.search(
        r'(123|234|345|456|567|678|789|987|876|765|654|543|432|321|000|111|222|333|444|555|666|777|888|999|qwerty|asdfgh|zxcvbn)', contrasena, flags=re.I)
    return tiene_mayuscula and tiene_minuscula and tiene_numero and no_contiene_secuencias


def debugPrint(string):
    # return
    print(string)
