document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".container");
    const userUid = localStorage.getItem('userUid');
    const logoutButton = document.getElementById("logout");

    logoutButton.addEventListener("click", function() {
        localStorage.removeItem("userUid");
        window.location.href = "login.html";
    });

    const checkoutButton = document.getElementById("checkout-btn");
    checkoutButton.addEventListener("click", function() {
        var deliveryType = document.getElementById("delivery-type-checkbox").checked ? true : false;
        var url = `http://127.0.0.1:8000/order/place_order?user_uid=${userUid}&delivery_type=${deliveryType}`;
        fetch(url, { method: "POST" })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response data here
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });

            alert("Заказ успешно оформлен!");
            location.reload();
    });


    
    // Функция для получения лекарств
    async function fetchMedicines() {
        try {
            const response = await fetch("http://127.0.0.1:8000/cure/get_all");
            if (!response.ok) {
                throw new Error("Failed to fetch medicines");
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(error);
        }
    }

    // Функция для изменения количества лекарства по cure_uid
    async function fetchCureCartCount(cureUid) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/order/get_cart?user_uid=${userUid}`);
            const cartItems = await response.json();
            if ("message" in cartItems && cartItems.message === "Cart is empty") {
                console.log("Корзина пуста");
                return 0;
            }
            
            const cureResponse = await fetch(`http://127.0.0.1:8000/cure/get_cure?cure_uid=${cureUid}`);
            const cure = await cureResponse.json();
            const cureItem = cartItems.find(item => item.name === cure.name);
            if (cureItem) {
                console.log(cureItem.count);
                return cureItem.count;
            } else {
                return 0; 
            }
        } catch (error) {
            console.error('Ошибка получения количества лекарства из корзины:', error);
            return 0;
        }
    }
    
    // Функция для создания HTML-разметки для каждого лекарства
    async function createMedicineElement(medicine) {
        const div = document.createElement("div");
        div.classList.add("medicine");

        const getDaysString = (days) => {
            if (days === 1) {
                return "день";
            } else if (days >= 2 && days <= 4) {
                return "дня";
            } else {
                return "дней";
            }
        };

        let availabilityText;
        if (medicine.count > 0) {
            availabilityText = `Есть на складе`;
        } else {
            availabilityText = `Поставка: ${medicine.availabilityTime} ${getDaysString(medicine.availabilityTime)}`;
}
        const cureUid = medicine.uid; // Получаем uid лекарства

        const cartCount = await fetchCureCartCount(cureUid);

        div.innerHTML = `
            <h3>${medicine.name}</h3>
            <p>Описание: ${medicine.description}</p>
            <p>Цена: $${medicine.price}</p>
            <p>${availabilityText}</p>
            <p>На складе: ${medicine.count}</p>
            <button class="add-to-cart">+</button>
            <span class="cart-quantity">${cartCount}</span>
            <button class="remove-from-cart">-</button>
        `;

        const addToCartButton = div.querySelector(".add-to-cart");
        addToCartButton.addEventListener("click", async () => {

        const cureCartCount = await fetchCureCartCount(cureUid);
        if (cureCartCount >= medicine.count) {
            alert("Недостаточно лекарства на складе");
            return;
        }
        

        const url = `http://127.0.0.1:8000/order/add_cure?cure_uid=${cureUid}&user_uid=${userUid}`;
        // Отправляем запрос
        fetch(url, { method: "POST" })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        
            const quantityElement = div.querySelector(".cart-quantity");
            const newCount = await fetchCureCartCount(cureUid);
            quantityElement.innerText = newCount;  

        });

        const removeFromCartButton = div.querySelector(".remove-from-cart");
        removeFromCartButton.addEventListener("click", async () => {

        const cureCartCount = await fetchCureCartCount(cureUid);
        if (cureCartCount === 0 ) {
            alert("У вас в корзине нет этого лекарства");
            return;
        }

        const url = `http://127.0.0.1:8000/order/remove_cure?cure_uid=${cureUid}&user_uid=${userUid}`;
        // Отправляем запрос
        fetch(url, { method: "POST" })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            })

            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });

            const quantityElement = div.querySelector(".cart-quantity");
            const newCount = await fetchCureCartCount(cureUid);
            quantityElement.innerText = newCount;
        });
        return div;
    }

    // Функция для добавления лекарств на страницу каталога
    async function renderMedicines() {
        const medicines = await fetchMedicines();
        if (medicines) {
            for (const medicine of medicines) {
                const medicineElement = await createMedicineElement(medicine);
                container.appendChild(medicineElement);
            }
        }
    }

    // Вызов функции для добавления лекарств на страницу каталога
    renderMedicines();
});
