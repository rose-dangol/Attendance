import React from "react";
import Login from "../src/Component/Login/Login";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./Component/Register/Register";
import Home from "./Component/Home/Home";
import Contact from "./Component/contact/contact";
import AdminDashboard from "./Component/AdminDashboard/AdminDashboard";

const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/AdminDashboard" element={<AdminDashboard />} />
      </Routes>
    </div>
  );
};

export default App;
