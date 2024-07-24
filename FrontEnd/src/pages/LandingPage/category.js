document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const categoryId = urlParams.get('category');

  if (!categoryId) {
    console.error('Category ID not found in URL.');
    return;
  }

  const productsApiUrl = `http://127.0.0.1:8000/category-products/?category=${categoryId}&subcategories=1`;

  fetch(productsApiUrl, {
    method: 'GET',
    redirect: 'follow' // This option is the default behavior, but explicitly stating it can be helpful.
  })
    .then(response => {
      if (response.redirected) {
        console.warn('Redirected to:', response.url);
      }
      return response.json();
    })
    .then(data => {
      console.log('Fetched products:', data);

      const productList = document.getElementById('product-list');
      productList.innerHTML = '';

      data.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';

        const img = document.createElement('img');
        img.src = product.image || '/assets/images/placeholder.png';

        const title = document.createElement('h3');
        title.textContent = product.name;

        const price = document.createElement('p');
        price.textContent = `$${product.price}`;

        productCard.appendChild(img);
        productCard.appendChild(title);
        productCard.appendChild(price);

        productList.appendChild(productCard);
      });
    })
    .catch(error => console.error('Error fetching products:', error));
});
