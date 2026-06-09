$(document).ready(function () {
  // Formateo de Moneda CLP ------------------------------------------------------------------------
  function formatCLP() {
    $(".clp-format").each(function () {
      let element = $(this);
      let text = element.text().trim();

      let numericValue = text.replace(/[^\d]/g, ""); // limpiar todo lo que no sea numero

      if (numericValue !== "") {
        let value = parseInt(numericValue);
        if (!isNaN(value)) {
          const formatted = new Intl.NumberFormat("es-CL", {
            style: "currency",
            currency: "CLP",
            minimumFractionDigits: 0, // forzar que no tenga decimales
          }).format(value);
          element.text(formatted);
        }
      }
    });
  }

  formatCLP();

  // Re-formatear tras peticiones AJAX (search o filters)
  $(document).ajaxComplete(function () {
    formatCLP();
  });

  // SISTEMA DE INACTIVIDAD (SESIÓN) ---------------------------------------------------------------
  const idleTimeLimit = 180000; // 3 min de inactividad para mostrar alerta
  const warningTimeLimit = 120000; // 2 min adicionales para confirmar
  let idleTimer;
  let countdownInterval;

  function resetIdleTimer() {
    clearTimeout(idleTimer);
    // Iniciar el timer SOLO si el usuario esta logueado (existe el sidebar)
    if ($("#sidebar").length > 0) {
      idleTimer = setTimeout(showInactivityAlert, idleTimeLimit);
    }
  }

  function showInactivityAlert() {
    let secondsLeft = warningTimeLimit / 1000;

    Swal.fire({
      title: "¿Sigues ahí?",
      html: `Tu sesión expirará por inactividad en <strong><span id="session-countdown">${secondsLeft}</span></strong> segundos.`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#0d6efd",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Sí, seguir navegando",
      cancelButtonText: "Cerrar sesión",
      allowOutsideClick: false,
    }).then((result) => {
      if (result.isConfirmed) {
        // Refrescar sesión vía AJAX
        $.get("/core/session-refresh/", function () {
          clearInterval(countdownInterval);
          resetIdleTimer();
        });
      } else {
        // El usuario eligió salir
        window.location.href = "/auth/logout/";
      }
    });

    // Iniciar el contador visual en la alerta
    countdownInterval = setInterval(function () {
      secondsLeft--;
      $("#session-countdown").text(secondsLeft);
      if (secondsLeft <= 0) {
        clearInterval(countdownInterval);
        window.location.href = "/auth/logout/";
      }
    }, 1000);
  }

  // Detectar actividad para resetear el timer
  $(document).on("mousemove keydown click scroll touchstart", function () {
    resetIdleTimer();
  });

  // Iniciar el timer la primera vez
  resetIdleTimer();

  // Manejo de Alertas del Backend (sw_alert) ------------------------------------------------------
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
