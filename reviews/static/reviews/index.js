async function topAiringAnime() {
    const response = await fetch('https://api.jikan.moe/v4/top/anime?filter=airing');
    const data = await response.json();
    const airingAnime = data.data.splice(0, 5);
    

    const topCards = document.getElementById('top-anime-cards');
    for (const anime of airingAnime) {
        const card = document.createElement('div');
        card.setAttribute('class', 'card')
        card.innerHTML = `<img src=${anime.images.jpg.image_url} alt='${anime.title}'>\n` +
            `<h3>${anime.title}</h3>`
        topCards.append(card);
    }
}

try {
    topAiringAnime();
} catch (error) {
    console.error(error);
}