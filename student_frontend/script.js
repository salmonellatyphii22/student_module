const BASE_URL = "http://127.0.0.1:8000";

// ✅ LOAD STUDENTS
async function loadStudents() {
    const res = await fetch(`${BASE_URL}/students/`);
    const data = await res.json();

    let container = document.getElementById("studentList");
    container.innerHTML = "";

    data.forEach(s => {
        container.innerHTML += `
            <div>
                <b>${s.FirstName} ${s.LastName}</b> (${s.Email})
                <button onclick="deleteStudent(${s.Student_ID})">Delete</button>
                <button onclick="updateStudent(${s.Student_ID})">Update</button>
            </div>
        `;
    });
}

// ✅ ADD STUDENT
async function addStudent() {
    const student = {
        FirstName: document.getElementById("fname").value,
        LastName: document.getElementById("lname").value,
        Email: document.getElementById("email").value,
        Phone_no: document.getElementById("phone").value,
        Address: document.getElementById("address").value,
        EnrollmentYear: parseInt(document.getElementById("year").value),
        Dept_ID: parseInt(document.getElementById("dept").value),
        Date_of_Birth: document.getElementById("dob").value
    };

    await fetch(`${BASE_URL}/students/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(student)
    });

    loadStudents();
}

// ✅ DELETE
async function deleteStudent(id) {
    await fetch(`${BASE_URL}/students/${id}`, {
        method: "DELETE"
    });

    loadStudents();
}

// ✅ UPDATE (PARTIAL using PATCH)
async function updateStudent(id) {
    const newName = prompt("Enter new First Name:");

    await fetch(`${BASE_URL}/students/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            FirstName: newName
        })
    });

    loadStudents();
}