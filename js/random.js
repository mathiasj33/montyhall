import * as restClient from './restClient.js';
import {BarChart} from "./chart.js";

google.charts.load('current', {packages: ['bar']});
google.charts.setOnLoadCallback(onLibraryLoaded);

const guessChart = new BarChart('guess-chart');
const randomChart = new BarChart('random-chart');

function onLibraryLoaded() {
    updateCharts();
    updateStreak();
    setInterval(updateCharts, 1000);
    setInterval(updateStreak, 1000);
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

async function updateCharts() {
    let [guesses, randoms] = await Promise.all([restClient.getRandomNumbers(), restClient.getRandomNumbers()]);
    guesses = augmentMissingKeys(guesses);
    randoms = augmentMissingKeys(randoms);
    guessChart.draw(guesses);
    randomChart.draw(randoms);
}

async function updateStreak() {
    // restClient.postStreak(4);
    const streak = await restClient.getStreak();
    document.getElementById('streak').textContent = streak;
    const power = 2 ** streak;
    const prob = 1 / power;
    document.getElementById('streak-length').textContent = power;
    document.getElementById('streak-percent').textContent = `${Number(prob * 100).toFixed(2)}%`;
}