function register() {
    const phoneNumber = document.getElementById('phoneNumber').value;
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;

    fetch(`http://127.0.0.1:8000/user/register?phoneNumber=${phoneNumber}&name=${name}&address=${address}`)
    .then(response => {
        if (response.ok) {
            alert("Регистрация завершена");
        } else {
            alert("Ошибка при регистрации");
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function login() {
    const phoneNumber = document.getElementById('phoneNumber').value;

    fetch(`http://127.0.0.1:8000/user/login?phone_number=${phoneNumber}`)
    .then(response => {
        if (response.ok) {
            window.location.href = "catalogue.html";
        } else {
            alert("Ошибка при входе");
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}