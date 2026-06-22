(function () {
    "use strict";

    function initialize(root) {
        var player = (root || document).querySelector("[data-evaluation-deadline]");
        if (!player || player.dataset.timerReady === "true") return;
        player.dataset.timerReady = "true";
        var deadline = Date.parse(player.dataset.evaluationDeadline);
        var output = player.querySelector("[data-evaluation-countdown]");
        var form = player.querySelector("[data-evaluation-form]");
        var timer = window.setInterval(function () {
            var seconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
            var minutes = Math.floor(seconds / 60);
            output.textContent = minutes + ":" + String(seconds % 60).padStart(2, "0");
            if (seconds === 0) {
                window.clearInterval(timer);
                if (form) form.requestSubmit();
            }
        }, 250);
    }

    document.addEventListener("DOMContentLoaded", function () { initialize(document); });
    document.addEventListener("htmx:afterSwap", function (event) { initialize(event.target); });
})();
