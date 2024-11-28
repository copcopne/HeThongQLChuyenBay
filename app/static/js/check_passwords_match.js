document.addEventListener('DOMContentLoaded', function() {

    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirm_password");
    const errorMessage = document.getElementById("error-message");

    function checkPasswordsMatch() {
        if (passwordInput.value !== confirmInput.value && confirmInput.value !=="") {
            errorMessage.style.display = 'block';
        } else {
            errorMessage.style.display = 'none';
        }
    }
    passwordInput.addEventListener("input", checkPasswordsMatch);
    confirmInput.addEventListener("input", checkPasswordsMatch);
    document.querySelector("form").onsubmit = function(event) {
        if (passwordInput.value !== confirmInput.value) {
            event.preventDefault();
            errorMessage.style.display = 'block';
        }
    };

});