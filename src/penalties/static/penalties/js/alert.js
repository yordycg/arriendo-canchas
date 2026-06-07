$(document).ready(function () {
  // 1. Manejo de Alertas del Backend (sw_alert)
  const swDataElement = $("#sw-data");

  if (swDataElement.length > 0) {
    const data = JSON.parse(swDataElement.text());

    Swal.fire({
      icon: data.type,
      title: data.title,
      text: data.message,
      confirmButtonColor: "#0d6efd",
      confirmButtonText: "Aceptar",
    }).then((result) => {
      if (data.redirect && result.isConfirmed) {
        window.location.href = data.redirect;
      }
    });
  }

  // 2. Manejo de Interacciones de Penalizaciones (Centralizado)

  // Registro de pago por Admin/Recepcionista
  $(document).on("click", ".btn-pay-admin", function () {
    const id = $(this).data("id");
    const usuario = $(this).data("usuario");
    const monto = $(this).data("monto");

    Swal.fire({
      title: "¿Registrar Pago?",
      text: `Se marcará como pagada la multa de $${monto} para ${usuario}.`,
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#198754",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Sí, pagar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "/penalties/pay/" + id + "/";
      }
    });
  });

  // Pago realizado por el Cliente
  $(document).on("click", ".btn-pay-client", function () {
    const id = $(this).data("id");
    const monto = $(this).data("monto");

    Swal.fire({
      title: "¿Proceder al pago?",
      text: `Serás redirigido a la pasarela de pago para cancelar tu multa de $${monto}.`,
      icon: "info",
      showCancelButton: true,
      confirmButtonColor: "#0d6efd",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Ir a pagar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "/penalties/pay/" + id + "/";
      }
    });
  });

  // Eliminación de penalización (Solo Admin)
  $(document).on("click", ".btn-delete-penalty", function () {
    const id = $(this).data("id");

    Swal.fire({
      title: "¿Eliminar Penalización?",
      text: "Esta acción no se puede deshacer y borrará el registro permanente.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dc3545",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "/penalties/delete/" + id + "/";
      }
    });
  });
});
