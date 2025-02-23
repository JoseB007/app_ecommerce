$(function () {
    $("#form-carrito").on("submit", function (e) {
        e.preventDefault();

        const url_ = $(this).attr("action");
        const formData = new FormData(this); // Usar FormData para enviar archivos y otros datos

        solicitud_post_ajax(url_, formData, function (response) {
            if (!response.error) {
                const carritoItemsBadge = $("#carrito-items");

                if (response.carrito_items > 0) {
                    if (carritoItemsBadge.length === 0) {
                        $("#notify-carrito").append(
                            '<span id="carrito-items" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">' +
                                response.carrito_items +
                                '<span class="visually-hidden">unread messages</span></span>'
                        );
                    } else {
                        // Si el badge ya existe, actualiza su texto
                        carritoItemsBadge.text(response.carrito_items);
                    }
                } else {
                    // Si el carrito está vacío, elimina el badge
                    carritoItemsBadge.remove();
                }
            }
        });
    });
});
