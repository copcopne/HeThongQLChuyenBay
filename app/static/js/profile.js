document.addEventListener("DOMContentLoaded", function () {
        // Lấy các mục menu
        const navLinks = document.querySelectorAll(".nav-link");

        // Kiểm tra và thêm class 'active' cho menu tương ứng với trang hiện tại
        if (window.location.pathname === "{{ url_for('update_profile') }}") {
            document.getElementById("profile").classList.add("active");
        } else if (window.location.pathname === "{{ url_for('update_password') }}") {
            document.getElementById("password").classList.add("active");
        }

        // Thêm sự kiện click cho các mục menu để thay đổi 'active'
        navLinks.forEach(link => {
            link.addEventListener("click", function () {
                navLinks.forEach(nav => nav.classList.remove("active"));
                this.classList.add("active");
            });
        });
    });