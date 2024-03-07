function register() {
    let phoneNumber = document.getElementById('phoneNumber').value;
    phoneNumber = phoneNumber.startsWith('+') ?  parseInt(phoneNumber.slice(1)) : parseInt(phoneNumber);
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;

    fetch(`http://127.0.0.1:8000/user/register?phoneNumber=${phoneNumber}&name=${name}&address=${address}`, { method: "POST" })
    .then(response => {
        console.log(response)
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
    let phoneNumber = document.getElementById('phoneNumber').value;
    phoneNumber = phoneNumber.startsWith('+') ? parseInt(phoneNumber.slice(1)) : parseInt(phoneNumber);

    fetch(`http://127.0.0.1:8000/user/login?phone_number=${phoneNumber}`)
    .then(response => {
        if (response.ok) {
            return response.json()
        }
        else {
            alert("Пользователь не найден");
        }
    })
    .then(data => {
        if (data) {
            localStorage.setItem('userUid', data);
            console.log(localStorage.getItem('userUid'));
            window.location.href = "catalogue.html";
        } 
        
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}