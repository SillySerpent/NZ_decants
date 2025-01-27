document.addEventListener('DOMContentLoaded', () => {
    const cartContainer = document.querySelector('.cart-items');
    const totalPriceElement = document.querySelector('.cart-total-price');
    const freeShippingThreshold = 100; // Threshold for free shipping

    // Function to update the total price and progress bar
    function updateTotalPrice() {
        let totalPrice = 0;
        const cartItems = document.querySelectorAll('.cart-item');

        cartItems.forEach(item => {
            const priceElement = item.querySelector('.item-details p');
            const priceText = priceElement.textContent.match(/Price:\s*\$([\d.]+)/);
            const price = parseFloat(priceText[1]);
            const quantity = parseInt(item.querySelector('.item-quantity input').value);
            const itemTotalElement = item.querySelector('.item-total');
            const itemTotalPrice = price * quantity;
            itemTotalElement.textContent = itemTotalPrice.toFixed(2);
            totalPrice += itemTotalPrice;
        });

        totalPriceElement.textContent = totalPrice.toFixed(2);

        // Update progress bar
        const progress = document.querySelector('.progress');
        const progressMessageElement = document.querySelector('.progress-container p');

        if (progress && progressMessageElement) {
            const percentage = Math.min((totalPrice / freeShippingThreshold) * 100, 100);
            progress.style.width = `${percentage}%`;

            if (totalPrice >= freeShippingThreshold) {
                progressMessageElement.innerHTML = "You've qualified for free shipping!";
            } else {
                const amountNeeded = Math.max(freeShippingThreshold - totalPrice, 0).toFixed(2);
                progressMessageElement.innerHTML = `You're only $<span class="amount-needed">${amountNeeded}</span> away from free shipping!`;
            }
        }

        // Update the disabled state of decrease buttons
        updateQuantityButtons();
    }

    // Disable decrease button when quantity is one
    function updateQuantityButtons() {
        const cartItems = document.querySelectorAll('.cart-item');
        cartItems.forEach(item => {
            const quantity = parseInt(item.querySelector('.item-quantity input').value);
            const decreaseButton = item.querySelector('.quantity-btn.decrease');
            if (quantity <= 1) {
                decreaseButton.disabled = true;
            } else {
                decreaseButton.disabled = false;
            }
        });
    }

    // Initialize total price and progress bar when the page loads
    updateTotalPrice();

    // Event delegation for plus and minus buttons
    cartContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('decrease')) {
            const input = event.target.parentElement.querySelector('input');
            let quantity = parseInt(input.value);
            if (quantity > 1) {
                quantity--;
                input.value = quantity;
                updateTotalPrice();
                updateQuantityInServer(event.target.closest('.cart-item'));
            }
        }

        if (event.target.classList.contains('increase')) {
            const input = event.target.parentElement.querySelector('input');
            let quantity = parseInt(input.value);
            quantity++;
            input.value = quantity;
            updateTotalPrice();
            updateQuantityInServer(event.target.closest('.cart-item'));
        }
    });

    // Event listener for quantity input change
    cartContainer.addEventListener('input', function(event) {
        if (event.target.matches('.item-quantity input')) {
            const input = event.target;
            let quantity = parseInt(input.value);
            if (isNaN(quantity) || quantity < 1) {
                input.value = 1;
                alert('Minimum quantity is 1.');
            }
            updateTotalPrice();
            updateQuantityInServer(event.target.closest('.cart-item'));
        }
    });

    // Function to update quantity in the server
    function updateQuantityInServer(cartItemElement) {
        const quantityInput = cartItemElement.querySelector('.item-quantity input');
        const quantity = parseInt(quantityInput.value);
        const cologneId = cartItemElement.dataset.cologneId;
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        fetch(updateQuantityUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                'cologne_id': cologneId,
                'quantity': quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Error updating quantity on server.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Continue Shopping Button
    const continueShoppingButtons = document.querySelectorAll('.continue-shopping-btn');
    continueShoppingButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = "{{ url_for('browse_page_blueprint.browse_page') }}";
        });
    });
});