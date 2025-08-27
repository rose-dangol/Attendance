import React from "react";

const RecentAttendance = () => {
  const data = [
    { date: "Jan 22", in: "09:15 AM", out: "06:30 PM", hrs: "9h 15m", status: "Present" },
    { date: "Jan 21", in: "09:05 AM", out: "06:15 PM", hrs: "9h 10m", status: "Present" },
    { date: "Jan 20", in: "09:45 AM", out: "06:45 PM", hrs: "9h 00m", status: "Late" },
  ];

  return (
    <div className="recent-attendance">
      <h3>Recent Attendance <span>(Last 5 working days)</span></h3>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Check In</th>
            <th>Check Out</th>
            <th>Working Hours</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{row.date}</td>
              <td>{row.in}</td>
              <td>{row.out}</td>
              <td>{row.hrs}</td>
              <td>
                <span className={`status ${row.status === "Present" ? "present" : "late"}`}>
                  {row.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecentAttendance;
