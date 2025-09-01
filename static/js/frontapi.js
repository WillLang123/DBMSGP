document.addEventListener("DOMContentLoaded", () => {
      fetchStudents();

      document.getElementById("add-btn").addEventListener("click", openModal);
      document.getElementById("cancel-btn").addEventListener("click", closeModal);
      document.getElementById("add-form").addEventListener("submit", handleAddStudent);
    });

    function fetchStudents() {
      fetch("/get/students")
        .then(res => res.json())
        .then(students => {
          const tbody = document.querySelector("#data-table tbody");
          tbody.innerHTML = "";
          students.forEach(student => tbody.appendChild(createRow(student)));
        })
        .catch(err => console.error("Error loading students:", err));
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

    row.querySelector(".modify-btn").addEventListener("click", () => handleModifyStudent(row, id));
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

    function openModal() {
      document.getElementById("modal").style.display = "block";
      document.getElementById("overlay").style.display = "block";
    }

    function closeModal() {
      document.getElementById("modal").style.display = "none";
      document.getElementById("overlay").style.display = "none";
      document.getElementById("add-form").reset();
    }