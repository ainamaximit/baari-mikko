function login() {
  var loginFlash = document.getElementById('flash');

  loginFlash.classList.add('show');

  // Return original icon
  setTimeout(function () {
    loginContent.classList.remove('show');
  }, 5000);

  window.location.assign(loginUrl);
}