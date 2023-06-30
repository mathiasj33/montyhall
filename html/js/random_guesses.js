import * as api from './restClient.js';
import {BarChart} from "./chart.js";

google.charts.load('current', {packages: ['bar']});
google.charts.setOnLoadCallback(onLibraryLoaded);

const chart = new BarChart('bar-chart');

function onLibraryLoaded() {
    updateChart();
    setInterval(updateChart, 1000);
}

function augmentMissingKeys(data) {
    const newData = structuredClone(data);
    for (let i = 1; i <= 10; i++) {
        if (!(i in data)) {
            newData[i] = 0;
        }
    }
    return newData;
}

async function updateChart() {
    let guesses = await api.getRandomGuesses();
    guesses = augmentMissingKeys(guesses);
    chart.draw(guesses);
}

document.onkeydown = function(e) {
    e = e || window.event;
    if(e.code === 'ArrowLeft') {
        window.location.replace('dice.html');
    }
}