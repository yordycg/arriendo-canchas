$(document).ready(function () {
  const swDataElement = $("#sw-data");

  if (swDataElement.length > 0) {
    const data = JSON.parse(swDataElement.text());

    Swal.fire({
      icon: data.type,
      title: data.title,
      text: data.message,
      confirmButtonColor: "#0d6efd",
      confirmButtonText: "Aceptar",
    }).then((result) => {
      if (data.redirect && result.isConfirmed) {
        window.location.href = data.redirect;
      }
    });
  }
});
