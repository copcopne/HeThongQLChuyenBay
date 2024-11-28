document.addEventListener('DOMContentLoaded', function() {

    const usernameInput = document.getElementById("username");
    const feedback = document.getElementById("feedback");
    const submitButton = document.getElementById("submit-btn");

    usernameInput.addEventListener("blur", function () {
        const username = usernameInput.value.trim();

            if (username === "") {
                feedback.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
                submitButton.disabled = true;
                return;
            }

            fetch(`/check-availability/${username}`)
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        feedback.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                        submitButton.disabled = false;
                    } else {
                        feedback.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
                        submitButton.disabled = true;
                    }
                })
                .catch(error => {
                    console.error('Lỗi:', error);
                });
        });

    document.querySelector("form").onsubmit = function(event) {
        const submitButton = document.getElementById("submit-btn");
        if (submitButton.disabled) {
            event.preventDefault();
            alert("Vui lòng kiểm tra tên người dùng trước khi đăng ký.");
        }
        if (passwordInput.value !== confirmInput.value) {
            event.preventDefault();
            errorMessage.style.display = 'block';
        }
    };
});

