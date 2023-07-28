// register.js

document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const nama_depan = document.getElementById('nama_depan').value;
    const nama_belakang = document.getElementById('nama_belakang').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const data = { username, nama_depan, nama_belakang, email, password };

    fetch('http://localhost:8000/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            // Login successful, redirect to another page or perform any other action
            console.log('Register successful');
        } else {
            // Login failed, display error message
            console.error('Register failed:', result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});