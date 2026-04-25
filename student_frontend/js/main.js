/* ================= SIDEBAR TOGGLE ================= */

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");

    sidebar.classList.toggle("active");
    content.classList.toggle("shift");
}

/* ================= MODULE LOAD ================= */

function loadModule(module) {
    console.log("Clicked:", module); // debug line

    // close sidebar
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");

    if (module === "student") {
        window.location.href = "./student.html";
    } 
    else if (module === "department") {
        window.location.href = "./department.html";
    } 
    else if (module === "faculty") {
        window.location.href = "./faculty.html";
    } 
    else if (module === "course") {
        window.location.href = "./courses.html";
    }
}

/* ================= PAGE NAVIGATION ================= */

function goToPage(page) {
    console.log("Navigating to:", page);

    // close sidebar before navigating
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");

    // redirect
    window.location.href = page;
}

/* ================= EXAM + REPORT ================= */

function loadPage(page) {
    const content = document.getElementById("content");

    // auto close sidebar
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");

    if (page === "exam") {
        content.innerHTML = `
            <h1>📅 Exams</h1>
            <div class="card">Math - 20 April</div>
            <div class="card">Physics - 25 April</div>
        `;
    }

    else if (page === "report") {
        content.innerHTML = `
            <h1>🎓 View Report Card</h1>

            <input id="studentId" placeholder="Enter Student ID">
            <input id="studentName" placeholder="Enter Student Name">

            <button onclick="getReport()">View Report</button>

            <div id="reportResult"></div>
        `;
    }
}

/* ================= REPORT ================= */

function getReport() {
    const id = document.getElementById("studentId").value;
    const name = document.getElementById("studentName").value;

    if (!id || !name) {
        alert("Please enter both ID and Name");
        return;
    }

    fetch(`http://localhost:3000/students/${id}`)
    .then(res => res.json())
    .then(data => {

        if (!data || data.name.toLowerCase() !== name.toLowerCase()) {
            alert("Invalid Student Details!");
            return;
        }

        const math = data.math || 0;
        const physics = data.physics || 0;
        const chemistry = data.chemistry || 0;

        const total = math + physics + chemistry;
        const percentage = (total / 3).toFixed(2);

        let grade = "F";
        if (percentage >= 90) grade = "A+";
        else if (percentage >= 75) grade = "A";
        else if (percentage >= 60) grade = "B";
        else if (percentage >= 50) grade = "C";

        document.getElementById("reportResult").innerHTML = `
            <div class="card">
                <h2>📊 Report Card</h2>

                <p><b>Name:</b> ${data.name}</p>
                <p><b>ID:</b> ${data._id}</p>

                <hr>

                <p>Math: ${math}</p>
                <p>Physics: ${physics}</p>
                <p>Chemistry: ${chemistry}</p>

                <hr>

                <p><b>Total:</b> ${total}</p>
                <p><b>Percentage:</b> ${percentage}%</p>
                <p><b>Grade:</b> ${grade}</p>
            </div>
        `;
    })
    .catch(() => alert("Error fetching report"));
}

function loadHome() {
    const content = document.getElementById("content");

    // close sidebar after click
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");

    content.innerHTML = `
        <div class="hero">
            <h1>🎓 Student Academy</h1>
            <p>Empowering Education Through Smart Management 🚀</p>
        </div>

        <div class="banner">
            <img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644" />
        </div>

        <!-- 🔥 Animated Stats -->
        <div class="stats">
            <div class="card">
                🎯 <span class="count" data-target="100">0</span>+ Students Enrolled
            </div>

            <div class="card">
                📘 <span class="count" data-target="20">0</span>+ Courses Available
            </div>

            <div class="card">
                🏆 <span class="count" data-target="95">0</span>% Success Rate
            </div>
        </div>

        <h2>✨ Why Choose Our Academy?</h2>

        <div class="features">
            <div class="card">
                <h3>📊 Smart Tracking</h3>
                <p>Track performance easily and monitor progress in real-time.</p>
            </div>

            <div class="card">
                <h3>⚡ Fast Management</h3>
                <p>Manage students, courses, and faculty efficiently.</p>
            </div>

            <div class="card">
                <h3>🔐 Secure System</h3>
                <p>Your data is protected with a reliable system.</p>
            </div>

            <div class="card">
                <h3>📈 Growth Insights</h3>
                <p>Analyze academic performance with smart insights.</p>
            </div>
        </div>

        <div class="quote">
            <p>"Education is the key to success." 🌍</p>
        </div>
    `;

    // 🔥 trigger animation
    setTimeout(animateCounters, 200);
}

function setActive(element) {
    document.querySelectorAll(".sidebar li").forEach(li => {
        li.classList.remove("active");
    });
    element.classList.add("active");
}

// Load home page on initial load
window.onload = loadHome;

function toggleTheme() {
    const body = document.body;
    const btn = document.querySelector(".theme-toggle");

    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {
        btn.innerHTML = "☀️";
        localStorage.setItem("theme", "dark");   // SAVE
    } else {
        btn.innerHTML = "🌙";
        localStorage.setItem("theme", "light");  // SAVE
    }
}

window.onload = function () {
    loadHome();

    const savedTheme = localStorage.getItem("theme");
    const btn = document.querySelector(".theme-toggle");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        btn.innerHTML = "☀️";
    }
};

function animateCounters() {
    const counters = document.querySelectorAll(".count");

    counters.forEach(counter => {
        const target = +counter.getAttribute("data-target");
        let count = 0;

        const update = () => {
            const increment = target / 50;

            if (count < target) {
                count += increment;
                counter.innerText = Math.ceil(count);
                setTimeout(update, 20);
            } else {
                counter.innerText = target;
            }
        };

        update();
    });
}


window.onload = function () {
    loadHome(); // load homepage

    const savedTheme = localStorage.getItem("theme");
    const btn = document.querySelector(".theme-toggle");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        btn.innerHTML = "☀️";
    } else {
        btn.innerHTML = "🌙";
    }
};