


const pdfViewer1 = document.getElementById('pdf-viewer1');
const pdfViewer2 = document.getElementById('pdf-viewer2');
const outputDiv = document.getElementById('output_div');

document.querySelector('form').addEventListener('submit', (event) => {

    event.preventDefault(); // Evita que se envíe el formulario
    const jsonInput = document.querySelector('#json_input').value; // Obtiene el valor del textarea
    const evalJson = validarJson(jsonInput);
    if (evalJson === "paila mi parapapa"){
    const url = window.location.href+"api";
    (async () => {
      const rawResponse = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: jsonInput
      });
      const content = await rawResponse.json();
    
      console.log(content);
    })();

      // pdfViewer1.src = "../output1#view=Fit&statusbar=0&messages=0&navpanes=0&scrollbar=0";
      // pdfViewer2.src = "../output2#view=Fit&statusbar=0&messages=0&navpanes=0&scrollbar=0";

      if (pdfViewer1.src === "" && pdfViewer2.src === ""){
        pdfViewer1.src = "../output1";
        pdfViewer2.src = "../output2";
      }else{
        pdfViewer1.src = pdfViewer1.src;
        pdfViewer2.src = pdfViewer2.src;
      }
      outputDiv.style.display = "block";
      outputDiv.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "nearest"
      });
}
else {
  alert(evalJson);
};
});


function validarJson(json) {
  try {
      const obj = JSON.parse(json);
      var valid_keys = [ "asignaturas", "creditos_opt_disc", "creditos_opt_fund" ];
      var keys = Object.keys(obj).sort();
      if (JSON.stringify(keys)!==JSON.stringify(valid_keys)){
        return "Se requieren estrictamente los campos: asignaturas, creditos_opt_disc y creditos_opt_fund";
      }
      if (obj.creditos_opt_fund !== null && !(typeof obj.creditos_opt_fund === 'number')){
        return `creditos_opt_fund debe ser un número`
      }

      if (obj.creditos_opt_disc !== null && !(typeof obj.creditos_opt_disc === 'number')){
        return `creditos_opt_disc debe ser un número`
      }

      for (let i = 0; i < obj.asignaturas.length; i++) {
          const asignatura = obj.asignaturas[i];
          if (!asignatura.nombre || !asignatura.codigo || !asignatura.tipologia) {
            return `Las asignaturas deben tener nombre, código y tipología (asignatura ${i+1})`
          }
          if (!(typeof asignatura.nombre === 'string') && !(asignatura.nombre instanceof String)){
            return `${asignatura.nombre} debe ser una palabra`
          }
          if (!(typeof asignatura.tipologia === 'string') && !(asignatura.tipologia instanceof String)){
            return `La tipologia de ${asignatura.nombre}: ${asignatura.tipologia} debe ser una palabra`
          }
          if (!(typeof asignatura.codigo === 'string') && !(asignatura.codigo instanceof String)){
            return `La tipologia de ${asignatura.nombre}: ${asignatura.tipologia} debe ser una palabra`
          }
          if (asignatura.nota !== null && !(typeof asignatura.nota === 'number')){
            return `La nota de ${asignatura.nombre}: ${asignatura.nota} debe ser un número`
          }
          if (!(typeof asignatura.creditos === 'number')){
            return `Los créditos de ${asignatura.nombre}: ${asignatura.creditos} debe ser un número`
          }
          if (asignatura.nota !== null && (isNaN(asignatura.nota) || asignatura.nota < 0 || asignatura.nota > 5)) {
            return `${asignatura.nombre} debe tener una nota entre 0.0 y 5.0`
          }
          if (isNaN(asignatura.creditos) || asignatura.creditos < 1 || !Number.isInteger(asignatura.creditos)) {
            return `${asignatura.nombre} tiene una cantidad errada de créditos`
          }
          if (!["fundamentacion_optativa", "fundamentacion_obligatoria", "disciplinar_optativa", "disciplinar_obligatoria", "nivelacion", "libre_eleccion"].includes(asignatura.tipologia)) {
            return `${asignatura.nombre} tiene una tipología errónea: ${asignatura.tipologia}`
          }
          if (asignatura.semestre !== null && isNaN(asignatura.semestre)) {
            return `${asignatura.nombre} debe tener un número positivo en su campo de semestre`
          }
          if (asignatura.semestre === null && (asignatura.nota !== null || asignatura.estado !== null)) {
            return `${asignatura.nombre} tiene semestre null, luego su nota y estado deben ser null`
          }
          if (asignatura.estado === "cancelada" && asignatura.nota !== null) {
            return `${asignatura.nombre} tiene estado cancelada, luego su nota debe ser null`
          }
      }
      return "paila mi parapapa";
  } catch (e) {
      return "Debes ingresar un JSON válido";
  }
}

function validarNota(nota) {
  if (nota === null) {
    return true;
  }
  return typeof nota === 'number' && nota >= 0 && nota <= 5;
}

function validarSemestre(semestre, nota, estado) {
  if (semestre === null) {
    return nota === null && estado === null;
  }
  return true;
}

function validarEstado(estado, nota) {
  if (estado === 'cancelada') {
    return nota === null;
  }
  return estado !== null;
}

