// Function to fetch and display products based on category ID
function fetchProducts(categoryId) {
  const apiUrl = `http://127.0.0.1:8000/category-products/?category=${categoryId}&subcategories=1`;

  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      console.log('Fetched products:', data);

      // Assuming the products are in the 'products' field of the response
      displayProducts(data.products); // Update based on the actual structure of your API response
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to display products
function displayProducts(products) {
  const productList = document.getElementById('product-list');

  // Clear existing products
  productList.innerHTML = '';

  // Loop through each product and create HTML elements
  products.forEach(product => {
    const listItem = document.createElement('div');
    listItem.className = 'product-item';

    listItem.innerHTML = `
      <img src="${product.image || '/path/to/default/image.png'}" alt="${product.name}">
      <h5>${product.name}</h5>
      <h4 class="price">$${product.price}</h4>
      ${product.offers ? `<p class="offers">Offers: ${product.offers}</p>` : ''}
      <a href="../product/product.html?id=${product.id}" class="view-product-btn">View Product</a>
    `;
    productList.appendChild(listItem);
  });
}
