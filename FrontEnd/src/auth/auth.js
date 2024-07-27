document.addEventListener('DOMContentLoaded', function () {
  const registerForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');
  const alertPrase = document.querySelector('.alert-prase'); // Select the alert-prase element

  if (registerForm) {
    registerForm.addEventListener('submit', function (event) {
      event.preventDefault();
      handleRegister();
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();
      handleLogin();
    });
  }

  function displayMessage(message, type) {
    // Create a new <p> element
    const messageElement = document.createElement('p');
    messageElement.classList.add(type === 'error' ? 'error-message' : 'success-message');
    messageElement.textContent = message;

    // Clear previous messages
    alertPrase.innerHTML = '';

    // Append the new message
    alertPrase.appendChild(messageElement);
  }

  async function handleRegister() {
    const formData = new FormData(registerForm);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    try {
      const response = await fetch('http://127.0.0.1:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        displayMessage('Registration successful! Please check your email to activate your account.', 'success');
        setTimeout(() => {
          window.location.href = './activate.html'; // Redirect to activation page
        }, 2000); // Add a short delay before redirect
      } else {
        displayMessage(result.error || 'An error occurred.', 'error');
      }
    } catch (error) {
      console.error('Error:', error);
      displayMessage('An error occurred. Please try again.', 'error');
    }
  }

  async function handleLogin() {
    const formData = new FormData(loginForm);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    try {
      const response = await fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        displayMessage(result.details || 'Login successful. Redirecting...', 'success');
        setTimeout(() => {
          window.location.href = result.redirect || '../pages/LandingPage/home.html'; // Redirect to the specified URL or landing page
        }, 2000); // Add a short delay before redirect
      } else {
        displayMessage(result.error || 'An error occurred.', 'error');
      }
    } catch (error) {
      console.error('Error:', error);
      displayMessage('An error occurred. Please try again.', 'error');
    }
  }
});
