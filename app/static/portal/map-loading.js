(function () {
  const screen = document.getElementById("mapLoading");
  if (!screen) return;

  const title = document.getElementById("mapLoadingTitle");
  const detail = document.getElementById("mapLoadingDetail");
  const retry = document.getElementById("mapLoadingRetry");

  retry.addEventListener("click", function () {
    window.location.reload();
  });

  window.MapLoading = {
    finish: function () {
      screen.setAttribute("aria-busy", "false");
      screen.classList.add("is-hidden");
      window.setTimeout(function () {
        screen.hidden = true;
      }, 350);
    },
    fail: function (message) {
      title.textContent = "No se pudo cargar el mapa";
      detail.textContent = message || "Comprueba la conexión e inténtalo de nuevo.";
      retry.hidden = false;
      screen.classList.add("is-error");
      screen.setAttribute("aria-busy", "false");
    },
  };
})();
