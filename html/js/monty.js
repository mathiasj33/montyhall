import * as api from './restClient.js';
import {BarChart} from "./chart.js";

google.charts.load('current', {packages: ['bar']});
google.charts.setOnLoadCallback(onLibraryLoaded);

const chart = new BarChart('bar-chart', 1.0);

function onLibraryLoaded() {
    updateChart();
    setInterval(updateChart, 1000);
}

async function updateChart() {
    const stats = await api.getMontyStats();
    chart.draw({
        'Fraction of stick wins': stats.stick_ratio,
        'Fraction of switch wins': stats.switch_ratio
    });
}

document.onkeydown = function(e) {
    e = e || window.event;
    if(e.code === 'ArrowRight') {
        window.location.replace('dice.html');
    }
}