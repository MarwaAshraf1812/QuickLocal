document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const categoryId = urlParams.get('category');

  if (!categoryId) {
    console.error('Category ID not found in URL.');
    return;
  }

  const productsApiUrl = `http://127.0.0.1:8000/category-products/?category=${categoryId}&subcategories=1`;

  fetch(productsApiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      if (data && data.products) {
        displayProducts(data.products); // Ensure we access the correct property
      } else {
        console.error('No products found in the response');
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });

  // Function to display products
  function displayProducts(products) {
    // Get the product list container
    const productList = document.getElementById('product-list');

    // Clear any existing content
    productList.innerHTML = '';

    // Loop through each product and create HTML elements
    products.forEach(product => {
      // Create a list item for each product
      const listItem = document.createElement('div');
      listItem.className = 'product-item';

      // Create the HTML structure for the product
      listItem.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <h5>${product.name}</h5>
        <h4 class="price">$${product.price}</h4>
        ${product.offers ? `<p class="offers">Offers: ${product.offers}</p>` : ''}
        <a href="../product/product.html?id=${product.id}" class="view-product-btn">View Product</a>
      `;
      productList.appendChild(listItem);
    });
  }
});