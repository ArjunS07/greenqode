let form = document.getElementById('creationForm');
form.addEventListener('change', validateForm);

function validateForm() {
    let name = document.getElementById('groupName').value;
    let quantityInputFields = document.getElementsByClassName('item-quantity-input');
    let submitBtn = document.getElementById('submitbtn');


    var isOnlyZeros = true;
    for (var i = 0; i < quantityInputFields.length; i++) {
        if (quantityInputFields[i].value != 0) {
            isOnlyZeros = false;
            break;
        }
    }

    var hasValidInput = false;
    if (name != '' && !isOnlyZeros) {
        hasValidInput = true;
    }

    if (hasValidInput) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}