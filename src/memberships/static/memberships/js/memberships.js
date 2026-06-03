$(document).ready(function () {
  // Manejo de eliminación de Membresías
  $(".btn-delete-membership").on("click", function () {
    const id = $(this).data("id");
    const nombre = $(this).data("nombre");

    Swal.fire({
      icon: "warning",
      title: "¿Eliminar Membresía?",
      html: `
        <div class="alert alert-danger border-0 shadow-sm p-3 mb-3 text-start">
            <div class="d-flex align-items-center">
                <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                <div>
                    <h6 class="alert-heading fw-bold mb-1">¡Atención!</h6>
                    <p class="mb-0 small">El plan <strong>${nombre}</strong> quedará inactivo y no podrá ser asignado a nuevos usuarios.</p>
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
        window.location.href = `/memberships/delete/${id}/`;
      }
    });
  });
});
