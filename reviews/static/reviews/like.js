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

function likeReview(node) {
    const like = node.children[1];
    node.classList.toggle('highlighted');

    const review = node.parentElement.parentElement;
    let likeCount = Number(like.innerHTML)

    const csrftoken = getCookie('csrftoken');
    fetch(`/like/${review.id}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            data.created ? likeCount++ : likeCount--;
            like.innerHTML = likeCount;

            if (data.dislike_exists) {
                const dislike = node.nextElementSibling;
                dislike.classList.toggle('highlighted');

                let dislikeCount = Number(dislike.children[1].innerHTML);
                dislike.children[1].innerHTML = --dislikeCount;
            }
        })
}

function dislikeReview(node) {
    const dislike = node.children[1];
    node.classList.toggle('highlighted');

    const review = node.parentElement.parentElement;
    let dislikeCount = Number(dislike.innerHTML)

    const csrftoken = getCookie('csrftoken');
    fetch(`/dislike/${review.id}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            data.created ? dislikeCount++ : dislikeCount--;
            dislike.innerHTML = dislikeCount;

            if (data.like_exists) {
                const like = node.previousElementSibling;
                like.classList.toggle('highlighted');

                let likeCount = Number(like.children[1].innerHTML);
                like.children[1].innerHTML = --likeCount;
            }
        })
}