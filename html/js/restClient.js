const SERVER_URL = 'https://montyhall.mathias-jackermeier.me/api/v1';

async function get(endpoint) {
    const response = await fetch(`${SERVER_URL}/${endpoint}`);
    return response.json();
}

async function post(body, endpoint) {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    };
    const api_key = localStorage.getItem('API_KEY')
    if (api_key !== null) {
        headers['Authorization'] = `Bearer ${api_key}`
    }
    return fetch(`${SERVER_URL}/${endpoint}`, {
        method: 'POST',
        mode: 'cors',
        headers: headers,
        body: JSON.stringify(body)
    });
}

export async function login(password) {
    return post(password, 'login');
}

export async function getDiceRolls() {
    return get('random/dice_rolls');
}

export async function addDiceRoll(roll) {
    return post(roll, 'random/dice_rolls');
}

export async function getRandomGuesses() {
    return get('random/guesses');
}

export async function addRandomGuess(guess) {
    return post(guess, 'random/guesses');
}

export async function getStreak() {
    return get('random/streak');
}

export async function setStreak(streak) {
    return post(streak, 'random/streak');
}

export async function getMontyStats() {
    return get('monty/stats');
}

export async function addGame(switched, won) {
    return post({'switched': switched, 'won': won}, 'monty/games');
}