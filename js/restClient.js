const SERVER_URL = 'http://127.0.0.1:5000/api/v1';

async function get(endpoint) {
    const response = await fetch(`${SERVER_URL}/${endpoint}`);
    return response.json();
}

async function post(body, endpoint) {
    const response = await fetch(`${SERVER_URL}/${endpoint}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    });
    return response.ok;
}

export async function getRandomNumbers() {
    return get('random/numbers');
}

export async function addRandomNumber() {
    return post({}, 'random/numbers');
}

export async function getStreak() {
    return get('random/streak');
}

export async function postStreak(streak) {
    return post(streak, 'random/streak');
}

export async function getMontyStats() {
    return get('monty/stats');
}

export async function addGame(switched, won) {
    return post({'switched': switched, 'won': won}, 'monty/games');
}