import React from "react";
import "./App.css";

function App() {
  return (
    <div>
      {/* ================= NAVBAR ================= */}
      <nav className="navbar">
        <a href="#" className="navbar-title">🏥 MedCare Dashboard</a>
        <div className="navbar-links">
          <button>Home</button>
          <button>Patients</button>
          <button>Reports</button>
          <button>Settings</button>
        </div>
      </nav>

      {/* ================= WELCOME CARD ================= */}
      <div className="welcome-card">
        <h1>Welcome 👋</h1>
        <p>Have a great shift. Saturday 30 August 2025</p>
      </div>

      {/* ================= STATS GRID ================= */}
      <div className="stats-grid">
        <div className="stat-card">
          <p className="stat-title">Patients Today</p>
          <p className="stat-value">245</p>
          <p className="stat-change stat-up">▲ 8%</p>
        </div>

        <div className="stat-card">
          <p className="stat-title">Appointments</p>
          <p className="stat-value">122</p>
          <p className="stat-change stat-down">▼ 3%</p>
        </div>

        <div className="stat-card">
          <p className="stat-title">Doctors Available</p>
          <p className="stat-value">37</p>
          <p className="stat-change stat-up">▲ 2%</p>
        </div>

        <div className="stat-card">
          <p className="stat-title">Surgeries Scheduled</p>
          <p className="stat-value">14</p>
          <p className="stat-change stat-up">▲ 5%</p>
        </div>
      </div>

      {/* ================= CHART SECTION ================= */}
      <div className="chart-section">
        <h2>Patient Flow - Weekly</h2>
        {/* Replace this placeholder with a chart later */}
        <div style={{
          background: "#0f172a",
          borderRadius: "10px",
          height: "200px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#94a3b8"
        }}>
          📊 Chart goes here
        </div>
      </div>

      {/* ================= PROFILE CARD ================= */}
      <div className="profile-card">
        <img
          src="https://placehold.jp/64x64.png"
          alt="Doctor"
        />
        <div className="profile-details">
          <h3>Dr. Harsh Sharma</h3>
          <p>Cardiologist</p>
          <p>On Duty</p>
        </div>
      </div>
    </div>
  );
}

export default App;
