async function topAiringAnime() {
    const loader = document.createElement('div');
    loader.setAttribute('class', 'loader');
    const topCards = document.getElementById('top-anime-cards');
    topCards.append(loader);

    const response = await fetch('https://api.jikan.moe/v4/top/anime?filter=airing');
    const data = await response.json();
    const airingAnime = data.data.splice(0, 10);

    topCards.innerHTML = '';
    for (const anime of airingAnime) {
        const card = document.createElement('article');
        card.setAttribute('class', 'card')
        card.innerHTML =
            `<a href='/anime/${anime.mal_id}'>\n` +
            `<img src=${anime.images.jpg.image_url} alt='${anime.title}'>\n` +
            `<h3>${anime.title}</h3>\n` +
            `</a>`
        topCards.append(card);
    }
}

try {
    topAiringAnime();
} catch (error) {
    console.error(error);
}