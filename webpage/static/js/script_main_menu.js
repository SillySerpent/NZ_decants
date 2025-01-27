document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.carousel-dot');
    let currentSlide = 0;
    const slideInterval = setInterval(nextSlide, 5000);

    function nextSlide() {
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('active');
        currentSlide = (currentSlide+1)%slides.length;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            currentSlide = index;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        });
    });
});






