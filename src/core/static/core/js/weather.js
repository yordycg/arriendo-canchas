$(document).ready(function () {
  function loadWeather() {
    const CODE = "SCGE"; // ciudad - Los Angeles, Chile
    const URL = `https://api.boostr.cl/weather/${CODE}.json`;

    $.ajax({
      url: URL,
      type: "GET",
      dataType: "json",
      // destructure object
      success: function ({ data }) {
        if (data) {
          // const CITY = "Los Angeles, Chile"; // output city = 'Loas Angeles'
          const CONDITION = data.condition;
          const HUMIDITY = data.humidity;
          const TEMP = data.temperature;
          const UPDATED_AT = data.updated_at;

          // Inyectar datos en el HTML
          $("#weather-temp").html(`${Math.round(TEMP)}&deg;C`);
          $("#weather-state").text(CONDITION);
          $("#weather-humidity").text(`${HUMIDITY}%`);
          // Formatear hora
          const TIME = UPDATED_AT.substring(0, 5); // output: 10:00:00 -> now: 10:00
          $("#weather-time").text(TIME);
        }
      },
      error: function (error) {
        console.error(`Error API CLima: ${error}`);
        $("#weather-state").text("Servicio no disponible");
      },
    });
  }

  loadWeather();
});
