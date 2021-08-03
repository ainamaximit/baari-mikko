function login() {
  let loginFlash = document.getElementById('flash');

  loginFlash.classList.add('show');

  // Return original icon
  setTimeout(function () {
    loginContent.classList.remove('show');
  }, 5000);

  window.location.assign(loginUrl);
}

function addRecipeIngredientRow() {
  let ingredientRow = document.getElementById('first-ingredient-row');
  let ingredientsList = document.getElementById('ingredients-list');

  let newRow = ingredientRow.cloneNode(true);
  newRow.childNodes.forEach((element, _, __) => {
    const name = element.getAttribute('name')

    if (name === 'ingredient') {
      element.value = null;
    } else if (name === 'amount') {
      element.value = 0;
    }
  })
  
  ingredientsList.append(newRow);
}

function removeRecipeIngredientRow(element) {
  let parent = element.parentElement;
  parent.delete();
}