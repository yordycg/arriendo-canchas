$(document).ready(function () {
  const rolSelect = $("#rol_id");
  const membresiaSelect = $("#membresia_id");
  const membresiaLabel = $('label[for="membresia_id"]');

  /**
   * Maneja el estado del selector de membresía basado en el rol seleccionado.
   * Admin (1) e Invitado (4) no pueden tener membresía.
   */
  function handleRolChange() {
    const rolVal = parseInt(rolSelect.val());
    const isRestricted = [1, 4].includes(rolVal);

    if (isRestricted) {
      membresiaSelect
        .prop("disabled", true)
        .prop("required", false)
        .css({
          opacity: "0.6",
          cursor: "not-allowed",
          "background-color": "#e9ecef",
        })
        .val("");

      membresiaLabel.css({
        color: "#6c757d",
        cursor: "not-allowed",
      });
    } else {
      membresiaSelect.prop("disabled", false).prop("required", true).css({
        opacity: "1",
        cursor: "default",
        "background-color": "#fff",
      });

      membresiaLabel.css({
        color: "#212529",
        cursor: "default",
      });

      // Si antes estaba deshabilitado, poner 'Normal' (1) por defecto
      if (!membresiaSelect.val()) {
        membresiaSelect.val("1");
      }
    }
  }

  // Escuchar cambios y ejecutar una vez al cargar
  rolSelect.on("change", handleRolChange);
  handleRolChange();
});
