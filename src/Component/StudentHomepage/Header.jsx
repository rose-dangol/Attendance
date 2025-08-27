import React from "react";

const Header = () => {
  return (
    <div className="header">
      <div className="user-info">
        <img
          src="/images/userProfile.jpg"
          alt="profile"
          className="avatar"
        />
        <div>
          <h2>Welcome, Rose Dangol</h2>
          <p>Hope you're having a productive day!</p>
        </div>
      </div>
      <div className="datetime">
        <h3>05:43:31 PM</h3>
        <p>Wednesday, August 27, 2025</p>
      </div>
    </div>
  );
};

export default Header;
