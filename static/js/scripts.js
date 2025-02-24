$(function () {
    toastr.options = {
        closeButton: false,
        debug: false,
        newestOnTop: false,
        progressBar: false,
        positionClass: "toast-bottom-right",
        preventDuplicates: false,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "5000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut",
    };

    const mensajes = $(".messages li");
    $.each(mensajes, function () {
        if ($(this).hasClass("success")) {
            toastr["success"]($(this).text(), "Éxito");
        } else if ($(this).hasClass("info")) {
            sweetAlert_mensajes("Info", $(this).text(), "info");
        } else {
            sweetAlert_mensajes("Error", $(this).text(), "error");
        }
    });
});
