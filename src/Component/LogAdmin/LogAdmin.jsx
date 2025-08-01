import React from "react";
import "./LogAdmin.css";
import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";
import LogTableContent from "../LogTableContent/LogTableContent";

import ReceiptLongOutlinedIcon from "@mui/icons-material/ReceiptLongOutlined";
import Groups3OutlinedIcon from "@mui/icons-material/Groups3Outlined";
import { BarChart } from "@mui/x-charts/BarChart";

const LogAdmin = () => {
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri"];
  return (
    <div>
      <div className="attendance-log-container">
        <Dashboard />
        <div className="logAdmin-container">
          <TopNavbar />
          <div className="page-title">
            <span className="page-heading">Attendance Log</span>
            <span className="page-subtext">
              View and manage daily attendance logs.
            </span>
          </div>
          <div className="center-content">
            <div className="log-left-container">
              <div className="log-table-heading">
                <ReceiptLongOutlinedIcon
                  sx={{
                    fontSize: 25,
                    borderRadius: "8px",
                    marginRight: "5px",
                  }}
                />
                <span className="log-table-title">Daily Attendance Log</span>
              </div>
              <div className="table-container">
                <table className="user-table">
                  <thead>
                    <tr>
                      <th>User</th>
                      <th>Role</th>
                      <th>Date</th>
                      <th>Check In</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <LogTableContent />
                  </tbody>
                </table>
              </div>
            </div>
            <div className="right-attendance-container">
              <div className="right-container-heading">
                <Groups3OutlinedIcon
                  sx={{
                    fontSize: 30,
                    borderRadius: "8px",
                    marginRight: "5px",
                  }}
                />
                <span>Aggregate Analytics</span>
              </div>
              <div className="right-container-bargraphs">
                <BarChart
                  xAxis={[{ scaleType: "band", data: days }]}
                  series={[
                    {
                      data: [30, 25, 23, 28, 22, 27],
                      label: "Present",
                      color: "#4caf50",
                    },
                    {
                      data: [3, 5, 7, 2, 8, 3],
                      label: "Absent",
                      color: "#f44336",
                    },
                  ]}
                  width={600}
                  height={400}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogAdmin;
