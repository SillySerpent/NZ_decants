document.addEventListener('DOMContentLoaded', () => {
    // Image Gallery Interaction
    const mainImage = document.querySelector('.cologne-images .main-image');
    const thumbnails = document.querySelectorAll('.thumbnail-image');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            const tempSrc = mainImage.src;
            mainImage.src = thumbnail.src;
            thumbnail.src = tempSrc;
        });
    });

    // Star Rating Interaction in Review Form
    const starRatingInputs = document.querySelectorAll('.star-rating input[type=radio]');
    const starRatingLabels = document.querySelectorAll('.star-rating label');

    starRatingLabels.forEach(label => {
        label.addEventListener('mouseover', highlightStars);
        label.addEventListener('mouseout', resetStars);
        label.addEventListener('click', setRating);
    });

    function highlightStars(event) {
        const label = event.currentTarget;
        const value = label.previousElementSibling.value;

        starRatingLabels.forEach(lab => {
            if (lab.previousElementSibling.value <= value) {
                lab.classList.add('hovered');
            } else {
                lab.classList.remove('hovered');
            }
        });
    }

    function resetStars() {
        starRatingLabels.forEach(lab => {
            lab.classList.remove('hovered');
        });
    }

    function setRating(event) {
        const label = event.currentTarget;
        const input = label.previousElementSibling;
        input.checked = true;

        starRatingLabels.forEach(lab => {
            if (lab.previousElementSibling.checked) {
                lab.classList.add('selected');
            } else {
                lab.classList.remove('selected');
            }
        });
    }
});