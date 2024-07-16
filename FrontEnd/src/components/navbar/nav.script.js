document.addEventListener("DOMContentLoaded", function () {
  fetch('../../../src/components/navbar/nav.html')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.text();
    })
    .then(data => {
      const headerElement = document.querySelector('header');
      if (headerElement) {
        headerElement.innerHTML = data;
      } else {
        console.error('Header element not found');
      }
    })
    .catch(error => console.error('Error loading navigation:', error));
});
