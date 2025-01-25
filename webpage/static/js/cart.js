document.addEventListener('DOMContentLoaded', () => {
    const decreaseButtons = document.querySelectorAll('.decrease');
    const increaseButtons = document.querySelectorAll('.increase');
    const quantityInputs = document.querySelectorAll('.item-quantity input');
    const removeButtons = document.querySelectorAll('.remove-item');
    const totalPriceElement = document.querySelector('.cart-summary h3');

    let totalPrice = 0;

    // Function to update the total price
    function updateTotalPrice() {
        totalPrice = 0;
        const cartItems = document.querySelectorAll('.cart-item');
        cartItems.forEach(item => {
            const price = parseFloat(item.querySelector('.item-details p').textContent.replace('Price: $', ''));
            const quantity = parseInt(item.querySelector('.item-quantity input').value);
            totalPrice += price * quantity;
        });
        totalPriceElement.textContent = `Total: $${totalPrice.toFixed(2)}`;
    }

    // Initialize total price
    updateTotalPrice();

    decreaseButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            let quantity = parseInt(quantityInputs[index].value);
            if (quantity > 1) {
                quantity--;
                quantityInputs[index].value = quantity;
                updateTotalPrice();
            }
        });
    });

    increaseButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            let quantity = parseInt(quantityInputs[index].value);
            quantity++;
            quantityInputs[index].value = quantity;
            updateTotalPrice();
        });
    });

    quantityInputs.forEach(input => {
        input.addEventListener('change', () => {
            if (input.value < 1) {
                input.value = 1;
            }
            updateTotalPrice();
        });
    });

    removeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const item = button.closest('.cart-item');
            item.remove();
            updateTotalPrice();
            alert('Item removed from your cart.');
        });
    });
});