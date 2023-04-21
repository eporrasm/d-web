const { Router } = require('express');
const router = Router();
const asignaturas = require('../sample.json');
const _ = require('underscore');

router.get('/', (req, res) => {
    res.status(200).json(asignaturas["asignaturas"]);
});

router.post('/', (req, res) => {
    const {nota, creditos, nombre, codigo, 
        tipologia, semestre, prerrequisitos, 
        estado, afecta_promedio} = req.body;
    if (creditos && nombre && codigo && 
        tipologia && semestre && 
        estado && afecta_promedio) {
        const newAsignatura = {...req.body};
        asignaturas["asignaturas"].push(newAsignatura);
        res.status(200).json(asignaturas["asignaturas"]);
    } else{
        res.status(500).json({error: 'There was an error.'});
    }
});

router.put('/:semestre/:codigo', (req, res) => {
    const semestre = parseInt(req.params.semestre);
    const codigo = req.params.codigo;
    const {nota, creditos, nombre,
        tipologia, prerrequisitos,
        estado, afecta_promedio} = req.body;
    if (creditos && nombre && codigo && 
        tipologia && semestre && 
        estado && afecta_promedio){
    _.each(asignaturas["asignaturas"], (asignatura, i) => {
        if (asignatura.semestre === semestre && 
            asignatura.codigo === codigo){
            asignatura.nota = nota;
            asignatura.creditos = creditos;
            asignatura.nombre = nombre;
            asignatura.tipologia = tipologia;
            asignatura.prerrequisitos = prerrequisitos;
            asignatura.estado = estado;
            asignatura.afecta_promedio = afecta_promedio;
        }
    });
    res.status(200).json(asignaturas["asignaturas"]);
    } else{
        res.status(500).json({error: 'There was an error.'});
    }
});

router.delete('/:semestre/:codigo', (req, res) => {
    const semestre = parseInt(req.params.semestre);
    const codigo = req.params.codigo;
    const index = _.findIndex(asignaturas["asignaturas"], 
                            function(asignatura) { return (asignatura.semestre === semestre && 
                                                asignatura.codigo === codigo) 
                        });
    asignaturas["asignaturas"].splice(index, 1);
    res.status(200).json(asignaturas["asignaturas"]);
});



module.exports = router;