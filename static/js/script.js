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