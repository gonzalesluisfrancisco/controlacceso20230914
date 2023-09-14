var DEBUG = true
document.addEventListener("DOMContentLoaded", function () {
    $("[name='PantallaLogin']").css("display", "flex");
    $("[name='PantallaToken']").css("display", "none");
    $("[name='PantallaContrasenaOlvidada']").css("display", "none");
});

function EnviarCredenciales() {
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
    var Usuario = $("#username").val()
    var Contrasena = $("#password").val()
    var Captcha = VerificarCaptcha()
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "VerificarLogin",
            Usuario: Usuario,
            Contrasena: Contrasena,
            Captcha: Captcha
        },
        success: function (response) {
            Swal.close();
            if (DEBUG) console.log(response.Mensaje)
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
                });
                $("#MensajeToken").html($("#MensajeToken").html() + " " + response.Correo);
                MostarSegundoFactor()
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

function VerificarCaptcha() {
    var recaptchaResponse = grecaptcha.getResponse();
    if (recaptchaResponse === "") {
        return "Fallido";
    } else {
        return recaptchaResponse;
        ;
    }
}

function DatosIngresadosValidos(Usuario, Password, CAPTCHA) {
    if (DEBUG) return true;
    if (Usuario.length < 6) { alert("El usuario debe tener 6 caracteres como mínimo."); return false; }
    if (Password.length < 6) { alert("El password debe tener 8 caracteres como mínimo."); return false; }
    if (CAPTCHA.length < 10) { alert("Debe validar el CAPTCHA para continuar"); return false; }
    return true;
}

function MostarSegundoFactor() {
    $("[name='PantallaLogin']").css("display", "none");
    $("[name='PantallaToken']").css("display", "flex");
    $("[name='PantallaContrasenaOlvidada']").css("display", "none");
}

function EnviarToken() {
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
    var Usuario = $("#username").val()
    var Contrasena = $("#password").val()
    var Captcha = VerificarCaptcha()
    var Token = $("#token").val()
    //if (Token.length != 8) { alert("El token debe tener 8 caracteres"); return; }
    if (DEBUG) console.log(`Token: ${Token}`)
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "VerificarToken",
            Usuario: Usuario,
            Contrasena: Contrasena,
            Captcha: Captcha,
            Token: Token
        },
        success: function (response) {
            Swal.close()
            if (DEBUG) console.log(response.Mensaje)
            if (response.Estado == "Invalido") {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
            }
            else {
                Swal.close();
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/livedata";
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

function MostrarContrasenaOlvidada() {
    $("[name='PantallaLogin']").css("display", "none");
    $("[name='PantallaToken']").css("display", "none");
    $("[name='PantallaContrasenaOlvidada']").css("display", "flex");
}

function EnviarContrasenaOlvidada() {
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
    var Correo = $("#correo").val()
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Comando: "RecuperarCuenta",
            Correo: Correo,
        },
        success: function (response) {
            if (DEBUG) console.log(response.Mensaje)
            $(".loader").css("display", "none")
            if (response.Estado == "Invalido") {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.Mensaje
                });
            }
            else {
                Swal.close();
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/";
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

function CambiarContrasena() {
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
    var Contrasena1 = $("#password").val();
    var Contrasena2 = $("#password2").val();
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: "",
        data: {
            csrfmiddlewaretoken: csrfToken,
            Contrasena1: Contrasena1,
            Contrasena2: Contrasena2
        },
        success: function (response) {
            if (DEBUG) console.log(response.Mensaje)
            if (response.Estado == "Invalido") {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    html: response.Mensaje.replace(/\n/g, '<br>')
                });
            }
            else {
                Swal.close();
                Swal.fire({
                    icon: 'success',
                    title: 'Correcto',
                    text: response.Mensaje
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/";
                    }
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