import React from "react";
import { useEffect, useState } from "react";
import Login from "../src/Component/Login/Login";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./Component/Register/Register";
import Home from "./Component/Home/Home";
import Contact from "./Component/contact/contact";
import AdminDashboard from "./Component/AdminDashboard/AdminDashboard";
import TotalStudents from "./Component/TotalStudents/TotalStudents";

const App = () => {
  const [userData, setUserData] = useState(
    () => JSON.parse(localStorage.getItem("userData")) || null
  );

  useEffect(() => {
    const storedUser = localStorage.getItem("userData");
    if(storedUser){
      setUserData(JSON.parse(storedUser));
    }
  },[]);
  // const userDatas = JSON.parse(localStorage.getItem("userData"));
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
        <Route path="/contact" element={<Contact />} />
        <Route path="/AdminDashboard" element={<AdminDashboard />} />
        <Route path="/TotalStudents" element={<TotalStudents />}/>
      </Routes>
    </div>
  );
};

export default App;

