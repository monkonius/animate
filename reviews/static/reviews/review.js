function toggleReview() {
    const reviewForm = document.querySelector('.review-form');
    reviewForm.classList.toggle('show');
    
    const toggleButton = document.getElementById('review-toggle');
    toggleButton.classList.toggle('hide');
}