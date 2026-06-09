$(document).ready(function () {
  // 0. Formateo de Moneda CLP
  function formatCLP() {
    $(".clp-format").each(function () {
      let element = $(this);
      let text = element.text().trim();

      // Limpiar todo lo que no sea número
      let numericValue = text.replace(/[^\d]/g, "");

      if (numericValue !== "") {
        let value = parseInt(numericValue);
        if (!isNaN(value)) {
          // Formato forzado con puntos (estándar chileno/alemán)
          let formatted = new Intl.NumberFormat("de-DE").format(value);
          element.text("$" + formatted);
        }
      }
    });
  }

  // Ejecutar inmediatamente
  formatCLP();

  // Re-formatear tras peticiones AJAX (ej: buscador o filtros)
  $(document).ajaxComplete(function () {
    formatCLP();
  });

  // 1. Manejo de Alertas del Backend (sw_alert)
  const swDataElement = $("#sw-data");

  if (swDataElement.length > 0) {
    const data = JSON.parse(swDataElement.text());

    Swal.fire({
      icon: data.type,
      title: data.title,
      html: data.message,
      confirmButtonColor: "#0d6efd",
      confirmButtonText: "Aceptar",
    }).then((result) => {
      if (data.redirect && (result.isConfirmed || result.isDismissed)) {
        window.location.href = data.redirect;
      }
    });
  }
});
