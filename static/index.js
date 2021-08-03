function login() {
  var loginContent = document.getElementById('login-content');
  var originalImage = loginContent.getAttribute('src');

  loginContent.setAttribute('src', './left-arrow.png');

  // Return original icon
  setTimeout(function () {
    loginContent.setAttribute('src', originalImage);
  }, 5000);

  window.location(loginUrl);
}