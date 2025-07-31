import React from "react";
import "./LogAdmin.css";
import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";
import LogTableContent from "../LogTableContent/LogTableContent";

import ReceiptLongOutlinedIcon from '@mui/icons-material/ReceiptLongOutlined';

const LogAdmin = () => {
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
                    <ReceiptLongOutlinedIcon sx={{
                        fontSize: 30,
                        borderRadius: "8px"
                      }}/>
                    <span className="log-table-title">Daily Attendance Log</span>
                </div>
                      <LogTableContent/>
                
            </div>
            <div className="right-attendance-container">
                aggregate analytics and charts here
                
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogAdmin;
