document.addEventListener("DOMContentLoaded", function() {
    const medicineListDiv = document.getElementById("medicine-list");
    const summaryDiv = document.getElementById("summary");
    const placeOrderButton = document.getElementById("place-order");

    // Sample medicine data
    const medicines = [
        { name: "Medicine 1", price: 10, quantity: 2 },
        { name: "Medicine 2", price: 15, quantity: 1 },
        { name: "Medicine 3", price: 20, quantity: 3 }
    ];

    // Render medicine blocks
    medicines.forEach(medicine => {
        const medicineDiv = document.createElement("div");
        medicineDiv.classList.add("medicine");

        const nameHeader = document.createElement("h3");
        nameHeader.textContent = medicine.name;

        const pricePara = document.createElement("p");
        pricePara.textContent = `Price: $${medicine.price}`;

        const quantityPara = document.createElement("p");
        quantityPara.textContent = `Quantity: ${medicine.quantity}`;

        medicineDiv.appendChild(nameHeader);
        medicineDiv.appendChild(pricePara);
        medicineDiv.appendChild(quantityPara);

        medicineListDiv.appendChild(medicineDiv);
    });

    // Calculate total price
    const totalPrice = medicines.reduce((total, medicine) => total + (medicine.price * medicine.quantity), 0);

    // Render summary
    const totalPricePara = document.createElement("p");
    totalPricePara.textContent = `Total Price: $${totalPrice}`;

    summaryDiv.appendChild(totalPricePara);

    // Place order button click event
    placeOrderButton.addEventListener("click", function() {
        alert("Order placed successfully!");
    });
});
