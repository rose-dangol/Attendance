import React from "react";
import "./LogTableContent.css";
const LogTableContent = () => {
  return (
    <>
      <tr>
        <td>Prashant Shrestha</td>
        <td>Admin</td>
        <td>2024-01-15</td>
        <td>09:30 AM</td>
        <td>
          <span className="status-active">Active</span>
        </td>
      </tr>
      <tr>
        <td>Rose Dangol</td>
        <td>Student</td>
        <td>2024-01-15</td>
        <td>09:00 AM</td>
        <td>
          <span className="status-inactive">Late</span>
        </td>
      </tr>
      <tr>
        <td>Ojashwi Shrestha</td>
        <td>Student</td>
        <td>2024-01-15</td>
        <td>10:00 AM</td>
        <td>
          <span className="status-active">Active</span>
        </td>
      </tr>
      <tr>
        <td>Saya Bogati</td>
        <td>Student</td>
        <td>2024-01-15</td>
        <td>10:30 AM</td>
        <td>
          <span className="status-inactive">Late</span>
        </td>
      </tr>
    </>
  );
};

export default LogTableContent;
