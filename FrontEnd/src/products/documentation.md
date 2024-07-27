# QuickLocal Products Page

## Description
This project is a simple front-end application for displaying products from a category using data fetched from a backend API. The application is built using HTML, CSS, and JavaScript.

## Installation
To set up this project locally, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/MarwaAshraf1812/QuickLocal.git
2. Navigate to the project directory: ```bash
                                      cd QuickLocal
2. Ensure you have a local server running at http://127.0.0.1:8000 to fetch category products.

## Detailed Explanation of the Fetch Method
- URLSearchParams: This API is used to parse the query string of the current URL to extract the category parameter.
- fetch(): The fetch function is used to make an HTTP GET request to the API endpoint, which returns a promise.
- Response Handling: The response is checked for ok status. If the - response is not ok, an error is thrown.
- JSON Parsing: The response is parsed as JSON.
- Data Validation: The parsed data is checked for the products - property.
- Display Products: If products are found, they are passed to the - displayProducts function, which dynamically generates HTML content - and inserts it into the DOM.

## Function to Display Products
- The displayProducts function takes an array of products and dynamically creates HTML elements to display each product.

- productList.innerHTML = '': Clears any existing content in the product list container.
- forEach(product => { ... }): Iterates over each product in the array.
- document.createElement('div'): Creates a new div element for each product.
- listItem.innerHTML = ...: Sets the inner HTML of the div to include product details such as the image, name, price, offers, and a link to the product detail page.
- productList.appendChild(listItem): Appends the newly created div to the product list container.