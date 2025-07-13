import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [loaded,setLoaded] = useState(false)
  const [clicked,Setclicked]=useState(false)
  
  const PageLoaded = () =>{
    setTimeout(()=>{
      setLoaded(true)
    },200)
  }
  useEffect(()=>{
    PageLoaded();
  },[])
  

  const handleClick = (e) =>{
    Setclicked(true)
    setTimeout(()=>{
      navigate('/register')
    },500);
  }
  return (
    <div className="LoginContainer" >
      <div className={!loaded?"LoginRightInitial":clicked?"LoginRightClicked":"LoginRight"}>
        <div className={!loaded?"LoginTextsInitial":clicked?"LoginTextsClicked":"LoginTexts"}>
          <h1 className="LoginHeading">Hello, Welcome!</h1>
          <p className="LoginBreadcrumb"> Don't have an account?</p>
          
          <button className="LoginRegisterButton" onClick={(e)=>handleClick(e)}>Register</button>
    
        </div>
      </div>
      <div className={!loaded?"LoginLeftInitial":clicked?"LoginLeftClicked":"LoginLeft"}>
        <div className="LoginDatas">
          <h1 className="LoginHeading-2">Login</h1>
          <input type="text" placeholder="Username" className="LoginUsername" />
          <input
            type="password"
            className="LoginPassword"
            placeholder="Password"
          />
          <Link to="" className="LoginForgotPassword">Forgot Password?</Link>
          <Link to="/" className="LoginButton">Login</Link>
          {/* <button className="LoginButton">Login</button> */}
        </div>
      </div>
    </div>
  );
};
export default Login;
