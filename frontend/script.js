document.getElementById("formulario").addEventListener("submit", async function(e) {
  e.preventDefault();
  const data = {
    edad: parseInt(document.getElementById("edad").value),
    sexo: document.getElementById("sexo").value,
    peso: parseFloat(document.getElementById("peso").value),
    altura: parseFloat(document.getElementById("altura").value),
    actividad: document.getElementById("actividad").value
  };

  const resCal = await fetch("http://localhost:8000/calcular", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const cal = await resCal.json();

  const resIMC = await fetch("http://localhost:8000/imc", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const imc = await resIMC.json();

  document.getElementById("resultados").innerHTML = `
    <p><strong>Calorías diarias:</strong> Mantener: ${cal.mantener}, Subir: ${cal.subir}, Bajar: ${cal.bajar}</p>
    <p><strong>IMC:</strong> ${imc.valor_imc} (${imc.categoria})</p>
  `;
});
