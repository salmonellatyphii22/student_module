window.onload = function () {
    fetch("http://localhost:3000/students")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("list");

            data.forEach(s => {
                const div = document.createElement("div");
                div.innerHTML = `${s._id} - ${s.name} (${s.age})`;
                list.appendChild(div);
            });
        });
};

function goBack() {
    window.location.href = "index.html";
}