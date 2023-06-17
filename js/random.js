import * as api from './restClient.js';
import {BarChart} from "./chart.js";

google.charts.load('current', {packages: ['bar']});
google.charts.setOnLoadCallback(onLibraryLoaded);

const guessChart = new BarChart('guess-chart');
const randomChart = new BarChart('random-chart');

async function onLibraryLoaded() {
    await Promise.all([updateCharts(), updateStreak()])
    setInterval(updateCharts, 1000);
    setInterval(updateStreak, 1000);
}

function augmentMissingKeys(data) {
    const newData = structuredClone(data);
    for (let i = 1; i <= 6; i++) {
        if (!(i in data)) {
            newData[i] = 0;
        }
    }
    return newData;
}

async function updateCharts() {
    let [guesses, randoms] = await Promise.all([api.getRandomNumbers(), api.getRandomNumbers()]);
    guesses = augmentMissingKeys(guesses);
    randoms = augmentMissingKeys(randoms);
    guessChart.draw(guesses);
    randomChart.draw(randoms);
}

async function updateStreak() {
    const streak = await api.getStreak();
    document.getElementById('streak').textContent = streak;
    const power = 2 ** streak;
    const prob = 1 / power;
    document.getElementById('streak-length').textContent = power;
    document.getElementById('streak-percent').textContent = `${Number(prob * 100).toFixed(2)}%`;
}