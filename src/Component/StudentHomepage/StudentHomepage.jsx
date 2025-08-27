import React, { useEffect, useState } from "react";
import "./StudentHomepage.css";
import Header from "./Header";
import StatusCard from "./StatusCard";
import RecentAttendance from "./RecentAttendance";
import Notifications from "./Notifications";

import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";


const StudentHomepage = () => {
  return (
    <div className="dashboard">
      <Header />

      <div className="cards-row">
        <StatusCard
          title="Today's Status"
          subtitle="Present"
          extra="Checked in at 9:15 AM"
          tag="On Time"
        />
        <StatusCard
          title="This Week"
          subtitle="4/5 Days"
          extra="80% attendance rate"
          tag="Alert"
        />
        <StatusCard
          title="This Month"
          subtitle="18/22 Days"
          extra="Above average performance"
          tag="On Time"
        />
      </div>

      <div className="bottom-row">
        <RecentAttendance />
        <Notifications />
      </div>
    </div>
  )
}

export default StudentHomepage


