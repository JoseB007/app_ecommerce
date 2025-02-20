$(function () {
    let titulo = ""
    let msj = ""
    let icono = ""

    if($(".mensajes li").length > 1) {
        $.each($(".mensajes li"), function() {
            msj += "<p>" + $(this).text() + "</p>";
        })
        sweetAlert_mensajes("Info", msj, "info");
    }

    if($(".mensajes li").length === 1) {
        icono = $(".mensajes li").attr('class')
        msj = $(".mensajes li").text()
        if($(".mensajes li").attr('class') === "success") {
            titulo = "Éxito"
        } else if($(".mensajes li").attr('class') === "info") {
            titulo = "Información"
        } else {
            titulo = "Error"
        };
        sweetAlert_mensajes(titulo, msj, icono)
    };
})