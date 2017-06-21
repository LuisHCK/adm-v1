/*
$("form").submit(function(event) {
    event.preventDefault();
    $.ajax({
        url: "{% url 'agregar_articulo_factura' factura.id %}",
        data: {
                articulo: $('#id_product').val(),
                cantidad: $('#id_cantidad').val(),
                csrfmiddlewaretoken:'{{ csrf_token }}'
               },
        dataType: "json",
        type: "POST",
        // handle a successful response
        success : function(json) {
            $('#id_product-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

         success : function(json) {
            $('#id_product-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#tabla_factura').prepend("<tr><td>"+json.articulo+"</td><td>"+json.precio+"</td><td>"+json.cantidad+"</td><td><a class='btn btn-danger' href='/facturas/articulos/"+json.item_id+"/eliminar/'>Eliminar</a></td></tr>");
            document.getElementById("total_factura").innerHTML = json.total_factura;
        },
    });
});
*/
$('#codigo_articulo').on('input', function () {
    var cod = $(this).val();
    var url = $(this).attr('action')
    //Si el texto introducido supera los 3 caracteres realizar la búsqueda
    if (cod.length >= 4) {
        busqueda_articulos('../buscar_articulo/', cod)
    } else {
        // Si no hay texto introducido limpiar los resultados y cerrar el form
        limpiarBusquedas();
    }
});

// Búsqueda mediante ajax
function busqueda_articulos(url, codigo) {
    $.ajax({
        url: url + codigo,
        dataType: "json",
        type: "GET",

        success: function (json) {
            $("#lista-articulos").html('');
            $.each(json, function (i, obj) {
                $("#lista-articulos").append(`
                        <button id="` + obj.id +
                    `
                        " class="list-group-item list-art" precio="` +
                    obj.precio_venta +
                    `">
                            <span class="float-right">` + obj.nombre +
                    ` </span> <strong>&emsp;|&emsp;</strong> ` + obj.codigo +
                    `
                        </button>`)
            });
            console.log(json)
        },
        error: function (json) {
            console.log(json)
        }
    })
};

$("#lista-articulos").on("click", ".list-group-item", function () {
    // Obtener del item de resultado los valores el articulo
    var id = $(this).attr('id')
    var nombre = $(this).children("span").text()
    var precio = $(this).attr('precio')

    //Mandar los datos al formulario
    $("#id_product").val(parseInt(id))
    $("#nombre_articulo").html(nombre)
    $("#precio_articulo").html(precio)
    $("#form_agregar_articulo").fadeIn()
});

//Limpia el input de busqueda
$("#borrar_codigo").click(function () {
    $("#codigo_articulo").val('');
    limpiarBusquedas("#lista-articulos", "#form_agregar_articulo");
});

// Limpia los resultados y el formulario de artículos
function limpiarBusquedas(id1, id2) {
    $(id1).html("");
    $(id2).fadeOut();
}

// Agregar un artículo mediante ajax 
$("#form_agregar_articulo").on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            articulo: $("#id_product").val(),
            cantidad: $('#id_cantidad_articulo').val(),
            csrfmiddlewaretoken: $(this).attr('token')
        },
        dataType: "json",
        type: "POST",
        // handle a successful response
        error: function (json) {
            $('#id_product').val().replace('');
            console.log(json);
        },

        success: function (json) {
            $('#id_product').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#tabla_factura').prepend("<tr id='hide_item' style='display:none;'><td>" + json.articulo +
                "</td><td>" + json.precio + "</td><td>" + json.cantidad +
                "</td> <td>" + parseFloat(json.precio) * parseFloat(json.cantidad) + "</td> <td><a class='btn btn-danger' href='/facturas/articulos/" + json.item_id +
                "/eliminar/'>Eliminar</a></td></tr>");
            $('#hide_item').fadeIn('slow');
            document.getElementById("total_factura").innerHTML = json.total_factura;
        },
    });
});

// SERIVICIOS //
$('#codigo_producto').on('input', function () {
    var cod = $(this).val();
    var url = $(this).attr('action')
    //Si el texto introducido supera los 3 caracteres realizar la búsqueda
    if (cod.length >= 4) {
        buscar_servicio(cod)
    } else {
        // Si no hay texto introducido limpiar los resultados y cerrar el form
        limpiarBusquedas("#lista-servicios", "#agregar_servicio");
    }
});


function buscar_servicio(codigo) {
    $.ajax({
        url: "../buscar_servicio/" + codigo,
        dataType: "json",
        type: "GET",

        success: function (json) {
            $("#lista-servicios").html('');
            $.each(json, function (i, obj) {
                $("#lista-servicios").append(`
                        <button id="` + obj.id +
                    `
                        " class="list-group-item list-prod" precio="` +
                    obj.costo + `">
                            <span class="float-right">` +
                    obj.nombre + ` </span> <strong>&emsp;|&emsp;</strong> ` + obj.codigo +
                    `
                        </button>`)
            });
            console.log(json)
        },
        error: function (json) {
            console.log(json)
        }
    })
}

$("#lista-servicios").on("click", ".list-group-item", function () {
    var codigo = $(this).attr('id')
    var nombre = $(this).children("span").text()
    var precio = $(this).attr('precio')

    $("#nombre_producto").text(nombre)
    $("#precio_producto").text(precio)
    $("#id_tipo_servicio").val(parseInt(codigo))
    $("#agregar_servicio").fadeIn()
})

// Al cliquear el boton borrar quitar los resultados y el form
$("#borrar_codigo_p").on('click', function () {
    $("#codigo_producto").val('')
    limpiarBusquedas("#lista-servicios", "#agregar_servicio");
})


$("#agregar_servicio").submit(function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            tipo_servicio: $('#id_tipo_servicio').val(),
            cantidad: $('#cantidad_servicio').val(),
            csrfmiddlewaretoken: $(this).attr('token')
        },
        dataType: "json",
        type: "POST",
        // Si hay un error enviar un mensaje 
        error: function (json) {
            console.log(json); // ver en la consola el json enviado
            alert(json.responseJSON.result);
        },

        success: function (json) {
            $('#id_tipo_servicio').val('');
            $('#cantidad_servicio').val(1);
            console.log(json); // ver en la consola el json enviado
            console.log("success"); // Exito GG
            $('#tabla_factura').prepend("<tr id='hide_item' style='display:none;'><td>" + json.servicio +
                "</td><td>" + json.costo + "</td><td>" + json.cantidad +
                "</td> <td>" + parseFloat(json.costo) * parseFloat(json.cantidad) + "</td> <td><a class='btn btn-sm btn-danger' href='/facturas/servicios/" + json.item_id +
                "/eliminar/'>Eliminar</a></td></tr>");
            $('#hide_item').fadeIn('slow');
            document.getElementById("total_factura").innerHTML = json.total_factura;
        },
    });
});

/* ACCIONES PARA FACTURAS */
$("#cerrar-factura").submit(function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            fecha_limite: $('#fecha-limite').val(),
            csrfmiddlewaretoken: $(this).attr('token')
        },
        dataType: "json",
        type: "POST",
        // Si hay un error enviar un mensaje 
        error: function (json) {
            toastr['error'](json.responseJSON.result)
        },

        success: function (json) {
            window.location.replace('../'+json.id)            
            toastr['success'](json.result)            
        },
    });
});

$("#eliminar-factura").submit(function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            csrfmiddlewaretoken: $(this).attr('token')
        },
        dataType: "json",
        type: "POST",
        // Si hay un error enviar un mensaje 
        error: function (json) {
            toastr['error'](json.responseJSON.result)
        },

        success: function (json) {
            window.location.replace('../')
            toastr['success'](json.result)
        },
    });
});