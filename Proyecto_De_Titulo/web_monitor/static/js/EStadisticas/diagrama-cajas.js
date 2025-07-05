// diagrama-cajas.js
console.log("Resultados JSON:", resultados);

// Función auxiliar para extraer y agrupar registros por fecha
const agruparPorFecha = (datos, campoDatos, campoValor) => {
    const agrupado = {};

    datos.forEach(item => {
        const registros = item[campoDatos] || [];
        registros.forEach(r => {
            const fecha = r.fecha_hora.split(" ")[0]; // solo fecha, sin hora
            if (!agrupado[fecha]) agrupado[fecha] = [];
            if (r[campoValor] !== undefined) {
                agrupado[fecha].push(r[campoValor]);
            }
        });
    });

    return agrupado;
};

// Función para crear boxplot
const crearBoxPlot = (divId, titulo, datos, campoDatos, campoValor, colorBase) => {
    const agrupado = agruparPorFecha(datos, campoDatos, campoValor);
    const fechas = Object.keys(agrupado);
    const colores = colorBase || [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ];

    const data = fechas.map((fecha, idx) => ({
        y: agrupado[fecha],
        type: 'box',
        name: fecha,
        boxmean: true,
        marker: {
            color: colores[idx % colores.length]
        }
    }));

    const hayDatos = data.some(trace => trace.y.length > 0);

    const layout = hayDatos ? {
        title: titulo,
        autosize: true,
        height: 400,
        margin: { t: 50, b: 100 },
        xaxis: {
            title: 'Fecha',
            tickangle: -45
        },
        yaxis: {
            title: campoValor
        },
        boxmode: 'group'
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

// Llamadas por variable
crearBoxPlot('boxFrecuencia', 'Frecuencia Fundamental (Hz)', resultados, 'registros_voz', 'freq');
crearBoxPlot('boxIntensidad', 'Intensidad de Voz (dB)', resultados, 'registros_voz', 'intensidad');
crearBoxPlot('boxRuido', 'Ruido Ambiental (dB)', resultados, 'registros_ruido', 'ruido');
crearBoxPlot('boxTemperatura', 'Temperatura (°C)', resultados, 'registros_temperatura', 'temperatura');
crearBoxPlot('boxHumedad', 'Humedad Relativa (%)', resultados, 'registros_humedad', 'humedad');
crearBoxPlot('boxCO2', 'Concentración de CO₂ (ppm)', resultados, 'registros_co2', 'co2');
