function enlazarListas(idPadre, idHija, urlModelo) {
    const padre = document.getElementById(idPadre);
    const hija = document.getElementById(idHija);

    padre.addEventListener("change", async function () {
        hija.innerHTML = '<option value="">-- Selecciona --</option>';
        if (!padre.value) return;

        const url = urlModelo.replace("/0/", "/" + padre.value + "/");
        const respuesta = await fetch(url);
        const opciones = await respuesta.json();

        for (const item of opciones) {
            const opcion = document.createElement("option");
            opcion.value = item.id;
            opcion.textContent = item.nombre;
            hija.appendChild(opcion);
        }
    });
}
