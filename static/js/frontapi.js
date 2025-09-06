let studentsData = [];
let professorsData = [];
let departmentsData = [];
let coursesData = [];
let sectionsData = [];
let enrollmentsData = [];

let studentStates = { col: null, asc: true };
let studentSearch = "";

document.addEventListener("DOMContentLoaded", async function () {
  await fetchData();

  const page = document.body.dataset.page;

  if (page === "students") {
    setupSearch({
      onSearch: function (term) {
        studentSearch = term;
        renderStudentTable();
      },
      selector: "#search-input"
    });

    setupSorting({
      state: studentStates,
      onSort: renderStudentTable,
      selector: ".sort-btn"
    });

    renderStudentTable();

    document.getElementById("add-btn")?.addEventListener("click", openAddModal);
    document.getElementById("cancel-btn")?.addEventListener("click", closeAddModal);
    document.getElementById("add-form")?.addEventListener("submit", handleAddStudent);
    document.getElementById("modify-form")?.addEventListener("submit", handleModifyStudent);
    document.getElementById("modify-cancel-btn")?.addEventListener("click", closeModifyModal);
  }
});

async function fetchData() {
  try {
    const res = await fetch("/get/students");
    studentsData = await res.json();
  } catch (error) {
    console.error("Error loading data:", error);
    studentsData = [];
  }
}

function renderStudentTable() {
  const tbody = document.querySelector("#data-table tbody");
  tbody.innerHTML = "";

  const filtered = studentsData.filter(function (student) {
    return student.some(function (value) {
      return String(value).toLowerCase().includes(studentSearch);
    });
  });

  const sorted = sortTableData(filtered, studentStates);

  sorted.forEach(function (student) {
    tbody.appendChild(createRow(student, openModifyModal, handleDeleteStudent));
  });
}

function createRow(data, onModify, onDelete) {
  const row = document.createElement("tr");
  const id = data[0];

  let cells = "";
  data.forEach(function (value, i) {
    cells += i === 0
      ? "<td>" + value + "</td>"
      : "<td contenteditable>" + value + "</td>";
  });

  row.innerHTML =
    cells +
    `
    <td>
      <button class="modify-btn">Modify</button>
      <button class="delete-btn">Delete</button>
    </td>
  `;

  row.querySelector(".modify-btn").addEventListener("click", function () {
    onModify(data);
  });
  row.querySelector(".delete-btn").addEventListener("click", function () {
    onDelete(id);
  });

  return row;
}

function setupSorting(options) {
  const state = options.state;
  const onSort = options.onSort;
  const selector = options.selector || ".sort-btn";

  document.querySelectorAll(selector).forEach(function (button) {
    button.addEventListener("click", function () {
      const colNum = parseInt(this.getAttribute("data-key"));

      if (state.col === colNum) {
        state.asc = !state.asc;
      } else {
        state.col = colNum;
        state.asc = true;
      }

      updateSortIcons(state, selector);
      onSort();
    });
  });
}

function sortTableData(data, state) {
  if (state.col === null) return data;

  const col = state.col;
  const asc = state.asc;

  return data.slice().sort(function (a, b) {
    const A = a[col];
    const B = b[col];

    if (typeof A === "number" && typeof B === "number") {
      return asc ? A - B : B - A;
    }

    const textA = String(A).toLowerCase();
    const textB = String(B).toLowerCase();

    if (textA < textB) return asc ? -1 : 1;
    if (textA > textB) return asc ? 1 : -1;
    return 0;
  });
}

function updateSortIcons(state, selector) {
  const buttons = document.querySelectorAll(selector);
  buttons.forEach(function (button) {
    const colNum = parseInt(button.getAttribute("data-key"));
    button.textContent = state.col === colNum ? (state.asc ? "↑" : "↓") : "↓";
  });
}

function setupSearch(options) {
  const onSearch = options.onSearch;
  const selector = options.selector || "[data-search]";
  const input = document.querySelector(selector);
  if (!input) return;

  input.addEventListener("input", function () {
    const term = input.value.trim().toLowerCase();
    onSearch(term);
  });
}
