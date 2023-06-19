import * as api from './restClient.js';

$(document).ready(function () {
    function handleApiResponse(response) {
        if (!response.ok) return;
        const successMsg = $('#alert');
        successMsg.fadeTo(10, 1);
        setTimeout(() => successMsg.fadeTo(50, 0), 1000);
    }

    $('#stick-btn-group button').on('click', async function () {
        const res = await api.addGame(false, $(this).text() === 'Won');
        handleApiResponse(res);
    });

    $('#switch-btn-group button').on('click', async function () {
        const res = await api.addGame(true, $(this).text() === 'Won');
        handleApiResponse(res);
    });

    $('#random-guess-btns button').on('click', async function () {
        const number = parseInt($(this).text());
        const res = await api.addRandomGuess(number);
        handleApiResponse(res);
    });

    $('#dice-roll-btns button').on('click', async function () {
        const number = parseInt($(this).text());
        const res = await api.addDiceRoll(number);
        handleApiResponse(res);
    });

    $('#streak-btn').on('click', async function () {
        const streak = parseInt($('#streak-input').val());
        const res = await api.setStreak(streak);
        handleApiResponse(res);
    });
});

if(localStorage.getItem('API_KEY') === null) {
    window.location.replace('signin.html')
}