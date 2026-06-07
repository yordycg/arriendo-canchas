$(document).ready(function() {
    // Función para obtener y mostrar el clima
    function loadWeather() {
        // Mostrar estado de carga (opcional, ya está por defecto en el HTML)
        $('#weather-temp').text('...');
        $('#weather-state').text('Cargando...');

        $.ajax({
            url: 'https://api.gael.cloud/general/public/clima',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Filtrar los datos para encontrar la estación de Concepción
                const concepcionWeather = data.find(function(station) {
                    return station.Estacion === 'Concepción';
                });

                if (concepcionWeather) {
                    // Actualizar el DOM con los datos recibidos
                    $('#weather-temp').html(`${concepcionWeather.Temp}&deg;C`);
                    $('#weather-state').text(concepcionWeather.Estado);
                    $('#weather-humidity').text(`${concepcionWeather.Humedad}%`);
                    $('#weather-time').text(concepcionWeather.HoraUpdate);
                    
                    // Cambiar icono según el estado (básico)
                    const state = concepcionWeather.Estado.toLowerCase();
                    let iconClass = 'bi-cloud-sun'; // Default
                    if (state.includes('despejado')) {
                        iconClass = 'bi-sun text-warning';
                    } else if (state.includes('lluvia') || state.includes('chubascos')) {
                        iconClass = 'bi-cloud-rain text-info';
                    } else if (state.includes('nublado')) {
                        iconClass = 'bi-clouds text-secondary';
                    }
                    
                    $('#weather-icon').removeClass().addClass(`bi ${iconClass} display-4`);

                } else {
                    $('#weather-state').text('No disponible');
                    $('#weather-temp').text('--');
                }
            },
            error: function(xhr, status, error) {
                console.error("Error al obtener el clima:", error);
                $('#weather-state').text('Error de conexión');
                $('#weather-temp').text('--');
            }
        });
    }

    // Cargar clima al iniciar
    loadWeather();
});