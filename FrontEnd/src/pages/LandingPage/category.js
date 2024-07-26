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

      categoryCard.innerHTML = `
                <img src="${category.image}" alt="${category.name}">
                <h3>${category.name}</h3>
            `;

      categoryCard.addEventListener('click', () => {
        window.location.href = `../../products/products.html?category=${category.id}`;
      });

      categoriesContainer.appendChild(categoryCard);
    });
  }
});