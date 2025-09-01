import React, { useEffect, useState } from "react";
import "./Home.css";
import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";

import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import HowToRegIcon from "@mui/icons-material/HowToReg";
import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import LocalActivityIcon from "@mui/icons-material/LocalActivity";

import StudentHomepage from "../StudentHomepage/StudentHomepage";
import { Navigate, useNavigate } from "react-router-dom";

const Home = () => {
  const [studentCount, setStudentCount] = useState(0);
  const [presentCount, setPresentCount] = useState(0);
  const navigate = useNavigate();
  useEffect(() => {
    fetch("http://localhost:5000/api/auth/getAll")
      .then((response) => response.json())
      .then((data) => {
        setStudentCount(data.length);
        const present = data.filter((s) => s.status === "present").length;
        setPresentCount(present);
      })
      .catch((error) => console.error("Error fetching student count:", error));
  }, []);
  const userData = JSON.parse(localStorage.getItem("userData"));
  console.log(userData?.role);
  return (<>
    {userData?.role==="admin"||userData?.role==="teacher"?
    (<div className="home-container">
      <Dashboard />
      <div className="main-content">
        <TopNavbar />
        <div className="home-center-content">
          <div className="center-heading">
            <h2>Dashboard Overview</h2>
            <p>
              Welcome Back! Here's what's happening today with your schedule.
            </p>
          </div>
          {/* 192 x140 */}
          <div className="center-stats">
            <div className="stats-box" >
              <div className="stats-box-icon">
                <PeopleAltIcon
                  sx={{
                    fontSize: 40,
                    border: "1px solid black",
                    backgroundColor: "black",
                    color: "white",
                    borderRadius: "8px",
                    padding: "4px",
                  }}
                />
              </div>
              <div className="stats-box-number">{studentCount}</div>
              <div className="stats-box-title" onClick={()=>navigate("/AllUser")}>Total Students</div>
            </div>
            <div className="stats-box">
              <div className="stats-box-icon">
                <HowToRegIcon
                  sx={{
                    fontSize: 40,
                    border: "1px solid black",
                    backgroundColor: "black",
                    color: "white",
                    borderRadius: "8px",
                    padding: "4px",
                  }}
                />
              </div>
              <div className="stats-box-number">{presentCount}</div>
              <div className="stats-box-title" onClick={()=>navigate("/PresentUser")}>Present Students</div>
            </div>
            <div className="stats-box">
              <div className="stats-box-icon">
                <LocalActivityIcon
                  sx={{
                    fontSize: 40,
                    border: "1px solid black",
                    backgroundColor: "black",
                    color: "white",
                    borderRadius: "8px",
                    padding: "4px",
                  }}
                />
              </div>
              <div className="stats-box-number">5</div>
              <div className="stats-box-title" onClick={()=>navigate("/LeaveUser")}>Students on Leave</div>
            </div>
            <div className="stats-box">
              <div className="stats-box-icon">
                <AutoGraphIcon
                  sx={{
                    fontSize: 40,
                    border: "1px solid black",
                    backgroundColor: "black",
                    color: "white",
                    borderRadius: "8px",
                    padding: "4px",
                  }}
                />
              </div>
              <div className="stats-box-number">88%</div>
              <div className="stats-box-title">Productivity</div>
            </div>
          </div>
          <div className="center-bargraph"></div>
        </div>
      </div>
    </div>):<StudentHomepage/>}
    </>
  );
};

export default Home;
