function solicitud_post_ajax(url, parametros, callback) {
    $.ajax({
        url: url,
        type: "POST",
        data: parametros,
        processData: false, // Importante: no procesar los datos
        contentType: false, // Importante: no establecer el tipo de contenido
        success: function (response) {
            if (!response.error) {
                if (typeof callback === "function") {
                    callback(response);
                } else {
                    location.href = callback;
                }
            } else {
                mensaje_error(response.error);
            }
        },
        error: function (xhr, status) {
            if (xhr.status === 401) {
                // Usuario no autenticado, redirigir manualmente a la página de login
                let response = JSON.parse(xhr.responseText);
                window.location.href = response.redirect_url;
            } else {
                alert("Disculpe, existió un problema.", status + ": " + xhr);
            }
        },
    });
}

function solicitud_get_ajax(url, parametros, callback = null) {
    $.ajax({
        url: url,
        type: "GET",
        headers: { "Ajax-Request": "true" },
        data: parametros,
        success: function (response) {
            if (!response.error) {
                if (callback && typeof callback === "function") {
                    callback(response);
                } else {
                    console.log("Respuesta recibida:", response);
                }
            }
        },
        error: function (xhr, status) {
            alert("Error en la solicitud AJAX:", status + ": " + xhr);
        },
    });
}

function sweetAlert_mensajes(titulo, msj, icono) {
    Swal.fire({
        title: titulo,
        html: msj,
        icon: icono,
    });
}

function mensaje_error(obj) {
    let msj = "";
    if (typeof obj === "object") {
        $.each(obj, function (key, value) {
            msj += "<p>" + key + ": " + value + "</p>";
        });
    } else {
        msj = "<p>" + obj + "</p>";
    }
    sweetAlert_mensajes("Error", msj, "error");
}

function toastr_funcion(obj) {
    $.each(obj, function () {
        if (this[0] == "success") {
            toastr["success"](this[1]);
        }
        if (this[0] == "info") {
            toastr["info"](this[1]);
        }
    });
}
