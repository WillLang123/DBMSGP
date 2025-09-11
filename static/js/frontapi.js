let studentsData = [];
let professorsData = [];
let departmentsData = [];
let coursesData = [];
let sectionsData = [];
let enrollmentsData = [];

let studentStates = { col: null, asc: true };
let professorStates = { col: null, asc: true };
let departmentStates = { col: null, asc: true };
let courseStates = { col: null, asc: true };
let sectionStates = { col: null, asc: true };
let enrollmentStates = { col: null, asc: true };

let studentSearch = "";
let professorSearch = "";
let departmentSearch = "";
let courseSearch = "";
let sectionSearch = "";
let enrollmentSearch = "";

document.addEventListener("DOMContentLoaded", async function () {
  await fetchData();

  const page = document.body.dataset.page;

  if (page === "students") {
    setupSearch({
      onSearch: function (term) {
        studentSearch = term;
        renderTable(studentsData, studentStates, studentSearch, openModifyModal, handleDeleteStudent);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: studentStates,
      onSort: function () {
        renderTable(studentsData, studentStates, studentSearch, openModifyModal, handleDeleteStudent);
      },
      selector: ".sort-btn",
    });

    renderTable(studentsData, studentStates, studentSearch, openModifyModal, handleDeleteStudent);

    document.getElementById("add-btn").addEventListener("click", openAddModal);
    document.getElementById("cancel-btn").addEventListener("click", closeAddModal);
    document.getElementById("add-form").addEventListener("submit", handleAddStudent);
    document.getElementById("modify-form").addEventListener("submit", handleModifyStudent);
    document.getElementById("modify-cancel-btn").addEventListener("click", closeModifyModal);
  }

  if (page === "professors") {
    setupSearch({
      onSearch: function (term) {
        professorSearch = term;
        renderTable(professorsData, professorStates, professorSearch, openModifyModal, handleDeleteProfessor);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: professorStates,
      onSort: function () {
        renderTable(professorsData, professorStates, professorSearch, openModifyModal, handleDeleteProfessor);
      },
      selector: ".sort-btn",
    });

    renderTable(professorsData, professorStates, professorSearch, openModifyModal, handleDeleteProfessor);
  }

  if (page === "departments") {
    setupSearch({
      onSearch: function (term) {
        departmentSearch = term;
        renderTable(departmentsData, departmentStates, departmentSearch, openModifyModal, handleDeleteDepartment);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: departmentStates,
      onSort: function () {
        renderTable(departmentsData, departmentStates, departmentSearch, openModifyModal, handleDeleteDepartment);
      },
      selector: ".sort-btn",
    });

    renderTable(departmentsData, departmentStates, departmentSearch, openModifyModal, handleDeleteDepartment);
  }

  if (page === "courses") {
    setupSearch({
      onSearch: function (term) {
        courseSearch = term;
        renderTable(coursesData, courseStates, courseSearch, openModifyModal, handleDeleteCourse);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: courseStates,
      onSort: function () {
        renderTable(coursesData, courseStates, courseSearch, openModifyModal, handleDeleteCourse);
      },
      selector: ".sort-btn",
    });

    renderTable(coursesData, courseStates, courseSearch, openModifyModal, handleDeleteCourse);
  }

  if (page === "sections") {
    setupSearch({
      onSearch: function (term) {
        sectionSearch = term;
        renderTable(sectionsData, sectionStates, sectionSearch, openModifyModal, handleDeleteSection);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: sectionStates,
      onSort: function () {
        renderTable(sectionsData, sectionStates, sectionSearch, openModifyModal, handleDeleteSection);
      },
      selector: ".sort-btn",
    });

    renderTable(sectionsData, sectionStates, sectionSearch, openModifyModal, handleDeleteSection);
  }

  if (page === "enrollments") {
    setupSearch({
      onSearch: function (term) {
        enrollmentSearch = term;
        renderTable(enrollmentsData, enrollmentStates, enrollmentSearch, openModifyModal, handleDeleteEnrollment);
      },
      selector: "#search-input",
    });

    setupSorting({
      state: enrollmentStates,
      onSort: function () {
        renderTable(enrollmentsData, enrollmentStates, enrollmentSearch, openModifyModal, handleDeleteEnrollment);
      },
      selector: ".sort-btn",
    });

    renderTable(enrollmentsData, enrollmentStates, enrollmentSearch, openModifyModal, handleDeleteEnrollment);
  }
});

async function fetchData() {
  try {
    const studentRes = await fetch("/get/students");
    studentsData = await studentRes.json();

    const professorRes = await fetch("/get/professors");
    professorsData = await professorRes.json();

    const departmentRes = await fetch("/get/departments");
    departmentsData = await departmentRes.json();

    const courseRes = await fetch("/get/courses");
    coursesData = await courseRes.json();

    const sectionRes = await fetch("/get/sections");
    sectionsData = await sectionRes.json();

    const enrollmentRes = await fetch("/get/enrollments");
    enrollmentsData = await enrollmentRes.json();
  } catch (error) {
    console.error("Error loading data:", error);
  }
}

function renderTable(dataArray, state, searchTerm, onModify, onDelete) {
  const tbody = document.querySelector("#data-table tbody");
  tbody.innerHTML = "";

  const filtered = dataArray.filter(function (entry) {
    return entry.some(function (value) {
      return String(value).toLowerCase().includes(searchTerm);
    });
  });

  const sorted = sortTableData(filtered, state);

  sorted.forEach(function (entry) {
    tbody.appendChild(createRow(entry, onModify, onDelete));
  });
}

function createRow(data, onModify, onDelete) {
  const row = document.createElement("tr");
  const id = data[0];

  let cells = "";
  data.forEach(function (value, i) {
    if (i === 0) {
      cells += "<td>" + value + "</td>";
    } else {
      cells += "<td contenteditable>" + value + "</td>";
    }
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
  if (state.col === null) {
    return data;
  }

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
    let arrow;
    if (state.col === colNum) {
      arrow = state.asc ? "↑" : "↓";
    } else {
      arrow = "↓";
    }
    button.textContent = arrow;
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
