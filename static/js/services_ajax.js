    $("#form_service").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            data: {
                type_service: $('#id_tipo_servicio').val(),
                quantity: $('#cantidad_servicio').val(),
                csrfmiddlewaretoken: $(this).attr('token')
            },
            dataType: "json",
            type: "POST",
            // handle a successful response
            error: function (json) {
                $('#id_product').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("Error al realizar la sale");
                toastr["error"](json.responseJSON.result)
            },

            success: function (json) {
                $('#id_product').val('');
                console.log(json);
                console.log("success");
                toastr["success"](json.result)

                // Quitar las la ultima fila de la tabla
                $('#tabla_servicios').prepend(
                    `<tr>
                        <th scope="row">`+ json.service_id +`</th>
                        <td>`+ json.service +`</td>
                        <td>`+ json.quantity +`</td>
                        <td>`+ json.service_price +`</td>
                        <td>`+ json.total +`</td>
                        <td>`+ json.seller +`</td>
                        <td>`+ json.created_at +`</td>
                        <td><a href="#" class="btn btn-outline-primary">Detalles</a></td>
                        
                    </tr>`
                );

                $('#tabla_servicios tr:last').remove();
            },
        });
    });


$(document).ready(function () {
    $(".ActivateService").click(function () {
        event.preventDefault();
        var link = $(this).attr('href');
        var act = $(this).attr('activar');
        var typ

        if (act == "True"){
            typ = "POST"
        }
        else{
            typ = "UPDATE"
        }

        $.ajax({
            type: typ,
            dataType: "json",
            url: link,
            data: {
                csrfmiddlewaretoken: $(this).attr('token')
                },
            error: function (json) {
                console.log(json); // log the returned json to the console
                console.log("Error al realizar la sale");
                toastr["error"](json.result)
            },
            success: function (json) {
                console.log(json); // log the returned json to the console
                console.log("Error al realizar la sale");
                toastr["success"](json.result)
            },
        });
    });
});