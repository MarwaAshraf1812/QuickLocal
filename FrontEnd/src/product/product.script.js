// Function to get query parameters from the URL
function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    id: params.get('id')
  };
}

// Get the product ID from the URL
const queryParams = getQueryParams();
const productId = Number(queryParams.id); // Convert to number

// Fetch data from JSON or API
fetch("../../JSON/data.test.json")
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    const product = data.shopping.find(item => item.productId === productId); // Correctly access the shopping array
    if (product) {
      displayProductDetails(product);
    } else {
      console.error('Product not found');
    }
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });


// Function to display product details
function displayProductDetails(product) {
  const productDetailContainer = document.getElementById('product-detail');

  if (productDetailContainer) {
    productDetailContainer.innerHTML = `
      <img src="${product.image}" alt="${product.name}">
      <div class="card">
        <h2>${product.name}</h2>
        <p class="description">Description: ${product.description}</p>
        <p class="productInformation">Product Information: ${product.productInformation}</p>
        <p class="price">Price: $${product.price}</p>
        <p class="stock">Stock: ${product.stock}</p>
        <p class="rating">Rating: ${product.rating}</p>
        <p class="status">Status: ${product.status}</p>
        <p class="color">Color: ${product.color}</p>
        <p class="size">Size: ${product.size}</p>
        <p class="tags">Tags: ${product.tags.join(', ')}</p>
        <button class="btn add-cart">ADD TO CART</button>
        <button class="btn buy">Buy Now</button>


        </div>
    `;
  } else {
    console.error('Element with ID "product-detail" not found.');
  }
}
