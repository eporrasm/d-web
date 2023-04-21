const { Router } = require('express');
const asignaturas = require('../sample.json');
const bodyParser = require('body-parser');
const fs = require('fs');
const { spawn } = require('child_process');
const _ = require('underscore');

const router = Router();

router.post('/', (req, res) => {
    const input = req.body;

    // Generate filename for the input JSON file
    const inputFilename = "input.json";

    // Write the input JSON to a file
    fs.writeFileSync(inputFilename, JSON.stringify(input));

    // Generate filename for the output PDF file
    const outputFilename = "output.pdf";

    // Run the Python script with the input and output filenames as arguments
    const pyprog = spawn('python', ['my_script.py', inputFilename, outputFilename]);

    // Send the output PDF as a file download when the Python script finishes
    pyprog.on('close', (code) => {
    const outputPdf = fs.readFileSync(outputFilename);
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename=${outputFilename}`);
    res.send(outputPdf);

    // Clean up the input and output files
    fs.unlinkSync(inputFilename);
    fs.unlinkSync(outputFilename);
  });
});


module.exports = router;