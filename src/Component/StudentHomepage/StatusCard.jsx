import React from "react";

const StatusCard = ({ title, subtitle, extra, tag }) => {
  return (
    <div className="status-card">
      <h4>{title}</h4>
      <h2>{subtitle}</h2>
      <p>{extra}</p>
      <span className={`tag ${tag === "On Time" ? "success" : "alert"}`}>
        {tag}
      </span>
    </div>
  );
};

export default StatusCard;
