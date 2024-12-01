document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById("username");
    const feedback = document.getElementById("feedback");
    const submitButton = document.getElementById("submit-btn");
    const form = document.querySelector("form");

    // Lưu giá trị ban đầu của username (nếu có)
    const initialUsername = usernameInput.value.trim();

    usernameInput.addEventListener("blur", function () {
        const username = usernameInput.value.trim();

        if (username === "") {
            // Tên người dùng trống, không hợp lệ
            feedback.innerHTML = '<div class="alert alert-danger" role="alert">Tên người dùng không được trống!</div>';
            submitButton.disabled = true;
            return;
        }

        if (username === initialUsername && initialUsername !== "") {
            // Nếu tên không thay đổi (cập nhật) hoặc đang đăng ký (ban đầu rỗng)
            feedback.innerHTML = '';
            submitButton.disabled = false;
            return;
        }

        // Kiểm tra tính khả dụng của username mới
        fetch(`/check-availability/${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    feedback.innerHTML = '<div class="alert alert-success" role="alert">Tên người dùng khả dụng!</div>';
                    submitButton.disabled = false;
                } else {
                    feedback.innerHTML = '<div class="alert alert-danger" role="alert">Tên người dùng không khả dụng!</div>';
                    submitButton.disabled = true;
                }
            })
            .catch(error => {
                console.error('Lỗi:', error);
            });
    });

    form.onsubmit = function (event) {

        if (submitButton.disabled) {
            event.preventDefault();
            alert("Vui lòng kiểm tra tên người dùng trước khi tiếp tục.");
        }
    };
});
