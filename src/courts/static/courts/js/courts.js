$(document).ready(function () {
  // Manejo de eliminación de Canchas
  $(".btn-delete-court").on("click", function () {
    const id = $(this).data("id");
    const nombre = $(this).data("nombre");

    Swal.fire({
      icon: "warning",
      title: "¿Eliminar Cancha?",
      html: `
        <div class="alert alert-danger border-0 shadow-sm p-3 mb-3 text-start">
            <div class="d-flex align-items-center">
                <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                <div>
                    <h6 class="alert-heading fw-bold mb-1">¡Atención!</h6>
                    <p class="mb-0 small">La cancha <strong>${nombre}</strong> quedará inactiva y no podrá ser reservada.</p>
                </div>
            </div>
        </div>
      `,
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Sí, desactivar",
      cancelButtonColor: "#6c757d",
      cancelButtonText: "Cancelar",
      reverseButtons: true,
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `/courts/delete/${id}/`;
      }
    });
  });

  // Manejo de eliminación de Quinchos
  $(".btn-delete-pavilion").on("click", function () {
    const id = $(this).data("id");
    const nombre = $(this).data("nombre");

    Swal.fire({
      icon: "warning",
      title: "¿Eliminar Quincho?",
      html: `
        <div class="alert alert-danger border-0 shadow-sm p-3 mb-3 text-start">
            <div class="d-flex align-items-center">
                <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                <div>
                    <h6 class="alert-heading fw-bold mb-1">¡Atención!</h6>
                    <p class="mb-0 small">El quincho <strong>${nombre}</strong> quedará inactivo para futuras reservas.</p>
                </div>
            </div>
        </div>
      `,
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Sí, desactivar",
      cancelButtonColor: "#6c757d",
      cancelButtonText: "Cancelar",
      reverseButtons: true,
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `/courts/pavilions/delete/${id}/`;
      }
    });
  });
});
