const menuToggle = document.querySelector('.menu-toggle');
const navbarMenu = document.querySelector('.navbar-menu');

menuToggle.addEventListener('click', () => {
    navbarMenu.classList.toggle('active');
    menuToggle.classList.toggle('active');
});

window.addEventListener('resize', () => {
    if(window.innerWidth > 768) {
        navbarMenu.classList.remove('active');
        menuToggle.classList.remove('active');
    }
});