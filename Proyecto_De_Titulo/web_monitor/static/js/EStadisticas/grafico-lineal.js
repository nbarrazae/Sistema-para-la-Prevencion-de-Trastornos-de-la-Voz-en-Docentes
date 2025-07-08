    //const resultados = {{ resultados_json|safe }};
    console.log("Resultados JSON:", resultados);
    const extraerRegistros = (clave) => resultados.flatMap(h => h[clave] || []);

    const crearGraficoPlotly = (divId, titulo, todosLosDatos, campoDatos, campoValor, coloresBase) => {
        const datosPorAula = {};

        todosLosDatos.forEach(horario => {
            const aula = horario.id_aula || 'Desconocido';
            const registros = horario[campoDatos] || [];

            if (!datosPorAula[aula]) datosPorAula[aula] = [];

            registros.forEach(r => {
                if (r[campoValor] !== undefined) {
                    datosPorAula[aula].push({
                        x: r.fecha_hora,
                        y: r[campoValor],
                    });
                }
            });
        });

        const aulas = Object.keys(datosPorAula);
        const colores = coloresBase || [
            'blue', 'orange', 'green', 'red', 'purple', 'brown', 'teal', 'pink', 'gray', 'black'
        ];

        const data = aulas.map((aula, idx) => ({
            x: datosPorAula[aula].map(p => p.x),
            y: datosPorAula[aula].map(p => p.y),
            name: aula,
            mode: 'lines',
            line: { color: colores[idx % colores.length] },
            connectgaps: false
        }));

        const hayDatos = data.some(trace => trace.x.length > 0 && trace.y.length > 0);

        const SHAPE_GAP_THRESHOLD_MINUTES = 5;
        const parseFecha = str => new Date(str).getTime();
        const detectarCortes = () => {
            const shapes = [];
            aulas.forEach((aula, idx) => {
                const puntos = datosPorAula[aula];
                if (puntos.length < 2) return;

                for (let i = 1; i < puntos.length; i++) {
                    const t1 = parseFecha(puntos[i - 1].x);
                    const t2 = parseFecha(puntos[i].x);
                    const deltaMin = (t2 - t1) / (1000 * 60);
                    if (deltaMin > SHAPE_GAP_THRESHOLD_MINUTES) {
                        shapes.push({
                            type: 'rect',
                            x0: puntos[i].x,
                            x1: puntos[i].x,
                            yref: 'paper',
                            y0: 0,
                            y1: 1,
                            line: {
                                color: 'rgba(150,150,150,0.5)',
                                width: 2,
                                dash: 'dot'
                            }
                        });
                    }
                }
            });
            return shapes;
        };

        const layout = hayDatos ? {
            width: 12000,
            title: titulo,
            xaxis: {
                title: 'Fecha y Hora',
                tickangle: -45,
                tickmode: 'auto',
                nticks: 40
            },
            yaxis: { title: campoValor },
            shapes: detectarCortes(),
            autosize: true,
            height: 400,
            margin: { t: 50, b: 50 },
            legend: { orientation: "h", x: 0, y: -0.2 }
        } : {
            title: titulo,
            xaxis: { visible: false },
            yaxis: { visible: false },
            annotations: [
                {
                    text: "Sin datos disponibles",
                    xref: "paper",
                    yref: "paper",
                    showarrow: false,
                    font: { size: 20, color: "gray" },
                    x: 0.5,
                    y: 0.5,
                    align: "center"
                }
            ],
            autosize: true,
            height: 400,
            margin: { t: 50, b: 50 }
        };

        Plotly.newPlot(divId, data, layout);
    };

    crearGraficoPlotly('graficoFrecuencia', 'Frecuencia Fundamental (Hz)', resultados, 'registros_voz', 'freq', ['#1f77b4', '#ff7f0e']);
    crearGraficoPlotly('graficoIntensidad', 'Intensidad de Voz (dB)', resultados, 'registros_voz', 'intensidad', ['#2ca02c', '#d62728']);
    crearGraficoPlotly('graficoRuido', 'Ruido Ambiental (dB)', resultados, 'registros_ruido', 'ruido');
    crearGraficoPlotly('graficoTemperatura', 'Temperatura (°C)', resultados, 'registros_temperatura', 'temperatura');
    crearGraficoPlotly('graficoHumedad', 'Humedad Relativa (%)', resultados, 'registros_humedad', 'humedad');
    crearGraficoPlotly('graficoCO2', 'CO₂ (ppm)', resultados, 'registros_co2', 'co2');



    
    function convertirDatosAExcelPorVariable(resultados_json) {
        const variables = [
            { nombre: 'Frecuencia (Hz)', clave: 'registros_voz', campo: 'freq' },
            { nombre: 'Intensidad (dB)', clave: 'registros_voz', campo: 'intensidad' },
            { nombre: 'Ruido (dB)', clave: 'registros_ruido', campo: 'ruido' },
            { nombre: 'Temperatura (°C)', clave: 'registros_temperatura', campo: 'temperatura' },
            { nombre: 'Humedad (%)', clave: 'registros_humedad', campo: 'humedad' },
            { nombre: 'CO₂ (ppm)', clave: 'registros_co2', campo: 'co2' }
        ];

        const hojas = {};

        variables.forEach(variable => {
            const data = [];
            resultados_json.forEach(item => {
                const registros = item[variable.clave] || [];
                registros.forEach((registro, index) => {
                    data.push({
                        'Fecha y Hora': registro.fecha_hora,
                        'Aula': item.id_aula || 'Desconocido',
                        [variable.nombre]: registro[variable.campo] !== undefined ? registro[variable.campo] : ''
                    });
                });
            });
            hojas[variable.nombre] = data;
        });

        return hojas;
    }

    // Función para exportar a Excel con múltiples hojas
    function exportarAExcelPorVariable() {
        const hojas = convertirDatosAExcelPorVariable(resultados); // Usar "resultados" que ya está definido en el template

        // Crea un nuevo libro
        const wb = XLSX.utils.book_new();

        // Agrega cada hoja al libro
        Object.keys(hojas).forEach(nombreHoja => {
            const ws = XLSX.utils.json_to_sheet(hojas[nombreHoja]);
            XLSX.utils.book_append_sheet(wb, ws, nombreHoja);
        });

        // Obtiene la fecha y hora actual en formato "YYYY-MM-DD_HH-MM-SS"
        const fechaActual = new Date();
        const fechaHoraActual = fechaActual.toISOString().replace(/T/, '_').replace(/:/g, '-').split('.')[0];

        // Genera el archivo Excel y lo descarga con la fecha y hora actual en el nombre
        const nombreProfesor = resultados[0]?.profesor || 'desconocido';
        XLSX.writeFile(wb, `resultados_${nombreProfesor}_${fechaHoraActual}.xlsx`);
    }

    document.getElementById('exportar-btn').addEventListener('click', exportarAExcelPorVariable);