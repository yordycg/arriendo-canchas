$(document).ready(function () {
  const $recursoSelector = $("#recurso_selector");
  const $fechaInput = $("#fecha");
  const $duracionSelect = $("#duracion");
  const $durationContainer = $("#duration-container");
  const $blocksContainer = $("#blocks-container");
  const $availabilitySection = $("#availability-section");
  const $noAvailability = $("#no-availability");
  const $summarySection = $("#summary-section");
  const $summaryText = $("#summary-text");
  const $horaInicioInput = $("#hora_inicio");
  const $horaFinInput = $("#hora_fin");
  const $recursoIdInput = $("#recurso_id");
  const $tipoInput = $("#tipo");

  // Al cambiar recurso, fecha o duración
  $recursoSelector.on("change", loadAvailability);
  $fechaInput.on("change", loadAvailability);
  $duracionSelect.on("change", loadAvailability);

  // Pre-selección desde URL (GET params)
  const urlParams = new URLSearchParams(window.location.search);
  const recursoIdParam = urlParams.get("recurso_id");
  const tipoParam = urlParams.get("tipo");

  if (recursoIdParam && tipoParam) {
    // Buscar la opción que coincida con tipo e ID
    $recursoSelector.find("option").each(function () {
      if (
        $(this).val() == recursoIdParam &&
        $(this).data("tipo") == tipoParam
      ) {
        $recursoSelector.val($(this).val());
        return false;
      }
    });
    // Disparar cambio manual
    loadAvailability();
  }

  function loadAvailability() {
    const recursoId = $recursoSelector.val();
    const $selected = $recursoSelector.find(":selected");
    const tipo = $selected.data("tipo");
    const fecha = $fechaInput.val();
    const isVip = $selected.data("vip");
    const duracion = $duracionSelect.val();

    // Mostrar/ocultar selector de duración solo para canchas
    if (tipo === "Cancha") {
      $durationContainer.removeClass("d-none");
    } else {
      $durationContainer.addClass("d-none");
      $duracionSelect.val("1"); // Reset a 1h para Quinchos
    }

    // Actualizar inputs ocultos
    $recursoIdInput.val(recursoId);
    $tipoInput.val(tipo);

    if (!recursoId || !fecha) return;

    // Mostrar loading o limpiar
    $blocksContainer.html(
      '<div class="col-12 text-center"><div class="spinner-border text-primary" role="status"></div></div>',
    );
    $availabilitySection.removeClass("d-none");
    $noAvailability.addClass("d-none");
    $summarySection.addClass("d-none");

    // Llamada AJAX
    $.ajax({
      url: AJAX_URL,
      data: {
        recurso_id: recursoId,
        tipo: tipo,
        fecha: fecha,
        duracion: duracion,
      },
      success: function (data) {
        $blocksContainer.empty();

        if (data.bloques.length === 0) {
          $availabilitySection.addClass("d-none");
          $noAvailability.removeClass("d-none");
          return;
        }

        data.bloques.forEach((bloque) => {
          const blockHtml = `
                        <div class="col-6 col-md-3">
                            <button type="button" class="btn btn-outline-primary w-100 py-3 block-btn"
                                    data-inicio="${bloque.inicio}" data-fin="${bloque.fin}">
                                <i class="bi bi-clock me-2"></i>${bloque.inicio} - ${bloque.fin}
                            </button>
                        </div>
                    `;
          $blocksContainer.append(blockHtml);
        });
      },
      error: function () {
        Swal.fire("Error", "No se pudo cargar la disponibilidad.", "error");
      },
    });
  }

  // Al seleccionar un bloque
  $(document).on("click", ".block-btn", function () {
    $(".block-btn")
      .removeClass("btn-primary text-white")
      .addClass("btn-outline-primary");
    $(this)
      .removeClass("btn-outline-primary")
      .addClass("btn-primary text-white");

    const inicio = $(this).data("inicio");
    const fin = $(this).data("fin");
    const recursoNombre = $recursoSelector.find(":selected").text();

    $horaInicioInput.val(inicio);
    $horaFinInput.val(fin);

    $summaryText.html(
      `Reserva para <strong>${recursoNombre}</strong> el día <strong>${$fechaInput.val()}</strong> de <strong>${inicio}</strong> a <strong>${fin}</strong>.`,
    );
    $summarySection.removeClass("d-none");
  });

  // Lógica para ver detalles
  $(document).on("click", ".btn-view-booking", function () {
    const d = $(this).data();
    let footerHtml = "";

    // Si la reserva está pendiente, mostrar botón de pago en el modal
    if (d.estado === "Pendiente") {
      footerHtml = `
                <hr>
                <div class="d-grid">
                    <button type="button" class="btn btn-success btn-pay-booking" 
                            data-url="${d.payUrl}" data-recurso="${d.recurso}" data-monto="${d.pago}">
                        <i class="bi bi-credit-card me-2"></i>Pagar Ahora
                    </button>
                </div>
            `;
    }

    const html = `
            <div class="text-start">
                <p><strong>Recurso:</strong> ${d.recurso} (${d.tipo})</p>
                <p><strong>Usuario:</strong> ${d.usuario} <span class="badge bg-info text-dark">${d.membresia}</span></p>
                <hr>
                <p><strong>Fecha:</strong> ${d.fecha}</p>
                <p><strong>Horario:</strong> ${d.horario}</p>
                <p><strong>Estado:</strong> <span class="badge bg-secondary">${d.estado}</span></p>
                <hr>
                <div class="d-flex justify-content-between align-items-center bg-light p-2 rounded">
                    <span>Precio Base:</span>
                    <span class="text-muted">$${d.base}</span>
                </div>
                <div class="d-flex justify-content-between align-items-center p-2 mt-1">
                    <span class="fw-bold text-dark">Total Pagado:</span>
                    <span class="fw-bold text-success fs-5">$${d.pago}</span>
                </div>
                <p class="small text-muted mt-2 text-center">* Descuento aplicado según membresía.</p>
                ${footerHtml}
            </div>
        `;

    Swal.fire({
      title: "Detalles de la Reserva",
      html: html,
      icon: "info",
      showConfirmButton: false,
      showCloseButton: true,
    });
  });

  // Lógica para pagar reserva
  $(document).on("click", ".btn-pay-booking", function () {
    const url = $(this).data("url");
    const recurso = $(this).data("recurso");
    const monto = $(this).data("monto");

    Swal.fire({
      title: "¿Confirmar Pago?",
      text: `¿Desea registrar el pago por $${monto} para la reserva de: ${recurso}?`,
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#198754",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sí, Pagar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = url;
      }
    });
  });

  // Lógica para cancelar reserva
  $(document).on("click", ".btn-cancel-booking", function () {
    const url = $(this).data("url");
    const recurso = $(this).data("recurso");

    Swal.fire({
      title: "¿Estás seguro?",
      text: `Vas a cancelar la reserva de: ${recurso}. Si lo haces fuera del plazo permitido (60 min normal / 30 min VIP), se aplicará una penalización.`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sí, cancelar",
      cancelButtonText: "Volver",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = url;
      }
    });
  });

  // Lógica para No-show
  $(document).on("click", ".btn-no-show-booking", function () {
    const url = $(this).data("url");
    const recurso = $(this).data("recurso");
    const usuario = $(this).data("usuario");

    Swal.fire({
      title: "¿Registrar Inasistencia?",
      html: `Vas a marcar como <strong>No Asistida</strong> la reserva de <strong>${usuario}</strong> en <strong>${recurso}</strong>.<br><br><span class="text-danger small"><i class="bi bi-exclamation-triangle"></i> Esto generará una multa automática y sumará una falta al usuario.</span>`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#f39c12",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Confirmar No-show",
      cancelButtonText: "Volver",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = url;
      }
    });
  });
});
