document.addEventListener("DOMContentLoaded", function () {
  fetch('/src/components/footer/footer.html')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.statusText);
      }
      return response.text();
    })
    .then(data => {
      const footerElement = document.querySelector('footer');
      if (footerElement) {
        footerElement.innerHTML = data;
      } else {
        console.error('Footer element not found');
      }
    })
    .catch(error => console.error('Error loading footer:', error));
});