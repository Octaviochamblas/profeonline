(function () {
  "use strict";

  var dashboard = document.querySelector("[data-bank-coverage]");

  if (dashboard) {
    var area = dashboard.querySelector("[data-filter-area]");
    var subject = dashboard.querySelector("[data-filter-subject]");
    var topic = dashboard.querySelector("[data-filter-topic]");
    var editorial = dashboard.querySelector("[data-filter-editorial]");
    var search = dashboard.querySelector("[data-filter-search]");
    var rows = Array.from(dashboard.querySelectorAll("[data-coverage-row]"));
    var empty = dashboard.querySelector("[data-filter-empty]");

    function syncCascades() {
      Array.from(subject.options).forEach(function (option) {
        option.hidden = Boolean(area.value && option.dataset.area !== area.value);
      });
      if (subject.selectedOptions[0] && subject.selectedOptions[0].hidden) subject.value = "";

      Array.from(topic.options).forEach(function (option) {
        option.hidden = Boolean(subject.value && option.dataset.subject !== subject.value);
      });
      if (topic.selectedOptions[0] && topic.selectedOptions[0].hidden) topic.value = "";
    }

    function update() {
      syncCascades();
      var query = search.value.trim().toLocaleLowerCase("es");
      var visible = [];

      rows.forEach(function (row) {
        var matches =
          (!area.value || row.dataset.area === area.value) &&
          (!subject.value || row.dataset.subject === subject.value) &&
          (!topic.value || row.dataset.topic === topic.value) &&
          (!editorial.value || row.dataset.editorial === editorial.value) &&
          (!query || row.dataset.title.indexOf(query) !== -1);
        row.hidden = !matches;
        if (matches) visible.push(row);
      });

      dashboard.querySelector("[data-total-resources]").textContent = visible.length;
      dashboard.querySelector("[data-total-empty]").textContent = visible.filter(function (row) {
        return row.dataset.state === "empty";
      }).length;
      dashboard.querySelector("[data-total-published]").textContent = visible.reduce(function (sum, row) {
        return sum + Number(row.dataset.published || 0);
      }, 0);
      dashboard.querySelector("[data-total-missing]").textContent = visible.reduce(function (sum, row) {
        return sum + Number(row.dataset.missing || 0);
      }, 0);
      dashboard.querySelector("[data-total-editorial-complete]").textContent = visible.filter(function (row) {
        return row.dataset.editorial === "complete";
      }).length;
      dashboard.querySelector("[data-total-editorial-pending]").textContent = visible.filter(function (row) {
        return row.dataset.editorial === "pending";
      }).length;
      empty.hidden = visible.length !== 0;
    }

    [area, subject, topic, editorial].forEach(function (select) {
      select.addEventListener("change", update);
    });
    search.addEventListener("input", update);
  }

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
