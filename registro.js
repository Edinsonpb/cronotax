import { usersCronotax } from './usuarios.js';
import { users } from './login.js';

document.addEventListener('DOMContentLoaded', () => {
    const registroForm = document.getElementById('registroForm');
    if (registroForm) {
        registroForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const nombres = document.getElementById('nombres').value;
            const apellidos = document.getElementById('apellidos').value;
            const telefono = document.getElementById('telefono').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Crear un nuevo objeto usuario
            const nuevoUsuario = {
                nombres: nombres,
                apellidos: apellidos,
                telefono: telefono,
                password: password
            };

            // Agregar el nuevo usuario al objeto usersCronotax con el email como clave
            usersCronotax[email] = nuevoUsuario;

            // Agregar el nuevo usuario al objeto users con el email como clave y la clave como valor
            users[email] = password;

            // Mostrar un mensaje de éxito
            document.getElementById('message').innerText = 'Registro exitoso';

            // Limpiar el formulario
            registroForm.reset();

            console.log(usersCronotax); // Para verificar en la consola
            console.log(users); // Para verificar en la consola
        });
    }
});