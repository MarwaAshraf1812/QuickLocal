document.addEventListener('DOMContentLoaded', () => {
  const categoriesContainer = document.querySelector('.categories-container');

  // Fetch categories from the API
  fetch('http://127.0.0.1:8000/categories/')
    .then(response => response.json())
    .then(data => {
      displayCategories(data);
    })
    .catch(error => console.error('Error fetching categories:', error));

  // Function to display categories
  function displayCategories(categories) {
    categories.forEach(category => {
      const categoryCard = document.createElement('div');
      categoryCard.className = 'category-card';

      const imageUrl = `http://127.0.0.1:8000${category.image}`;  // Prepend the URL

      categoryCard.innerHTML = `
        <img src="${imageUrl}" alt="${category.name}">
        <h3>${category.name}</h3>
      `;

      categoryCard.addEventListener('click', () => {
        window.location.href = `../../products/products.html?category=${category.id}`;
      });

      categoriesContainer.appendChild(categoryCard);
    });
  }
});
