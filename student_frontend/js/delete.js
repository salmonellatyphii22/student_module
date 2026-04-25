function deleteStudent() {
    const id = document.getElementById("id").value;

    fetch(`http://localhost:3000/students/${id}`, {
        method: "DELETE"
    })
    .then(() => alert("Deleted"))
    .catch(err => console.log(err));
}

function goBack() {
    window.location.href = "index.html";
}