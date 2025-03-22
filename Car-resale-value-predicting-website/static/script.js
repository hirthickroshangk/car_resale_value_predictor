document.addEventListener("DOMContentLoaded", function () {
    // Animate Title Color Change
    const title = document.querySelector(".animate-title");
    setInterval(() => {
        title.classList.toggle("text-blue-500");
        title.classList.toggle("text-purple-500");
    }, 1000);

    // Button Hover Effect
    const buttons = document.querySelectorAll("button");
    buttons.forEach(button => {
        button.addEventListener("mouseover", () => {
            button.style.transform = "scale(1.1)";
            button.style.transition = "transform 0.3s ease-in-out";
        });
        button.addEventListener("mouseleave", () => {
            button.style.transform = "scale(1)";
        });
    });

    // Smooth Page Load Effect
    document.body.style.opacity = "1";
    document.body.style.transition = "opacity 1s ease-in-out";
});
