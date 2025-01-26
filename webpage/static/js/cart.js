document.addEventListener('DOMContentLoaded', () => {
    const decreaseButtons = document.querySelectorAll('.decrease');
    const increaseButtons = document.querySelectorAll('.increase');
    const quantityInputs = document.querySelectorAll('.item-quantity input');
    const removeButtons = document.querySelectorAll('.remove-item');
    const totalPriceElement = document.querySelector('.cart-total-price');
    const itemTotalPrices = document.querySelectorAll('.item-total');

    // Function to update the total price
    function updateTotalPrice() {
        let totalPrice = 0;
        const cartItems = document.querySelectorAll('.cart-item');
        cartItems.forEach(item => {
            const price = parseFloat(item.querySelector('.item-details p').textContent.replace('Price: $', ''));
            const quantity = parseInt(item.querySelector('.item-quantity input').value);
            const itemTotalElement = item.querySelector('.item-total');
            const itemTotalPrice = price * quantity;
            itemTotalElement.textContent = itemTotalPrice.toFixed(2);
            totalPrice += itemTotalPrice;
        });
        totalPriceElement.textContent = totalPrice.toFixed(2);
    }

    // Initialize total price
    updateTotalPrice();

    decreaseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const input = button.parentElement.querySelector('input');
            let quantity = parseInt(input.value);
            if (quantity > 1) {
                quantity--;
                input.value = quantity;
                updateTotalPrice();
            }
        });
    });

    increaseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const input = button.parentElement.querySelector('input');
            let quantity = parseInt(input.value);
            quantity++;
            input.value = quantity;
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

    // Continue Shopping Button
    const continueShoppingButtons = document.querySelectorAll('.continue-shopping-btn');
    continueShoppingButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = "{{ url_for('browse_page_blueprint.browse_page') }}";
        });
    });
});

// At the top of your script
const freeShippingThreshold = 100; // Example threshold for free shipping

// In your updateTotalPrice function, add:
function updateTotalPrice() {
    // ...existing code...

    // Update progress bar
    const progress = document.querySelector('.progress');
    const amountNeededElement = document.querySelector('.amount-needed');

    if (progress && amountNeededElement) {
        const percentage = Math.min((totalPrice / freeShippingThreshold) * 100, 100);
        progress.style.width = `${percentage}%`;

        const amountNeeded = Math.max(freeShippingThreshold - totalPrice, 0);
        amountNeededElement.textContent = amountNeeded.toFixed(2);

        if (totalPrice >= freeShippingThreshold) {
            amountNeededElement.parentElement.textContent = "You've qualified for free shipping!";
        }
    }
}