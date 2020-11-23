const intro = introJs();
intro.setOptions({
    steps: [
        {
            element:'#step-uno',
            intro: 'Aqui puedes visualizar a los aspirantes',
        },
        {
            element:'#step-dos',
            intro: "Aqui subes su identificación oficial"
        },
        {
            element:'#step-tres',
            intro: 'Aqui subes su comprobante de domicilio',
        },
        {
            element:'#step-cuatro',
            intro: 'Aqui creas su contrato',
        },
        {
            element:'#step-cinco',
            intro: 'Aqui envias su contrato',
        },
        {
            element:'#step-seis',
            intro: 'Aqui puedes ver el proceso del aspirante',
        },
        {
            element:'#step-siete',
            intro: 'Aqui puedes preguntarle dudas a nuestro chat',
        },
        {
            element:'#step-ocho',
            intro: 'Aqui puedes visualizar el trabajo de los reclutadores',
        },
        {
            element:'#step-nueve',
            intro: 'Aqui te sales',
        }
    ]
})

intro.start();