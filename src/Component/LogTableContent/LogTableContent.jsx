import React from "react";
import "./LogTableContent.css";
const LogTableContent = () => {
  return (
    <div>
      <div className="log-table">
        <div className="table-username">
          <span className="table-username-text">User</span>
        </div>
        <div className="table-role">
          <span className="table-role-text">Roles</span>
        </div>
        <div className="table-date">
          <span className="table-date-text">Date</span>
        </div>
        <div className="table-checkin">
          <span className="table-checkin-text">Check-In</span>
        </div>
        <div className="table-status">
          <span className="table-status-text">Status</span>
        </div>
      </div>

      {/* <div className="log-content-heading">
        <div className="heading-username">User</div>
        <div className="heading-roles">Roles</div>
        <div className="heading-date">Date</div>
        <div className="heading-checkin">Check-In</div>
        <div className="heading-status">Status</div>
      </div>
        <div className="log-table-content">
            <div className="log-entry">
                <div className="entry-username">Prashant Shrestha</div>
                <div className="entry-roles">Admin</div>
                <div className="entry-date">2023-10-01</div>
                <div className="entry-checkin">09:00 AM</div>
                <div className="entry-status">Present</div>
            </div>

<div className="log-entry">
                <div className="entry-username">Rose Dangol</div>
                <div className="entry-roles">Admin</div>
                <div className="entry-date">2023-10-01</div>
                <div className="entry-checkin">09:00 AM</div>
                <div className="entry-status">Present</div>
            </div>


            <div className="log-entry">
                <div className="entry-username">Jane</div>
                <div className="entry-roles">Student</div>
                <div className="entry-date">2023-10-31</div>
                <div className="entry-checkin">12:00 AM</div>
                <div className="entry-status">Present</div>
            </div>

        </div> */}
    </div>
  );
};

export default LogTableContent;
