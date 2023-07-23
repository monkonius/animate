async function searchAnime() {
    const loader = document.createElement('div');
    loader.setAttribute('class', 'loader');
    const searchCards = document.getElementById('anime-search-cards');
    searchCards.append(loader);

    const query = document.getElementById('search');
    const response = await fetch(`https://api.jikan.moe/v4/anime?q=${query.value}`);
    const data = await response.json();
    const results = data.data;

    searchCards.innerHTML = '';
    if (!results.length) {
        const message = document.createElement('span');
        message.innerHTML = 'No results found';
        searchCards.append(message);
    } else {
        for (const anime of results) {
            const card = document.createElement('article');
            card.setAttribute('class', 'card')
            card.innerHTML =
                `<a href='#'>\n` +
                `<img src=${anime.images.jpg.image_url} alt='${anime.title}'>\n` +
                `<h3>${anime.title}</h3>\n` +
                `</a>`
            searchCards.append(card);
        }
    }
}

try {
    searchAnime();
} catch (error) {
    console.error(error);
}