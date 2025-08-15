
const lightModeButton = document.createElement("button");
const savedTheme = localStorage.getItem('theme') || "dark";

document.body.appendChild(lightModeButton);
if (savedTheme === "light") {
    document.body.classList.add("light-mode");
}

lightModeButton.addEventListener("click", () =>
    {
        document.body.classList.toggle("light-mode");

        if (document.body.classList.contains("light-mode")) {
            localStorage.setItem("theme", "light");
        } else {
            localStorage.setItem("theme", "dark");
        }
    }
);
