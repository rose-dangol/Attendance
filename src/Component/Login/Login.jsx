import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [loaded, setLoaded] = useState(false);
  const [clicked, Setclicked] = useState(false);

  const PageLoaded = () => {
    setTimeout(() => {
      setLoaded(true);
    }, 200);
  };
  useEffect(() => {
    PageLoaded();
  }, []);

  const handleClick = (e) => {
    Setclicked(true);
    setTimeout(() => {
      navigate("/register");
    }, 500);
  };

  const handleSubmit = async (e) => {
    try {
      e.preventDefault();
      console.log("Submitting...");
      const formData = new FormData(e.target);
      const loginData = {
        username: formData.get("username"),
        password: formData.get("password"),
      };
      const res = await axios.post(
        "http://localhost:5000/api/auth/login",
        loginData
      );
      const userData = JSON.stringify(res.data); // now it's initialized
      await localStorage.setItem("userData", userData);
      // console.log(userData);

      // console.log(res.data);
      navigate("/");
    } catch (error) {
      console.log(error.message);
    }
  };
  return (
    <div className="LoginContainer">
      <div
        className={
          !loaded
            ? "LoginRightInitial"
            : clicked
            ? "LoginRightClicked"
            : "LoginRight"
        }
      >
        <div
          className={
            !loaded
              ? "LoginTextsInitial"
              : clicked
              ? "LoginTextsClicked"
              : "LoginTexts"
          }
        >
          <h1 className="LoginHeading">Hello, Welcome!</h1>
          <p className="LoginBreadcrumb"> Don't have an account?</p>

          <button
            className="LoginRegisterButton"
            onClick={(e) => handleClick(e)}
          >
            Register
          </button>
        </div>
      </div>
      <div
        className={
          !loaded
            ? "LoginLeftInitial"
            : clicked
            ? "LoginLeftClicked"
            : "LoginLeft"
        }
      >
        <form className="LoginDatas" onSubmit={(e) => handleSubmit(e)}>
          <h1 className="LoginHeading-2">Login</h1>
          <input
            type="text"
            placeholder="Username"
            name="username"
            className="LoginUsername"
            required
          />
          <input
            type="password"
            name="password"
            className="LoginPassword"
            placeholder="Password"
            required
          />
          <Link to="" className="LoginForgotPassword">
            Forgot Password?
          </Link>
          <button className="LoginButton">Login</button>
        </form>
        {/* <Link to="" className="LoginButton">Login</Link> */}
      </div>
    </div>
  );
};
export default Login;
