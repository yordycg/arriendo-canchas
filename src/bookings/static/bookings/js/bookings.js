$(document).ready(function () {
  const $recursoSelector = $("#recurso_selector");
  const $fechaInput = $("#fecha");
  const $blocksContainer = $("#blocks-container");
  const $availabilitySection = $("#availability-section");
  const $noAvailability = $("#no-availability");
  const $summarySection = $("#summary-section");
  const $summaryText = $("#summary-text");
  const $horaInicioInput = $("#hora_inicio");
  const $horaFinInput = $("#hora_fin");
  const $recursoIdInput = $("#recurso_id");
  const $tipoInput = $("#tipo");

  // Al cambiar recurso o fecha
  $recursoSelector.on("change", loadAvailability);
  $fechaInput.on("change", loadAvailability);

  function loadAvailability() {
    const recursoId = $recursoSelector.val();
    const tipo = $recursoSelector.find(":selected").data("tipo");
    const fecha = $fechaInput.val();
    const isVip = $recursoSelector.find(":selected").data("vip");

    // Actualizar inputs ocultos
    $recursoIdInput.val(recursoId);
    $tipoInput.val(tipo);

    if (!recursoId || !fecha) return;

    // Validación básica de VIP en Frontend
    if (
      isVip &&
      USER_ROL === "Cliente" &&
      !confirm(
        "Este recurso es SOLO VIP. ¿Desea continuar? (El sistema validará su membresía)",
      )
    ) {
      $recursoSelector.val("");
      return;
    }

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
                                <i class="bi bi-clock me-2"></i>${bloque.inicio}
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
});
