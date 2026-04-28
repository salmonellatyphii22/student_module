const BASE_URL = "http://127.0.0.1:8000";

/* ================= AUTH HEADER ================= */

function getHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
    };
}

/* ================= LOAD STUDENTS ================= */

async function loadStudents() {
    try {
        const res = await fetch(`${BASE_URL}/students/`, {
            headers: getHeaders()
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Failed to fetch students");
        }

        const data = await res.json();

        let container = document.getElementById("list");
        container.innerHTML = "";

        data.forEach(s => {
            container.innerHTML += `
                <div class="student-card">
                    <p><b>ID:</b> ${s.Student_ID}</p>
                    <p><b>Name:</b> ${s.FirstName} ${s.LastName}</p>
                    <p><b>Email:</b> ${s.Email}</p>

                    <button onclick="deleteStudent(${s.Student_ID})">Delete</button>
                    <button onclick="updateStudent(${s.Student_ID})">Update</button>
                </div>
            `;
        });

    } catch (err) {
        document.getElementById("list").innerHTML =
            `<p style="color:red;">${err.message}</p>`;
    }
}

/* ================= ADD STUDENT ================= */

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

    try {
        const res = await fetch(`${BASE_URL}/students/`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify(student)
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail);

        alert("Student Added Successfully");
        loadStudents();

    } catch (err) {
        alert(err.message);
    }
}

/* ================= DELETE ================= */

async function deleteStudent(id) {
    try {
        const res = await fetch(`${BASE_URL}/students/${id}`, {
            method: "DELETE",
            headers: getHeaders()
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }

        alert("Deleted Successfully");
        loadStudents();

    } catch (err) {
        alert(err.message);
    }
}

/* ================= UPDATE ================= */

async function updateStudent(id) {
    const newName = prompt("Enter new First Name:");

    if (!newName) return;

    try {
        const res = await fetch(`${BASE_URL}/students/${id}`, {
            method: "PATCH",
            headers: getHeaders(),
            body: JSON.stringify({
                FirstName: newName
            })
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail);

        alert("Updated Successfully");
        loadStudents();

    } catch (err) {
        alert(err.message);
    }
}

/* ================= AUTO LOAD ================= */

window.onload = function () {
    loadStudents();
};