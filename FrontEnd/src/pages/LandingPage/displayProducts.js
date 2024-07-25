document.addEventListener('DOMContentLoaded', () => {
  const productsContainer = document.querySelector('.products-container');

  // Fetch products from the API
  fetch('http://127.0.0.1:8000/products/')
    .then(response => response.json())
    .then(data => {
      displayProducts(data);
    })
    .catch(error => console.error('Error fetching products:', error));

  // Function to display products
  function displayProducts(products) {
    products.forEach(product => {
      const productCard = document.createElement('div');
      productCard.className = 'product-card';

      productCard.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <h4 class="price">$${product.price}</h4>
                ${product.offers ? `<p class="offers">Offers: ${product.offers}</p>` : ''}
                <a href="../product/product.html?id=${product.id}" class="view-product-btn">View Product</a>
            `;

      productsContainer.appendChild(productCard);
    });
  }
});
