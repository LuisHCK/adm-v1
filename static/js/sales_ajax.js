    $("#form_vender").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: {
                product: $('#id_product').val(),
                quantity: $('#id_quantity').val(),
                discount: $('#id_discount').val(),
                csrfmiddlewaretoken: $(this).attr('token')
            },
            dataType: "json",
            type: "POST",
            // handle a successful response
            error: function (json) {
                $('#id_product').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                toastr["error"](json.responseJSON.result)
            },

            success: function (json) {
                $('#id_product').val('');
                console.log(json);
                toastr["success"](json.result)

                // Quitar las la ultima fila de la tabla
                $('#tabla_ventas').prepend(
                    `<tr>
                    <th scope="row">` + json.sale_id +
                    `</th>
                    <td>` + json.product +
                    `</td>
                    <td>` + json.quantity +
                    `</td>
                    <td>` + json.sale_price +
                    `</td>
                    <td>` + json.total +
                    `</td>
                    <td>` + json.created_at +
                    `</td>
                    <td>` + json.seller +
                    `</td>
                </tr>`
                );
            },
        });
    });