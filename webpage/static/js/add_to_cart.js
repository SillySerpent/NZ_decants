const addToCartButtons = document.querySelectorAll('.add-to-cart');

addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.innerText = "Added!";
        button.disabled = true;
        setTimeout(() => {
            button.innerText = "Add to Cart";
            button.disabled = false;
        }, 2000);
    });
});