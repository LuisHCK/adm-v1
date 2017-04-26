$(document).ready(function () {
    $("#vender").click(function () {
        $("#form_vender").toggle(500);
    });
    $("#servicio").click(function () {
        $("#form_servicio").toggle(500);
    });
    $("#abrirfact").click(function () {
        $("#form_factura").toggle(500);
    });
    $("#primera_apertura").click(function () {
        $("#form_primera_apertura").toggle(500);
    });
    $("#cierre_caja").click(function () {
        $("#cierre_form").toggle(500);
    });
    $("#btn_egreso").click(function () {
        $("#form_egreso").toggle(500);
    });
});