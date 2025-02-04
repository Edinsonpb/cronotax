import { usersCronotax } from './usuarios.js';
import { users } from './usuarios.js';

const login = (username, password) => {
    if (users[username] && users[username] === password) {
        return true;
    } else {
        return false;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const isSuccess = login(username, password);
            if (isSuccess) {
                window.location.href = './sesion.html';
            } else {
                document.getElementById('message').innerText = 'Invalid username or password';
            }
        });
    }
});
