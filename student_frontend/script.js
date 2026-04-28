const BASE_URL = "http://127.0.0.1:8000";

// ✅ LOAD STUDENTS
async function loadStudents() {
    try {
        const res = await fetch(`${BASE_URL}/students/`);

        if (!res.ok) {
            console.error("GET ERROR:", res.status);
            return;
        }

        const data = await res.json();
        console.log("Students:", data); // 🔍 debug

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

    } catch (err) {
        console.error("LOAD ERROR:", err);
    }
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

    console.log("Sending:", student); // 🔍 debug

    try {
        const res = await fetch(`${BASE_URL}/students/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        if (!res.ok) {
            const errData = await res.json();
            console.error("POST ERROR:", errData);
            alert("Error adding student. Check console.");
            return;
        }

        loadStudents();

    } catch (err) {
        console.error("ADD ERROR:", err);
    }
}


// ✅ DELETE
async function deleteStudent(id) {
    try {
        const res = await fetch(`${BASE_URL}/students/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            console.error("DELETE ERROR:", res.status);
            return;
        }

        loadStudents();

    } catch (err) {
        console.error("DELETE ERROR:", err);
    }
}


// ✅ UPDATE (PATCH)
async function updateStudent(id) {
    const newName = prompt("Enter new First Name:");

    if (!newName) return;

    try {
        const res = await fetch(`${BASE_URL}/students/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                FirstName: newName
            })
        });

        if (!res.ok) {
            const errData = await res.json();
            console.error("UPDATE ERROR:", errData);
            return;
        }

        loadStudents();

    } catch (err) {
        console.error("UPDATE ERROR:", err);
    }

    async function testAPI() {
    try {
        const res = await fetch("http://127.0.0.1:8000/students/");
        console.log("Status:", res.status);

        const data = await res.json();
        console.log("Data:", data);
    } catch (err) {
        console.error("Error:", err);
    }
}

testAPI();

}