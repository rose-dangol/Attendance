import React, { useState } from "react";
import "./AdminDashboard.css";
import Dashboard from "../Dashboard/Dashboard";
import axios from "axios";
const handleTakeAttendance = async () => {
  try {
    const res = await axios.get("http://localhost:5000/run-attendance");
    console.log(res.data.message);
    alert(res.data.message);
  } catch (err) {
    console.error("Error running attendance:", err);
    alert("Failed to run attendance.");
  }
};
const AdminDashboard = () => {
  return (
    <div>
      <div className="AdminDashboard-wrapper">
        <Dashboard />
        <div className="AdminDashboard-container">
          <h1 className="AdminDashboard-title">Admin Dashboard</h1>
          <div className="AdminDashboard-body">
            <div className="body-center">
              <div className="body-welcome">
                <p>
                  Hey there, Admin! 👋 Welcome aboard Attendify — your smart and
                  friendly Face Recognition Attendance System! We're here to
                  make attendance tracking easier, faster, and just a little
                  more fun, all with the magic of face recognition. Let’s get
                  started and make managing attendance a breeze!
                </p>
              </div>
              <div className="operations">
                <div className="operation-box" onClick={handleTakeAttendance}
    style={{ cursor: "pointer" }}>
                  <div className="operation-image">
                    <img
                      src={"/images/1.png"}
                      alt="Logo"
                      style={{
                        height: "100%",
                        width: "100%",
                        objectFit: "cover", // Apply her
                        // borderRadius: "50%", // Make image circular too
                      }}
                    />
                  </div>
                  <div className="operation-title">Take Attendance</div>
                </div>
                <div className="operation-box">
                  <div className="operation-image">
                    {" "}
                    <img
                      src={"/images/2.png"}
                      alt="Logo"
                      style={{
                        height: "100%",
                        width: "100%",
                        objectFit: "cover", // Apply here
                        // borderRadius: "50%", // Make image circular too
                      }}
                    />
                  </div>
                  <div className="operation-title">View Attendance Log</div>
                </div>
                <div className="operation-box">
                  <div className="operation-image">
                    <img
                      src={"/images/3.png"}
                      alt="Logo"
                      style={{
                        height: "100%",
                        width: "100%",
                        objectFit: "cover", // Apply here
                        // borderRadius: "50%", // Make image circular too
                      }}
                    />
                  </div>
                  <div className="operation-title">Add New User</div>
                </div>
                <div className="operation-box">
                  <div className="operation-image">
                    <img
                      src={"/images/4.png"}
                      alt="Logo"
                      style={{
                        height: "100%",
                        width: "100%",
                        objectFit: "cover", // Apply here
                        // borderRadius: "50%", // Make image circular too
                      }}
                    />
                  </div>
                  <div className="operation-title">Assign Courses</div>
                </div>
              </div>
            </div>
            <div className="students-list">
              <h2>Number of Students</h2>
              <h3>400</h3>
            </div>
          </div>
        </div>
      </div>

      {/* <div className="AdminDashboard-wrapper">
  <Dashboard />
  <div className="AdminDashboard-container">
    <h1 className="AdminDashboard-title">Admin Dashboard</h1>
    <div className="AdminDashboard-body">
      <div className="body-center">
        <div className="body-welcome">
          <p>
            Hey there, Admin! 👋 Welcome aboard Attendify — your smart and
            friendly Face Recognition Attendance System! We're here to make
            attendance tracking easier, faster, and just a little more fun,
            all with the magic of face recognition. Let’s get started and
            make managing attendance a breeze!
          </p>
        </div>
        <div className="students-list">
          <h2>Number of Students</h2>
          <h3>400</h3>
        </div>
      </div>
      <div className="operations">
        <div className="operation-box">
          <div className="operation-image">
            <img
              src={"/images/1.png"}
              alt="Take Attendance"
              style={{ height: "100%", width: "100%", objectFit:"cover" }}
            />
          </div>
          <div className="operation-title">Take Attendance</div>
        </div>
        <div className="operation-box">
          <div className="operation-image">
            <img
              src={"/images/2.png"}
              alt="View Attendance Log"
              style={{ height: "100%", width: "100%", objectFit:"cover" }}
            />
          </div>
          <div className="operation-title">View Attendance Log</div>
        </div>
        <div className="operation-box">
          <div className="operation-image">
            <img
              src={"/images/3.png"}
              alt="Add New User"
              style={{ height: "100%", width: "100%", objectFit:"cover" }}
            />
          </div>
          <div className="operation-title">Add New User</div>
        </div>
        <div className="operation-box">
          <div className="operation-image">
            <img
              src={"/images/4.png"}
              alt="Assign Courses"
              style={{ height: "100%", width: "100%", objectFit:"cover" }}
            />
          </div>
          <div className="operation-title">Assign Courses</div>
        </div>
      </div>
      <div className="empty-space">
        <p>hhhddhfi</p>
      </div>
    </div>
  </div>
</div> */}
    </div>
  );
};

export default AdminDashboard;
