import React, { useState } from "react";
import "./Home.css";
import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";

import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import HowToRegIcon from "@mui/icons-material/HowToReg";
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import LocalActivityIcon from '@mui/icons-material/LocalActivity';

const Home = () => {
  return (
    <div className="home-container">
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
            <div className="stats-box">
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
              <div className="stats-box-number">1234</div>
              <div className="stats-box-title">Total Students</div>
            </div>
            <div className="stats-box">
              <div className="stats-box-icon">
                <HowToRegIcon sx={{
                    fontSize: 40,
                    border: "1px solid black",
                    backgroundColor: "black",
                    color: "white",
                    borderRadius: "8px",
                    padding: "4px",
                  }}/>
              </div>
              <div className="stats-box-number">1234</div>
              <div className="stats-box-title">Present Students</div>
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
              <div className="stats-box-number">1234</div>
              <div className="stats-box-title">Students on Leave</div>
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
              <div className="stats-box-number">1234</div>
              <div className="stats-box-title">Productivity</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
