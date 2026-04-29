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

        // $("#indicators-list").html(html + html);
        // Duplicamos para efecto infinito si fuera necesario
      },
      error: function () {
        $("#indicators-list").html(`
            <span class="px-3 text-warning">Error al cargar indicadores</span>
        `);
      },
    });
  }
  loadEconomicIndicators();
  setInterval(loadEconomicIndicators, 3600000);
});
