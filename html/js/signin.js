import * as api from "./restClient.js";

$(document).ready(function () {
    $('#login-btn').on('click', async function (e) {
        e.preventDefault();
        const pwd = $('#password-input').val();
        const res = await api.login(pwd);
        if(!res.ok) {
            $('#password-input').addClass('is-invalid');
            return;
        }
        const api_key = await res.json();
        localStorage.setItem('API_KEY', api_key);
        window.location.replace('client.html')
    });
});

if(localStorage.getItem('API_KEY') !== null) {
    window.location.replace('client.html')
}