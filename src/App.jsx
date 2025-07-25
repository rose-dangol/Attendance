import React from "react";
import { useEffect, useState } from "react";
import Login from "../src/Component/Login/Login";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./Component/Register/Register";
import Home from "./Component/Home/Home";
import AdminDashboard from "./Component/AdminDashboard/AdminDashboard";
import TotalStudents from "./Component/TotalStudents/TotalStudents";
import TopNavbar from "./Component/TopNavbar/TopNavbar";

const App = () => {
  // const [userData, setUserData] = useState(
  //   () => JSON.parse(localStorage.getItem("userData")) || null
  // );

  // useEffect(() => {
  //   const storedUser = localStorage.getItem("userData");
  //   if(storedUser){
  //     setUserData(JSON.parse(storedUser));
  //   }
  // },[]);
  //   let userData;

  //   setTimeout(() => {
  //    userData = JSON.parse(localStorage.getItem("userData"));
  //   console.log(userData);
  // }, 200);

  const userData = JSON.parse(localStorage.getItem("userData"));
  console.log(userData)

  return (
    <div>
      <Routes>
        {userData ? (
          <Route path="/" element={<Home />} />
        ) : (
          <Route path="/" element={<Login />} />
        )}
        {/* <Route path="/" element={<Home />} /> */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/AdminDashboard" element={<AdminDashboard />} />
        <Route path="/TotalStudents" element={<TotalStudents />} />
        <Route path="/TopNavbar" element={<TopNavbar/>}/>
      </Routes>
    </div>
  );
};

export default App;
