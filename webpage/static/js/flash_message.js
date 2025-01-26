// flash_message.js

document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message, index) {
        setTimeout(function() {
            message.classList.add('show');
        }, 100 * index);

        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            message.classList.remove('show');
        }, 5000 + (100 * index));

        var closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.classList.remove('show');
            });
        }

        // Remove the message element after the transition ends
        message.addEventListener('transitionend', function(event) {
            if (!message.classList.contains('show')) {
                message.parentNode.removeChild(message);
            }
        });
    });
});