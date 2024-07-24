document.addEventListener('DOMContentLoaded', () => {
  const apiUrl = 'http://127.0.0.1:8000/categories/';
  const container = document.querySelector('.categories-container');

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      console.log('Fetched categories:', data); // Log fetched data to check the number of categories

      // Limit the number of categories displayed to 10
      const categories = data.slice(0, 10);
      console.log('Displaying categories:', categories); // Log the categories being displayed

      categories.forEach(category => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.onclick = () => window.location.href = `/products?category=${category.id}`;

        const img = document.createElement('img');
        img.src = category.image || '/assets/images/num5.png'; // Fallback image if none is provided

        const title = document.createElement('h3');
        title.textContent = category.name;

        card.appendChild(img);
        card.appendChild(title);

        container.appendChild(card);
      });
    })
    .catch(error => console.error('Error fetching categories:', error));
});
