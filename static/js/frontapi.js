/*
document.addEventListener("DOMContentLoaded", () => {
  fetchStudents();

  document.getElementById("add-btn").addEventListener("click", openAddModal);
  document.getElementById("cancel-btn").addEventListener("click", closeAddModal);
  document.getElementById("add-form").addEventListener("submit", submitNewStudent);
});

function fetchStudents() {
  fetch("/api/students")
    .then((res) => res.json())
    .then((students) => populateStudentTable(students))
    .catch((err) => console.error("Error fetching students:", err));
}

function populateStudentTable(students) {
  const tbody = document.querySelector("#data-table tbody");
  tbody.innerHTML = "";

  students.forEach((student) => {
    const row = createTableRow(student);
    tbody.appendChild(row);
  });
}

function createTableRow(student) {
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${student.id}</td>
    <td contenteditable="true">${student.fname}</td>
    <td contenteditable="true">${student.lname}</td>
    <td contenteditable="true">${student.email}</td>
    <td contenteditable="true">${student.major_id ?? ""}</td>
    <td contenteditable="true">${student.enroll_year}</td>
    <td>
      <button class="modify-btn">Modify</button>
      <button class="delete-btn">Delete</button>
    </td>
  `;

  row.querySelector(".modify-btn").addEventListener("click", () => modifyRow(row));
  row.querySelector(".delete-btn").addEventListener("click", () => deleteRow(row));

  return row;
}


function openAddModal() {
  document.getElementById("modal").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function closeAddModal() {
  document.getElementById("modal").style.display = "none";
  document.getElementById("overlay").style.display = "none";
  document.getElementById("add-form").reset();
}

function submitNewStudent(event) {
  event.preventDefault();
  const form = event.target;

  const newStudent = {
    fname: form.fname.value.trim(),
    lname: form.lname.value.trim(),
    email: form.email.value.trim(),
    major_id: form.major_id.value.trim() || null,
    enroll_year: form.enroll_year.value.trim(),
  };

  console.log("Submitting new student", newStudent);

  fetch("/api/students", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newStudent),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to add student");
      return res.json();
    })
    .then((createdStudent) => {
      // Add new row to table
      const tbody = document.querySelector("#data-table tbody");
      tbody.appendChild(createTableRow(createdStudent));
      closeAddModal();
    })
    .catch((err) => alert(err.message));
}

function modifyRow(row, id) {
  const cells = row.querySelectorAll("td");
  const updatedData = {
    id: id,
    fname: cells[1].textContent.trim(),
    lname: cells[2].textContent.trim(),
    email: cells[3].textContent.trim(),
    major_id: cells[4].textContent.trim() || null,
    enroll_year: cells[5].textContent.trim(),
  };

  console.log("Modifying student", updatedData);

  fetch(`/api/students/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedData),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to update student");
      alert("Student updated successfully!");
    })
    .catch((err) => alert(err.message));
}

function deleteRow(id, rowElement) {
  if (!confirm("Are you sure you want to delete this student?")) return;

  fetch(`/api/students/${id}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to delete student");
      // Remove row from table on success
      rowElement.remove();
      alert("Student deleted successfully!");
    })
    .catch((err) => alert(err.message));
}
    function createTableRow(student) {
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${student.id}</td>
    <td contenteditable="true">${student.fname}</td>
    <td contenteditable="true">${student.lname}</td>
    <td contenteditable="true">${student.email}</td>
    <td contenteditable="true">${student.major_id ?? ""}</td>
    <td contenteditable="true">${student.enroll_year}</td>
    <td>
      <button class="modify-btn">Modify</button>
      <button class="delete-btn">Delete</button>
    </td>
  `;

  row.querySelector(".modify-btn").addEventListener("click", () => modifyRow(row));
  row.querySelector(".delete-btn").addEventListener("click", () => deleteRow(row));

  return row;
}

*/