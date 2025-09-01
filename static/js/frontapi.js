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