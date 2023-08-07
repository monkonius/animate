function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleReview() {
    const reviewForm = document.querySelector('.review-form');
    reviewForm.classList.toggle('show');
    
    const toggleButton = document.getElementById('review-toggle');
    toggleButton.classList.toggle('hide');
}

function likeReview(node) {
    const likeCount = node.children[1];
    node.classList.toggle('liked');

    const review = node.parentElement;
    let count = Number(likeCount.innerHTML)

    const csrftoken = getCookie('csrftoken');
    fetch(`/like/${review.id}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            data.created ? count++ : count--;
            likeCount.innerHTML = count;
        })
}