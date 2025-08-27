import React, { useEffect, useState } from "react";
import "./AddNewUser.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import Dashboard from "../Dashboard/Dashboard";
import TopNavbar from "../TopNavbar/TopNavbar";

import PersonAddAltIcon from "@mui/icons-material/PersonAddAlt";
import PersonPinCircleOutlinedIcon from "@mui/icons-material/PersonPinCircleOutlined";
import BadgeOutlinedIcon from "@mui/icons-material/BadgeOutlined";
import EmailOutlinedIcon from "@mui/icons-material/EmailOutlined";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import ClearOutlinedIcon from "@mui/icons-material/ClearOutlined";
import MiscellaneousServicesOutlinedIcon from '@mui/icons-material/MiscellaneousServicesOutlined';

const AddNewUser = () => {
  const handleSubmit = async (e) => {
    try{
      e.preventDefault();
      const formData = new FormData(e.target);
      const userData = {
          fullName: formData.get("fullName"),
          username: formData.get("username"),
          email: formData.get("email"),
          password: formData.get("password"),
          role: formData.get("role"),
        };
      const response = await axios.post("http://localhost:5000/api/auth/addNewUser", userData);
      alert("User added successfully!");
      console.log(response.data);
      e.target.reset(); // Resets the form

    }catch (error) {
      console.error("Error adding new user:", error);
      alert("Failed to add new user. Please try again.");
    }
  };
  const handleClear = (e) => {
    e.preventDefault();
    document.querySelectorAll(".add-new-user-input").forEach((input) => {
      input.value = "";
    });
    document.querySelector(".add-new-user-input[name='role']").value = "";
  };
  return (
    <div>
      <div className="add-new-user-container">
        <Dashboard />
        <div className="add-new-user-main-container">
          <TopNavbar />
          <div className="add-new-user-center">
            <div className="add-new-user-pageTitle">
              <span className="add-new-user-icon">
                <PersonAddAltIcon
                  sx={{
                    fontSize: 38,
                    backgroundColor: "#D4D2DA",
                    color: "black",
                    borderRadius: "10px",
                    padding: "5px",
                  }}
                />
              </span>
              <div className="add-new-user-titleGroup">
                <span className="add-new-user-title">User Registration</span>
                <span className="add-new-user-subtitle">
                  Fill in the details to add a new user.
                </span>
              </div>
            </div>
            <div className="add-new-user-form">
              <div className="add-new-user-formHeading">
                <span className="add-new-user-formTitle">Create New User</span>
                <span className="add-new-user-formSubtitle">
                  Fill in the details below to register a user in the system
                </span>
              </div>
              <form className="add-new-user-formInputs" onSubmit={(e) => handleSubmit(e)}>
                <div className="form-row">
                  <div className="form-inputLabel half-width">
                    <div className="label-icon">
                      <PersonPinCircleOutlinedIcon />
                      <label className="add-new-user-label">Name</label>
                    </div>
                    <input
                      type="text"
                      placeholder="Full Name"
                      className="add-new-user-input name-input"
                      name="fullName"
                      required
                    />
                  </div>
                  <div className="form-inputLabel half-width">
                    <div className="label-icon">
                      <BadgeOutlinedIcon />
                      <label className="add-new-user-label">Username</label>
                    </div>
                    <input
                      type="text"
                      placeholder="Username"
                      className="add-new-user-input username-input"
                      name="username"
                      required
                    />
                  </div>
                </div>

                <div className="form-inputLabel">
                  <div className="label-icon">
                    <EmailOutlinedIcon />
                    <label className="add-new-user-label">Email</label>
                  </div>
                  <input
                    type="email"
                    placeholder="Email"
                    className="add-new-user-input email-input"
                    name="email"
                    required
                  />
                </div>

                <div className="form-inputLabel">
                  <div className="label-icon">
                    <LockOutlinedIcon />
                    <label className="add-new-user-label">Password</label>
                  </div>
                  <input
                    type="password"
                    placeholder="Password"
                    className="add-new-user-input password-input"
                    name="password"
                    required
                  />
                </div>
                <div className="form-inputLabel">
                  <div className="label-icon">
                    <MiscellaneousServicesOutlinedIcon />
                    <label className="add-new-user-label">Role</label>
                  </div>
                  <select
                    name="role"
                    className="add-new-user-input role-input"
                    required
                  >
                    <option value="" disabled selected>Select Role</option>
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                  </select>
                </div>

                <div className="form-buttons">
                  <button className="add-new-user-submitButton">
                    <PersonAddAltIcon />
                    <span>Create User</span>
                  </button>
                  <button className="add-new-user-cancelButton" onClick={(e) => handleClear(e)}>
                    <ClearOutlinedIcon />
                    Clear Form
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddNewUser;
