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

// BLSUNTECH PROJECT SHOWCASE ADDITION V1
document.addEventListener("DOMContentLoaded", () => {
    const showcases = document.querySelectorAll("[data-showcase]");

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        return;
    }

    showcases.forEach(showcase => {
        const slides = [...showcase.querySelectorAll(".showcase-slide")];
        if (slides.length < 2) return;

        let current = 0;

        setInterval(() => {
            const previous = slides[current];

            current = (current + 1) % slides.length;
            const next = slides[current];

            slides.forEach(slide => {
                slide.classList.remove("is-active", "is-previous");
            });

            previous.classList.add("is-previous");
            next.classList.add("is-active");
        }, 3500);
    });
});
