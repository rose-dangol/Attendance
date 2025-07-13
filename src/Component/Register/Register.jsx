import React, { useEffect, useState } from 'react'
import "./Register.css"
import { useNavigate } from 'react-router-dom'
const Register = () => {
  const navigate = useNavigate();
  const [clicked,Setclicked]=useState(false)
   const [loaded,setLoaded] = useState(0)
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
    setTimeout(() => {
      navigate("/login");
    }, 500);
  }
  return (
    <div className='RegisterContainer'>
      <div className={!loaded?"RegisterLeftInitial":clicked?"RegisterLeftClicked":"RegisterLeft"}>
        <div className="RegisterDatas">
          <h1 className="RegisterHeading-2">Registration</h1>
          <input type="text" className="RegisterUsername" placeholder='Username' />
          <input type="email" className="RegisterEmail" placeholder='Email'/>
          <input type="password" className="RegisterPassword" placeholder='Password'/>
          <button className="RegisterButton">Register</button>
        </div>
      </div>
      <div className={!loaded?"RegisterRightInitial":clicked?"RegisterRightClicked":"RegisterRight"}>
        <div className={!loaded?"RegisterTextsInitial":clicked?"RegisterTextsClicked":"RegisterTexts"}>
          <h1 className="RegisterHeading">Welcome Back!</h1>
          <p className="RegisterBreadcrumb">Alredy have an account?</p>
          <button className="RegisterLoginButton" onClick={(e) => handleClick(e)}>Login</button>
        </div>

      </div>
      
    </div>
  )
}

export default Register
