document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message, index) {
        // Delay the appearance for a smoother effect
        setTimeout(function() {
            message.classList.add('show');
        }, 300 * index);

        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            message.classList.remove('show');
        }, 5000 + (300 * index));

        var closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.classList.remove('show');
            });
        }

        // Remove the message element after it hides
        message.addEventListener('transitionend', function(event) {
            if (!message.classList.contains('show') && event.propertyName === 'opacity') {
                message.parentNode.removeChild(message);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const togglePasswords = document.querySelectorAll('.toggle-password');

    togglePasswords.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = toggle.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                toggle.classList.remove('fa-eye');
                toggle.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                toggle.classList.remove('fa-eye-slash');
                toggle.classList.add('fa-eye');
            }
        });
    });
});
