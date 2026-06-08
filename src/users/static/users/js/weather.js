$(document).ready(function() {
    function loadWeather() {
        const lat = -37.4697;
        const lon = -72.3539;
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&timezone=auto`;

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data && data.current_weather) {
                    const current = data.current_weather;
                    
                    // Actualizar Temperatura
                    $('#weather-temp').html(`${Math.round(current.temperature)}&deg;C`);
                    
                    // Actualizar Viento (En vez de humedad, ya que Open-Meteo current lo da más fácil)
                    $('#weather-humidity').text(`${current.windspeed} km/h`);
                    
                    // Hora de actualización
                    const now = new Date();
                    const timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
                    $('#weather-time').text(timeStr);

                    // Interpretar Código de Clima WMO
                    const code = current.weathercode;
                    let stateText = "Despejado";
                    let iconClass = "bi-sun text-warning";

                    if (code >= 1 && code <= 3) {
                        stateText = "Parcialmente Nublado";
                        iconClass = "bi-cloud-sun text-primary";
                    } else if (code >= 45 && code <= 48) {
                        stateText = "Neblina";
                        iconClass = "bi-cloud-fog text-secondary";
                    } else if (code >= 51 && code <= 67) {
                        stateText = "Lluvia";
                        iconClass = "bi-cloud-rain text-info";
                    } else if (code >= 71 && code <= 77) {
                        stateText = "Nieve";
                        iconClass = "bi-cloud-snow text-light";
                    } else if (code >= 80 && code <= 82) {
                        stateText = "Chubascos";
                        iconClass = "bi-cloud-drizzle text-info";
                    } else if (code >= 95) {
                        stateText = "Tormenta Eléctrica";
                        iconClass = "bi-cloud-lightning-rain text-dark";
                    }

                    $('#weather-state').text(stateText);
                    $('#weather-icon').removeClass().addClass(`bi ${iconClass} display-4`);

                }
            },
            error: function(xhr, status, error) {
                console.error("Error al obtener el clima de Los Ángeles:", error);
                $('#weather-state').text('Error de conexión');
            }
        });
    }

    loadWeather();
});