        // Add subtle animations to cards on scroll
        document.addEventListener('DOMContentLoaded', () => {
            const cards = document.querySelectorAll('.card');

            cards.forEach(card => {
                card.style.transform = 'translateY(50px)';
                card.style.opacity = '0';

                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if(entry.isIntersecting) {
                            card.style.transform = 'translateY(0)';
                            card.style.opacity = '1';
                        }
                    });
                }, { threshold: 0.1 });

                observer.observe(card);
            });

            // Add hover sound effect
            document.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('mouseenter', () => {
                    new Audio('static/sounds/hover.mp3').play();
                });
            });
        });






