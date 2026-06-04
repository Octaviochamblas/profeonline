// Contadores animados (count-up) para las cifras del hero del home.
// Sin dependencias. Respeta prefers-reduced-motion y CSP (cargado con nonce).
(function () {
    "use strict";

    var nums = document.querySelectorAll(".hero-stats [data-count-to]");
    if (!nums.length) {
        return;
    }

    var reduceMotion =
        window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function format(value, suffix) {
        return String(value) + (suffix || "");
    }

    function animate(el) {
        var target = parseInt(el.getAttribute("data-count-to"), 10);
        var suffix = el.getAttribute("data-suffix") || "";

        if (isNaN(target)) {
            return;
        }

        if (reduceMotion) {
            el.textContent = format(target, suffix);
            return;
        }

        var duration = 1100;
        var start = null;

        function step(timestamp) {
            if (start === null) {
                start = timestamp;
            }
            var progress = Math.min((timestamp - start) / duration, 1);
            // easeOutCubic
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = format(Math.round(target * eased), suffix);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                el.textContent = format(target, suffix);
            }
        }

        el.textContent = format(0, suffix);
        window.requestAnimationFrame(step);
    }

    if (reduceMotion || !("IntersectionObserver" in window)) {
        nums.forEach(animate);
        return;
    }

    var observer = new IntersectionObserver(
        function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animate(entry.target);
                    obs.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.4 }
    );

    nums.forEach(function (el) {
        observer.observe(el);
    });
})();
