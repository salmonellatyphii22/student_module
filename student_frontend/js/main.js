const BASE_URL = "http://127.0.0.1:8000";

/* ================= AUTH HEADER ================= */

function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + sessionStorage.getItem("token")
    };
}

/* ================= TOKEN CHECK ================= */

function checkAuth() {
    if (!sessionStorage.getItem("token")) {
        window.location.href = "login.html";
    }
}

/* ================= SIDEBAR ================= */

function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("active");
    document.getElementById("content").classList.toggle("shift");
}

/* ================= NAVIGATION ================= */

function goToPage(page) {
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");
    window.location.href = page;
}

/* ================= LOAD PAGE ================= */

function loadPage(page) {
    const content = document.getElementById("content");

    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("content").classList.remove("shift");

    if (page === "exam") {
        content.innerHTML = `
            <h1>📅 Exams</h1>
            <div id="examList">Loading...</div>
        `;
        loadExams();
    }

    else if (page === "report") {
        content.innerHTML = `
            <h1>🎓 Your Report Card</h1>
            <div id="reportResult">Loading...</div>
        `;
        loadStudentReport();
    }
}

/* ================= REPORT ================= */

function loadStudentReport() {
    fetch(`${BASE_URL}/result/`, {
        method: "GET",
        headers: getAuthHeaders()
    })
    .then(res => {
        if (res.status === 401) throw new Error("Session expired");
        return res.json();
    })
    .then(data => {
        let html = "";

        if (!data.length) {
            html = "<p>No results available</p>";
        } else {
            html = `<div class="card"><h2>📊 Report Card</h2><hr>`;

            data.forEach(r => {
                html += `
                    <p><b>Course:</b> ${r.Course_Name}</p>
                    <p>Marks: ${r.Marks_Obtained}</p>
                    <p>Grade: ${r.Grade}</p>
                    <p>Status: ${r.Result_Status}</p>
                    <hr>
                `;
            });

            html += `</div>`;
        }

        document.getElementById("reportResult").innerHTML = html;
    })
    .catch(err => {
        document.getElementById("reportResult").innerHTML =
            `<p style="color:red;">${err.message}</p>`;
    });
}

/* ================= EXAMS ================= */

function loadExams() {
    fetch(`${BASE_URL}/exam/`, {
        headers: getAuthHeaders()
    })
    .then(res => res.json())
    .then(data => {
        let html = "";
        data.forEach(e => {
            html += `<div class="card">${e.Exam_Type} - ${e.Exam_Date}</div>`;
        });
        document.getElementById("examList").innerHTML = html;
    });
}

/* ================= HOME ================= */

function loadHome() {
    const content = document.getElementById("content");

    content.innerHTML = `
        <div class="hero">
            <h1>🎓 Student Academy</h1>
            <p>Empowering Education Through Smart Management 🚀</p>
        </div>

        <div class="banner">
            <img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644" />
        </div>

        <!-- Animated Stats -->
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

    setTimeout(animateCounters, 200);
}

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

/* ================= ACTIVE MENU ================= */

function setActive(el) {
    document.querySelectorAll(".sidebar li").forEach(li => li.classList.remove("active"));
    el.classList.add("active");
}

/* ================= LOGOUT ================= */

function logout() {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("role");
    window.location.href = "login.html";
}

/* ================= THEME ================= */

function toggleTheme() {
    document.body.classList.toggle("dark-mode");

    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

/* ================= INIT ================= */

window.onload = function () {
    checkAuth();
    loadHome();

    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }
};