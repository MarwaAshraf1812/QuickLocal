# Project Structure
Here is the directory structure for the landing page:
```plaintext
QuickLocal/
└── FrontEnd/
    └── src/
        └── pages/
            └── LandingPage/
                ├── category.js
                ├── documentation.md
                ├── land.css
                ├── displayProducts.js
                └── home.html
```
## `home.html`
- The main HTML file for the landing page includes:
- Header: Empty header element included in the HTML file for future use.
- Banner Section: Displays promotional content and an image.
- Gallery Section: Features a main image and thumbnail images.
- Categories Section: Dynamically populated with categories fetched from an API.
- Products Section: Dynamically populated with products fetched from an API.
- Footer: Empty footer element included in the HTML file for future use.

## `category.js`
### Overview

The `category.js` script is responsible for fetching categories from the API and displaying them on the landing page. Each category is shown as a clickable card that redirects users to a specific products page.

### Detailed Explanation

1. **Event Listener for DOM Content Loaded**

  - The script waits until the DOM content is fully loaded before executing, ensuring that all HTML elements are available.

2. Selecting the Categories Container
3. Fetching Category
  - Fetches categories from the API endpoint /categories/, expects a JSON response, and passes it to the displayCategories function. Logs any errors encountered during the fetch operation.
