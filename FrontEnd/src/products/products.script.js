fetch("../../JSON/data.test.json")
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    displayProducts(data.shopping);
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

// Function to display products
function displayProducts(products) {
  // Get the product list container
  const productList = document.getElementById('product-list');

  // Loop through each product and create HTML elements
  products.forEach(product => {
    // Create a list item for each product
    const listItem = document.createElement('div');
    listItem.className = 'product-item';

    // Create the HTML structure for the product
    listItem.innerHTML = `
      <img src="${product.image}" alt="${product.name}">
      <h5>${product.name}</h5>
      <p class="price">${product.price}</p>
      ${product.offers ? `<p class="offers">Offers: ${product.offers}</p>` : ''}
      <a href="../product/product.html?id=${product.productId}" class="view-product-btn">View Product</a>
    `;
    productList.appendChild(listItem);
  });
}
