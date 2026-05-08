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
    const name = $(this).data("nombre");

    confirmDelete(rut, name);
  });

  function confirmDelete(rut, nombre) {
    Swal.fire({
      title: "Estas seguro?",
      text: `Vas a "eliminar" al usuario: ${nombre}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Si, eliminar",
      cancelButtonColor: "#3085d6",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `/users/delete/?rut=${rut}`;
      }
    });
  }

  loadEconomicIndicators();
  setInterval(loadEconomicIndicators, 3600000);
});
