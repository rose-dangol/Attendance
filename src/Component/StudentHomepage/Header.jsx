import React, { useState, useEffect } from "react";

const Header = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);
  const timeString = currentTime.toLocaleTimeString("en-US", {
    hour12: true,
  });
  const dateString = currentTime.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  const userData = JSON.parse(localStorage.getItem("userData"));
  return (
    <div className="header">
      <div className="user-info">
        <img src="/images/userProfile.jpg" alt="profile" className="avatar" />
        <div>
          <h2>Welcome, {userData.fullName}</h2>
          <p>Hope you're having a productive day!</p>
        </div>
      </div>
      <div className="datetime">
        <h3>{timeString}</h3>
        <p>{dateString}</p>
      </div>
    </div>
  );
};

export default Header;
