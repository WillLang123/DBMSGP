let studentsData = [];
let professorsData = [];
let departmentsData = [];
let coursesData = [];
let sectionsData = [];
let enrollmentsData = [];

document.addEventListener("DOMContentLoaded", async () => {
  await fetchData();

  const page = document.body.dataset.page;

  if (page === "students") {
    manageStudents();
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
    console.error("Error loading students:", err);
    studentsData = [];
  }
}

function manageStudents() {
  const tbody = document.querySelector("#data-table tbody");
  tbody.innerHTML = "";
  studentsData.forEach(student => {
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

function openModifyModal(student) {
  const modal = document.getElementById("modify-modal");
  const overlay = document.getElementById("modify-overlay");
  const form = document.getElementById("modify-form");

  form.id.value = student[0];
  form.email.value = student[1];
  form.name.value = student[2];
  form.enrollmentyear.value = student[3];

  modal.style.display = "block";
  overlay.style.display = "block";
}

function closeModifyModal() {
  document.getElementById("modify-modal").style.display = "none";
  document.getElementById("modify-overlay").style.display = "none";
  document.getElementById("modify-form").reset();
}

function openAddModal() {
  document.getElementById("add-modal").style.display = "block";
  document.getElementById("add-overlay").style.display = "block";
}

function closeAddModal() {
  document.getElementById("add-modal").style.display = "none";
  document.getElementById("add-overlay").style.display = "none";
  document.getElementById("add-form").reset();
}
