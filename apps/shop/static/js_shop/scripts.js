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
                            '<span id="carrito-items" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-info">' +
                                response.carrito_items +
                                '<span class="visually-hidden">unread messages</span></span>'
                        );
                    } else {
                        // Si el badge ya existe, actualiza su texto
                        carritoItemsBadge.text(response.carrito_items);
                    }
                    toastr_funcion(response.message);
                } else {
                    // Si el carrito está vacío, elimina el badge
                    carritoItemsBadge.remove();
                }
            }
        });
    });

    $("#form-favorito").on("submit", function (e) {
        e.preventDefault();

        const url_ = $(this).attr("action");
        const formData = new FormData(this);

        solicitud_post_ajax(url_, formData, function (response) {
            if (!response.error) {
                toastr_funcion(response.message);

                // Selecciona el botón actual
                let btn = $("#add-favorito");

                // Define el nuevo botón
                let new_btn =
                    '<button id="add-favorito"><i class="fas fa-heart"></i> ' +
                    response.txt_button +
                    "</button>";
                
                // Reemplaza el botón actual con el nuevo botón
                btn.replaceWith(new_btn);

                if (response.txt_button == "Eliminar de favoritos") {
                    $("#add-favorito").addClass('btn btn-outline-danger')
                }
                else {
                    $("#add-favorito").addClass('btn btn-outline-secondary')
                }
            }
        });
    });
});
