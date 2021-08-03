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
  const template = document.createElement('template');
  template.innerHTML = `
                <div class="ingredients-list-row" id="first-ingredient-row">
                    <div class="ingredients-list-row-remove">
                        <button onclick="removeRecipeIngredientRow(this)">-</button>
                    </div>
                    <div class="ingredients-list-row-ingredient">
                        <select name="ingredient">
                            <option>Lol</option>
                            <option>Asd</option>
                        </select>
                    </div>
                    <div class="ingredients-list-row-amount">
                        <input name="amount" type="number" step="1"> ml
                    </div>
                </div>
  `.trim();
  let ingredientsList = document.getElementById('ingredients-list');

  ingredientsList.append(template.content.firstChild);
}

function removeRecipeIngredientRow(element) {
  let parent = element.parentElement;
  parent.delete();
}