$("form").submit(function(event) {
    event.preventDefault();
    $.ajax({
        url: "{% url 'agregar_articulo_factura' factura.id %}",
        data: {
                articulo: $('#id_articulo').val(),
                cantidad: $('#id_cantidad').val(),
                csrfmiddlewaretoken:'{{ csrf_token }}'
               },
        dataType: "json",
        type: "POST",
        // handle a successful response
        success : function(json) {
            $('#id_articulo-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

         success : function(json) {
            $('#id_articulo-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#tabla_factura').prepend("<tr><td>"+json.articulo+"</td><td>"+json.precio+"</td><td>"+json.cantidad+"</td><td><a class='btn btn-danger' href='/facturas/articulos/"+json.item_id+"/eliminar/'>Eliminar</a></td></tr>");
            document.getElementById("total_factura").innerHTML = json.total_factura;
        },
    });
});