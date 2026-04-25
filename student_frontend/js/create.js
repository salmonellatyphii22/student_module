const API_URL = "http://127.0.0.1:8000";

function addStudent(event) {
    event.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        age: parseInt(document.getElementById("age").value),
        course: document.getElementById("course").value
    };

    fetch(`${API_URL}/students/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Failed to add student");
        }
        return res.json();
    })
    .then(() => {
        alert("✅ Student Created Successfully!");

        // Clear form
        document.getElementById("name").value = "";
        document.getElementById("age").value = "";
        document.getElementById("course").value = "";
    })
    .catch(err => {
        console.error(err);
        alert("❌ Error creating student");
    });
}

function goBack() {
    window.location.href = "index.html";
}