document.addEventListener("DOMContentLoaded", function() {
    const mainContainer = document.getElementById("main-contatiner");

    const userUid = localStorage.getItem('userUid');

    const logoutButton = document.getElementById("logout");
    logoutButton.addEventListener("click", function() {
        localStorage.removeItem("userUid");
        window.location.href = "index.html";
    });

    const checkoutButton = document.getElementById("checkout-btn");
    checkoutButton.addEventListener("click", function() {
        var deliveryType = document.getElementById("self-delivery").checked ? true : false;
        var url = `http://127.0.0.1:8000/order/place_order?user_uid=${userUid}&delivery_type=${deliveryType}`;
        fetch(url, { method: "POST" })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
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
        const cureUid = medicine.uid; 
        console.log(cureUid)
        const cartCount = await fetchCureCartCount(cureUid);

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

        const div = document.createElement("div");
        div.classList.add("medicine");

        const link = document.createElement('link');

        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = 'components/medicine.css';
    
        div.appendChild(link);

        

        div.innerHTML = `
        <div>
        <link href="components/medicine.css" rel="stylesheet" />
        <div class="medicine-container">
            <div class="medicine-cname">
            <h3 class="medicine-name">${medicine.name}</h3>
            </div>
            <div class="medicine-cdescription">
            <span class="medicine-description">${medicine.description}</span>
            </div>
            <div class="medicine-cprice">
            <span class="medicine-price">${medicine.price} руб</span>
            </div>
            <div class="medicine-cavailability">
            <span class="medicine-availability">${availabilityText}</span>
            </div>
            <div class="medicine-cstock">
            <span class="medicine-stock">На складе: ${medicine.count}</span></div>
            <div class="medicine-ccart">
            <span class="medicine-cart"><span>В корзине:</span></span>
            <div class="medicine-cart-buttons">
                <button type="button" class="medicine-plus-btn button">
                <span>+</span>
                </button>
                <span class="medicine-cart-count">${cartCount}</span>
                <button type="button" class="medicine-minus-btn button">
                <span>-</span>
                </button>
            </div>
            </div>
        </div>
        </div>
        `;

        const addToCartButton = div.querySelector(".medicine-plus-btn");
        addToCartButton.addEventListener("click", async () => {
            const cureCartCount = await fetchCureCartCount(cureUid);
            if (cureCartCount >= medicine.count) {
                alert("Недостаточно лекарства на складе");
                return;
            }
            
            const url = `http://127.0.0.1:8000/order/add_cure?cure_uid=${cureUid}&user_uid=${userUid}`;
            fetch(url, { method: "POST" })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
            
                const quantityElement = div.querySelector(".medicine-cart-count");
                const newCount = await fetchCureCartCount(cureUid);
                quantityElement.innerText = newCount;  

        });


        const removeFromCartButton = div.querySelector(".medicine-minus-btn");
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

                const quantityElement = div.querySelector(".medicine-cart-count");
                const newCount = await fetchCureCartCount(cureUid);
                quantityElement.innerText = newCount;
        });
        return div;
    }

    // Функция для добавления лекарств на страницу каталога
    async function renderMedicines() {
        const medicines = await fetchMedicines();
        if (medicines) {
            let count = 0;
            let currentRow;
            for (const medicine of medicines) {
                if (count % 5 === 0) {
                    currentRow = document.createElement('div');
                    currentRow.classList.add('catalogue-catalogue-row');
                    mainContainer.appendChild(currentRow);
            }
            const medicineElement = await createMedicineElement(medicine);
            currentRow.appendChild(medicineElement);
            count++;
            }
        }

    }
    // Вызов функции для добавления лекарств на страницу каталога
    renderMedicines();
});
