const API_URL = "http://127.0.0.1:8000";

// GET students
function loadStudents() {
  fetch(`${API_URL}/students`)
    .then(res => res.json())
    .then(data => {
      console.log(data);
    });
}

// ADD student
function addStudent() {
  const name = document.getElementById("name").value;
  const age = document.getElementById("age").value;
  const course = document.getElementById("course").value;

  fetch(`${API_URL}/students`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, age, course })
  })
  .then(res => res.json())
  .then(data => {
    alert("Student Added");
  });
}