import React from "react";

const Notifications = () => {
  const notes = [
    { type: "warning", title: "Late Check-in Alert", desc: "You checked in 15 minutes late yesterday. Please ensure timely attendance.", time: "2 hours ago" },
    // { type: "info", title: "Upcoming Holiday", desc: "Republic Day holiday on January 26th. Office will be closed.", time: "1 day ago" }
  ];

  return (
    <div className="notifications">
      <h3>Notifications <span>3 new</span></h3>
      {notes.map((n, i) => (
        <div key={i} className={`note ${n.type}`}>
          <h4>{n.title}</h4>
          <p>{n.desc}</p>
          <span className="time">{n.time}</span>
        </div>
      ))}
    </div>
  );
};

export default Notifications;
