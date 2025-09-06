let studentsData = [];
let professorsData = [];
let departmentsData = [];
let coursesData = [];
let sectionsData = [];
let enrollmentsData = [];

let studentSortState = { column: null, ascending: true };
let studentSearchTerm = "";

document.addEventListener("DOMContentLoaded", async () => {
  await fetchData();

  const page = document.body.dataset.page;

  if (page === "students") {
    setupSearch();
    setupSorting();
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
  } catch (err) {
    console.error("Error loading data:", err);
    studentsData = [];
  }
}

function renderStudentTable() {
  const tbody = document.querySelector("#data-table tbody");
  tbody.innerHTML = "";

  const filtered = studentsData.filter(student =>
    student.some(value =>
      String(value).toLowerCase().includes(studentSearchTerm.toLowerCase())
    )
  );

  const sorted = sortStudentsData(filtered);

  sorted.forEach(student => {
    tbody.appendChild(createRow(student));
  });
}

function createRow(student) {
  const row = document.createElement("tr");

  const [id, email, name, enrollmentyear] = student;

  row.innerHTML = `
    <td>${id}</td>
    <td contenteditable>${name}</td>
    <td contenteditable>${email}</td>
    <td contenteditable>${enrollmentyear}</td>
    <td>
      <button class="modify-btn">Modify</button>
      <button class="delete-btn">Delete</button>
    </td>
  `;

  row.querySelector(".modify-btn").addEventListener("click", () => openModifyModal(student));
  row.querySelector(".delete-btn").addEventListener("click", () => handleDeleteStudent(id));

  return row;
}

function handleAddStudent(e) {
  e.preventDefault();
  const form = e.target;

  const student = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    enrollmentyear: form.enrollmentyear.value.trim()
  };

  fetch("/api/students", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to add student");
      return res.json();
    })
    .then(() => {
      closeAddModal();
      location.reload();
    })
    .catch(err => alert(err.message));
}

function handleModifyStudent(e) {
  e.preventDefault();
  const form = e.target;

  const student = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    enrollmentyear: form.enrollmentyear.value.trim()
  };

  const id = form.id.value;

  fetch(`/api/students/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to update student");
      return res.json();
    })
    .then(() => {
      closeModifyModal();
      location.reload();
    })
    .catch(err => alert(err.message));
}

function handleDeleteStudent(id) {
  if (!confirm("Delete this student? This will remove their enrollments too.")) return;

  fetch(`/api/students/${id}`, { method: "DELETE" })
    .then(res => {
      if (!res.ok) throw new Error("Failed to delete student");
      location.reload();
    })
    .catch(err => alert(err.message));
}

function setupSorting() {
  document.querySelectorAll(".sort-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const column = parseInt(btn.dataset.key);
      if (studentSortState.column === column) {
        studentSortState.ascending = !studentSortState.ascending;
      } else {
        studentSortState.column = column;
        studentSortState.ascending = true;
      }

      updateSortIcons();
      renderStudentTable();
    });
  });
}

function sortStudentsData(data) {
  if (studentSortState.column === null) return data;

  return [...data].sort((a, b) => {
    const valA = a[studentSortState.column];
    const valB = b[studentSortState.column];

    if (typeof valA === "number" && typeof valB === "number") {
      return studentSortState.ascending ? valA - valB : valB - valA;
    }

    return studentSortState.ascending
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });
}

function updateSortIcons() {
  document.querySelectorAll(".sort-btn").forEach(btn => {
    const column = parseInt(btn.dataset.key);
    btn.textContent = studentSortState.column === column
      ? (studentSortState.ascending ? "↑" : "↓")
      : "↓";
  });
}

function setupSearch() {
  const input = document.getElementById("search-input");
  if (!input) return;

  input.addEventListener("input", () => {
    studentSearchTerm = input.value.trim().toLowerCase();
    renderStudentTable();
  });
}
