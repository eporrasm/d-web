const pdfViewer1 = document.getElementById('pdf-viewer1');
const pdfViewer2 = document.getElementById('pdf-viewer2');

document.querySelector('form').addEventListener('submit', (event) => {
    
    event.preventDefault(); // Evita que se envíe el formulario
    const jsonInput = document.querySelector('#json_input').value; // Obtiene el valor del textarea
    
    const url = window.location.href+"api";
    (async () => {
      const rawResponse = await fetch(url, {
        method: 'POST',
        // headers: {
        //   'Content-Type': 'application/json'
        // },
        body: JSON.stringify(jsonInput)
      });
      const content = await rawResponse.json()
      console.log(content);

      pdfViewer1.src = "../output1#view=Fit&statusbar=0&messages=0&navpanes=0&scrollbar=0";
      pdfViewer2.src = "../output2#view=Fit&statusbar=0&messages=0&navpanes=0&scrollbar=0";
  });
});