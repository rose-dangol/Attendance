import React from "react";
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import Login from "../src/Component/Login/Login";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./Component/Register/Register";
import Home from "./Component/Home/Home";
import AdminDashboard from "./Component/AdminDashboard/AdminDashboard";
import TotalStudents from "./Component/TotalStudents/TotalStudents";
import TopNavbar from "./Component/TopNavbar/TopNavbar";
import TakeAttendance from "./Component/TakeAttendance/TakeAttendance";
import CameraTest from "./Component/CameraTest/CameraTest";
import LogAdmin from "./Component/LogAdmin/LogAdmin";
import LogTableContent from "./Component/LogTableContent/LogTableContent";
import AddNewUser from "./Component/AddNewUser/AddNewUser";
import StudentHomepage from "./Component/StudentHomepage/StudentHomepage";
import TeacherDashboard from "./Component/TeacherDashboard/TeacherDashboard";
import AllUser from "./Component/AllUser/AllUser";
import PresentStudent from "./Component/AllUser/PresentStudent";
import LeaveStudent from "./Component/AllUser/LeaveStudent";
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
  

  return (
    <div>
      <Routes>
        {userData ? (
          <Route path="/" element={<Home />} />
        ) : (
          <Route path="/" element={<Login />} />
        )}
        {userData ? (
          <Route path="/" element={<StudentHomepage />} />
        ) : (
          <Route path="/" element={<Login />} />
        )}
        
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/AdminDashboard" element={<AdminDashboard />} />
        <Route path="/TotalStudents" element={<TotalStudents />} />
        <Route path="/TopNavbar" element={<TopNavbar/>}/>
        <Route path="/TakeAttendance" element={<TakeAttendance/>}/>
        <Route path="/CameraTest" element={<CameraTest/>}/>
        <Route path="/LogAdmin" element={<LogAdmin/>} />
        <Route path="/LogTableContent" element={<LogTableContent/>}/>
        <Route path="/AddNewUser" element={<AddNewUser/>}/>
        <Route path="/StudentHomepage" element={<StudentHomepage/>}/>
        <Route path="/TeacherDashboard" element={<TeacherDashboard/>}/>
        <Route path="/AllUSer" element={<AllUser/>}/>
        <Route path="/PresentUser" element={<PresentStudent/>}/>
        <Route path="/LeaveUser" element={<LeaveStudent/>}/>
      </Routes>
    </div>
  );
};

export default App;
