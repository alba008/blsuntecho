document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".nav-toggle");
    const navigation = document.querySelector(".nav-links");

    if (!toggle || !navigation) return;

    function closeNavigation() {
        navigation.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", () => {
        const isOpen = navigation.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
    });

    navigation.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeNavigation);
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") closeNavigation();
    });

    document.addEventListener("click", event => {
        if (!navigation.contains(event.target) && !toggle.contains(event.target)) {
            closeNavigation();
        }
    });
});
