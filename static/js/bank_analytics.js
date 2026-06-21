(function () {
  "use strict";

  var effectiveness = document.querySelector("[data-effectiveness-dashboard]");
  if (effectiveness) {
    var studentSearch = effectiveness.querySelector("[data-student-search]");
    var studentRows = Array.from(effectiveness.querySelectorAll("[data-student-row]"));
    var actionButtons = effectiveness.querySelectorAll("[data-student-action]");

    studentSearch.addEventListener("input", function () {
      var query = studentSearch.value.trim().toLocaleLowerCase("es");
      studentRows.forEach(function (row) {
        row.hidden = Boolean(query && row.dataset.searchText.indexOf(query) === -1);
      });
    });

    actionButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var shouldCheck = button.dataset.studentAction === "all";
        studentRows.forEach(function (row) {
          if (!row.hidden || !shouldCheck) {
            row.querySelector('input[type="checkbox"]').checked = shouldCheck;
          }
        });
      });
    });
  }
})();
