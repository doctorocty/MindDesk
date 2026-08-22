console.log("MindDesk is running.");

const signupForm = document.querySelector(".auth-form");

if (signupForm) {

    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("email-error");

    const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");

const passwordError = document.getElementById("password-error");
const confirmPasswordError = document.getElementById("confirm-password-error");

    signupForm.addEventListener("submit", function (event) {

        emailError.style.display = "none";
emailError.textContent = "";

passwordError.style.display = "none";
passwordError.textContent = "";

confirmPasswordError.style.display = "none";
confirmPasswordError.textContent = "";

        const email = emailInput.value.trim();

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {

            event.preventDefault();

            emailError.textContent =
                "Oh c'mon twin that ain't a valid email address.";

            emailError.style.display = "block";
        }

        const password = passwordInput.value;
const confirmPassword = confirmPasswordInput.value;

const passwordPattern =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;

if (!passwordPattern.test(password)) {

    event.preventDefault();

    passwordError.textContent =
        "Password must be at least 8 characters and include an uppercase letter, lowercase letter, number, and special character.";

    passwordError.style.display = "block";
}

if (password !== confirmPassword) {

    event.preventDefault();

    confirmPasswordError.textContent =
        "Passwords do not match.";

    confirmPasswordError.style.display = "block";
}

    });

}

const toggleButtons = document.querySelectorAll(".toggle-password");

toggleButtons.forEach(button => {

    button.addEventListener("click", () => {

        const input = document.getElementById(button.dataset.target);

       const icon = button.querySelector("i");

if (input.type === "password") {

    input.type = "text";

    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");

} else {

    input.type = "password";

    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");

}
    });

});

const lamp = document.getElementById("themeToggle");

if (lamp) {

    let angle = 0;
    let velocity = 0;
    let animationRunning = false;

    const gravity = 0.22;
    const damping = 0.985;

    const glow = document.querySelector(".lamp-glow");

    // Restore saved theme
    if (localStorage.getItem("minddesk-theme") === "dark") {
        document.body.classList.add("dark");
    }

    function updateGlow() {
        if (!glow) return;

        glow.style.opacity =
            document.body.classList.contains("dark")
                ? "1"
                : "0";
    }

    updateGlow();

    function animateLamp() {

        velocity += (-angle) * gravity;
        velocity *= damping;
        angle += velocity;

        lamp.style.transform = `rotate(${angle}deg)`;

        if (Math.abs(angle) < 0.05 && Math.abs(velocity) < 0.05) {

            lamp.style.transform = "rotate(0deg)";
            angle = 0;
            velocity = 0;
            animationRunning = false;
            return;

        }

        requestAnimationFrame(animateLamp);

    }

    lamp.addEventListener("click", () => {

        document.body.classList.toggle("dark");

        localStorage.setItem(
            "minddesk-theme",
            document.body.classList.contains("dark")
                ? "dark"
                : "light"
        );

        updateGlow();

        velocity += 4;

        if (!animationRunning) {
            animationRunning = true;
            requestAnimationFrame(animateLamp);
        }

    });

}

const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {

    const savedTheme =
        localStorage.getItem("minddesk-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }


    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        const isDark =
            document.body.classList.contains("dark-mode");

        localStorage.setItem(
            "minddesk-theme",
            isDark ? "dark" : "light"
        );

    });

}

    updateThemeButton();

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        const isDark =
            document.body.classList.contains("dark-mode");

        localStorage.setItem(
            "minddesk-theme",
            isDark ? "dark" : "light"
        );

        updateThemeButton();

    });
         

document.addEventListener("DOMContentLoaded", function () {

    const flashMessages =
        document.querySelectorAll(".flash-message");

    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.remove();

        }, 4000);

    });

});