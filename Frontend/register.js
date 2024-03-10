function register() {
    let phoneNumber = document.getElementById('phone-input').value.toString();
    phoneNumber = phoneNumber.startsWith('+') ?  parseInt(phoneNumber.slice(1)) : parseInt(phoneNumber);
    if(phoneNumber.toString().length === 11 && !isNaN(phoneNumber)) {
        console.log(phoneNumber.toString().length);
    } else {
        alert("Некорректный номер телефона");
        console.log(phoneNumber.toString());
        return
    }

    const name = document.getElementById('name-input').value;
    const address = document.getElementById('adress-input').value;

    fetch(`http://127.0.0.1:8000/user/register?phoneNumber=${phoneNumber}&name=${name}&address=${address}`, { method: "POST" })
    .then(response => {
        console.log(response)
        if (response.ok) {
            alert("Регистрация завершена");
            window.location.href = 'index.html';
        } else {
            alert("Ошибка при регистрации");
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function toLogin() {
        window.location.href = 'index.html';
}