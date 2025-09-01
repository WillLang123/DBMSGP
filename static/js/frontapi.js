let studentsData = [];
let teachersData = [];
let majorsData = [];
let subjectsData = [];
let coursesData = [];
let enrollmentsData = [];

document.addEventListener("DOMContentLoaded", async () => {
  await fetchData();

  const page = document.body.dataset.page;

  if (page === "students") {
    manageStudents();
    document.getElementById("add-btn")?.addEventListener("click", openAddModal);
    document.getElementById("cancel-btn")?.addEventListener("click", closeAddModal);
    document.getElementById("add-form")?.addEventListener("submit", handleAddStudent);
    document.getElementById("modify-form").addEventListener("submit", handleModifySubmit);
    document.getElementById("modify-cancel-btn").addEventListener("click", closeModifyModal);
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

    const [id, fname, lname, email, major_id, enroll_year] = student;

    row.innerHTML = `
      <td>${id}</td>
      <td contenteditable>${fname}</td>
      <td contenteditable>${lname}</td>
      <td contenteditable>${email}</td>
      <td contenteditable>${major_id ?? ""}</td>
      <td contenteditable>${enroll_year}</td>
      <td>
        <button class="modify-btn">Modify</button>
        <button class="delete-btn">Delete</button>
      </td>
    `;

    row.querySelector(".modify-btn").addEventListener("click", () => openModifyModal(student));
    row.querySelector(".delete-btn").addEventListener("click", () => handleDeleteStudent(row, id));

    return row;
  }


    function handleAddStudent(e) {
      e.preventDefault();
      const form = e.target;

      const newStudent = {
        fname: form.fname.value.trim(),
        lname: form.lname.value.trim(),
        email: form.email.value.trim(),
        major_id: form.major_id.value.trim() || null,
        enroll_year: form.enroll_year.value.trim(),
      };

      fetch("/api/students", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newStudent),
      })
        .then(res => {
          if (!res.ok) throw new Error("Failed to add student");
          return res.json();
        })
        .then(student => {
          document.querySelector("#data-table tbody").appendChild(createRow(student));
          closeModal();
        })
        .catch(err => alert(err.message));
    }

    function handleModifyStudent(row, id) {
      const cells = row.querySelectorAll("td");
      const updatedStudent = {
        fname: cells[1].textContent.trim(),
        lname: cells[2].textContent.trim(),
        email: cells[3].textContent.trim(),
        major_id: cells[4].textContent.trim() || null,
        enroll_year: cells[5].textContent.trim(),
      };

      fetch(`/api/students/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedStudent),
      })
        .then(res => {
          if (!res.ok) throw new Error("Failed to update student");
          alert("Student updated!");
        })
        .catch(err => alert(err.message));
    }

    function handleDeleteStudent(row, id) {
      if (!confirm("Delete this student?")) return;

      fetch(`/api/students/${id}`, { method: "DELETE" })
        .then(res => {
          if (!res.ok) throw new Error("Failed to delete student");
          row.remove();
          alert("Student deleted!");
        })
        .catch(err => alert(err.message));
    }

    function openModifyModal(student) {
    const modal = document.getElementById("modify-modal");
    const overlay = document.getElementById("modify-overlay");
    const form = document.getElementById("modify-form");

    form.id.value = student[0]; // ID
    form.fname.value = student[1];
    form.lname.value = student[2];
    form.email.value = student[3];
    form.major_id.value = student[4] ?? "";
    form.enroll_year.value = student[5];

    modal.style.display = "block";
    overlay.style.display = "block";
    }

    function closeModifyModal() {
    document.getElementById("modify-modal").style.display = "none";
    document.getElementById("modify-overlay").style.display = "none";
    document.getElementById("modify-form").reset();
    }

    function handleModifySubmit(e) {
    e.preventDefault();
    const form = e.target;

    const updatedStudent = {
        fname: form.fname.value.trim(),
        lname: form.lname.value.trim(),
        email: form.email.value.trim(),
        major_id: form.major_id.value.trim() || null,
        enroll_year: form.enroll_year.value.trim(),
    };

    const id = form.id.value;

    fetch(`/api/students/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedStudent),
    })
        .then(res => {
        if (!res.ok) throw new Error("Failed to update student");
        return res.json();
        })
        .then(() => {
        closeModifyModal();
        fetchData().then(manageStudents); // Refresh the table
        })
        .catch(err => alert(err.message));
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
