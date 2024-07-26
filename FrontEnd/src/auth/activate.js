document.getElementById('activation-form').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent form from submitting the default way

  const activationCode = document.getElementById('activation-code').value;
  const messageDiv = document.getElementById('message');

  // Ensure the activation code is not empty
  if (!activationCode) {
    messageDiv.textContent = 'Please enter an activation code.';
    messageDiv.style.color = 'red';
    return;
  }

  // Log the activation code for debugging
  console.log('Activation Code:', activationCode);

  // Construct the activation URL correctly
  const activationUrl = `http://127.0.0.1:8000/activate/${activationCode}/`;

  fetch(activationUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ code: activationCode })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Log the response data for debugging
      console.log('Response Data:', data);

      if (data.success) {
        messageDiv.textContent = 'Account activated successfully!';
        messageDiv.style.color = 'green';
        setTimeout(() => {
          window.location.href = '../pages/LandingPage/home.html';
        }, 2000); // Redirect after 2 seconds
      } else {
        messageDiv.textContent = 'Activation failed: ' + data.error;
        messageDiv.style.color = 'red';
      }
    })
    .catch(error => {
      messageDiv.textContent = 'An error occurred: ' + error.message;
      messageDiv.style.color = 'red';
    });
});