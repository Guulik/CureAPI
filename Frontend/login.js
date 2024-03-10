function toRegister() {
    window.location.href = 'register.html';
}

function login() {
    let phoneNumber = document.querySelector('.login-phone-input').value;
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