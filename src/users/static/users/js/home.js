$(document).ready(function () {
  function loadEconomicIndicators() {
    $.ajax({
      url: "https://mindicador.cl/api",
      method: "GET",
      dataType: "json",
      success: function (data) {
        const uf = data.uf.valor.toLocaleString("es-CL", {
          style: "currency",
          currency: "CLP",
        });
        const dolar = data.dolar.valor.toLocaleString("es-CL", {
          style: "currency",
          currency: "CLP",
        });
        const euro = data.euro.valor.toLocaleString("es-CL", {
          style: "currency",
          currency: "CLP",
        });
        const utm = data.utm.valor.toLocaleString("es-CL", {
          style: "currency",
          currency: "CLP",
        });

        const html = `
            <div class="ticker-item px-3 text-nowrap">
                <strong>UF:</strong> ${uf}
            </div>
            <div class="ticker-item px-3 text-nowrap">
                <strong>DÓLAR:</strong> ${dolar}
            </div>
            <div class="ticker-item px-3 text-nowrap">
                <strong>EURO:</strong> ${euro}
            </div>
            <div class="ticker-item px-3 text-nowrap">
                <strong>UTM:</strong> ${utm}
            </div>
            `;

        $("#indicators-list").html(html + html + html + html);
        // Duplicamos para efecto infinito si fuera necesario
      },
      error: function () {
        $("#indicators-list").html(`
            <span class="px-3 text-warning">Error al cargar indicadores</span>
        `);
      },
    });
  }

  $(".btn-delete").on("click", function () {
    const rut = $(this).data("rut");
    const nombre = $(this).data("nombre");

    Swal.fire({
      icon: "warning",
      title: "¿Estás seguro?",
      html: `
        <div class="alert alert-danger border-0 shadow-sm p-3 mb-3 text-start">
            <div class="d-flex align-items-center">
                <i class="bi bi-exclamation-triangle-fill fs-4 me-3"></i>
                <div>
                    <h6 class="alert-heading fw-bold mb-1">¡Atención!</h6>
                    <p class="mb-0 small">Esta acción marcará al usuario como <strong>inactivo</strong> en el sistema.</p>
                </div>
            </div>
        </div>
        <div class="card border-0 bg-light p-3 text-start">
            <div class="d-flex justify-content-between mb-1">
                <span class="text-muted small">USUARIO:</span>
                <span class="fw-bold">${nombre}</span>
            </div>
            <div class="d-flex justify-content-between">
                <span class="text-muted small">RUT:</span>
                <span class="fw-bold text-primary">${rut}</span>
            </div>
        </div>
      `,
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Sí, eliminar",
      cancelButtonColor: "#6c757d",
      cancelButtonText: "Cancelar",
      reverseButtons: true,
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `/users/delete/${rut}/`;
      }
    });
  });

  $(".btn-more").on("click", function () {
    const rut = $(this).data("rut");
    const nombres = $(this).data("nombres");
    const apellidos = $(this).data("apellidos");
    const sexo = $(this).data("sexo");
    const telefono = $(this).data("telefono");
    const email = $(this).data("email");
    const estado = $(this).data("estado");
    const rol = $(this).data("rol");
    const membresia = $(this).data("membresia");

    Swal.fire({
      icon: "info",
      title: `Detalles del Usuario`,
      html: `
        <div class="table-responsive">
          <table class="table table-sm table-hover border-0 text-start align-middle mt-2">
            <tbody>
              <tr>
                <th class="text-muted small ps-3 py-2" style="width: 40%">RUT</th>
                <td class="text-dark fw-bold py-2">${rut}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">NOMBRE COMPLETO</th>
                <td class="text-dark py-2">${nombres} ${apellidos}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">GÉNERO</th>
                <td class="text-dark py-2">${sexo}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">EMAIL</th>
                <td class="py-2"><a href="mailto:${email}" class="text-primary text-decoration-none fw-semibold">${email}</a></td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">TELÉFONO</th>
                <td class="text-dark py-2">${telefono}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">ROL</th>
                <td class="text-dark py-2">${rol}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">MEMBRESÍA</th>
                <td class="text-dark py-2">${membresia}</td>
              </tr>
              <tr>
                <th class="text-muted small ps-3 py-2">ESTADO</th>
                <td class="text-dark py-2">${estado}</td>
              </tr>
            </tbody>
          </table>
        </div>
      `,
      confirmButtonColor: "#0d6efd",
      confirmButtonText: "Cerrar Vista Previa",
      customClass: {
        popup: "rounded-4 shadow-lg",
      },
    });
  });

  loadEconomicIndicators();
  setInterval(loadEconomicIndicators, 3600000);
});
