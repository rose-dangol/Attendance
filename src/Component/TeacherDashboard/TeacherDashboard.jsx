import React, { useEffect, useState } from "react";
import "./TeacherDashboard.css";

function TeacherDashboard() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const stats = {
    totalStudents: 30,
    present: 26,
    absent: 4,
  };

  const attendanceToday = [
    { name: "Alice", status: "Present" },
    { name: "Bob", status: "Present" },
    { name: "Charlie", status: "Absent" },
    { name: "Daisy", status: "Present" },
  ];

  const notifications = [
    "Staff meeting tomorrow at 10 AM.",
    "Submit attendance report by Friday.",
  ];

  return (
    <div className="Teacherdashboard-container">
      {/* Welcome */}
      <div className="welcome-card">
        <h2>Welcome, Admin/Teacher</h2>
        <p>
          {time.toLocaleDateString("en-US", {
            weekday: "long",
            month: "long",
            day: "numeric",
            year: "numeric",
          })}{" "}
          {time.toLocaleTimeString()}
        </p>
      </div>

      {/* Stats */}
      <div className="stats-container">
        <div className="stat-card">Total Students: {stats.totalStudents}</div>
        <div className="stat-card">Present Today: {stats.present}</div>
        <div className="stat-card">Absent Today: {stats.absent}</div>
      </div>

      {/* Attendance Table */}
      <div className="attendance-card">
        <h3>Today's Attendance</h3>
        <table>
          <thead>
            <tr>
              <th>Student Name</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {attendanceToday.map((s, i) => (
              <tr key={i}>
                <td>{s.name}</td>
                <td className={s.status.toLowerCase()}>{s.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Notifications */}
      <div className="notifications-card">
        <h3>Notifications</h3>
        <ul>
          {notifications.map((note, i) => (
            <li key={i}>{note}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default TeacherDashboard;
