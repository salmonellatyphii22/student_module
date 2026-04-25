function updateStudent() {
    const id = document.getElementById("id").value;

    const data = {
        name: document.getElementById("name").value,
        age: document.getElementById("age").value
    };

    fetch(`http://localhost:3000/students/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(() => alert("Updated"))
    .catch(err => console.log(err));
}

function goBack() {
    window.location.href = "index.html";
}