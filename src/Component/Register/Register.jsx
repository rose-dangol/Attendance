import React, { useEffect, useState } from "react";
import "./Register.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();
  const [clicked, setClicked] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const PageLoaded = () => {
    setTimeout(() => {
      setLoaded(true);
    }, 200);
  };

  useEffect(() => {
    PageLoaded();
  }, []);

  const handleClick = (e) => {
    setClicked(true);
    setTimeout(() => {
      navigate("/login");
    }, 500);
  };

  // const [formData, setFormData] = useState({
  //   fullName: "",
  //   username: "",
  //   email: "",
  //   password: "",
  // });

  // const handleChange = (e) => {
  //   setFormData((prev) => ({
  //     ...prev,
  //     [e.target.name]: e.target.value,
  //   }));
  // };

  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   try {
  //     const res = await axios.post("http://localhost:5000/api/auth/register", formData);
  //     alert(res.data.message);
  //     navigate("/login");
  //   } catch (err) {
  //     alert(err.response?.data?.message || "Something went wrong");
  //   }
  // };
  const handleSubmit = async (e) => {
    try {
      e.preventDefault();
      const formData = new FormData(e.target);
      const userData = {
        fullName: formData.get("fullName"),
        username: formData.get("username"),
        email: formData.get("email"),
        password: formData.get("password"),
      };
      const res = await axios.post("http://localhost:5000/api/auth/register", userData);
      console.log(res.data);
      navigate('/login')
    } catch (err) {
      console.log(err.message);
    }
  };

  return (
    <div className="RegisterContainer">
      <div
        className={
          !loaded
            ? "RegisterLeftInitial"
            : clicked
            ? "RegisterLeftClicked"
            : "RegisterLeft"
        }
      >
        <form className="RegisterDatas" onSubmit={(e) => handleSubmit(e)}>
          <h1 className="RegisterHeading-2">Registration</h1>
          <input
            type="text"
            name="fullName"
            className="RegisterUsername"
            placeholder="Full Name"
            required
          />
          <input
            type="text"
            name="username"
            className="RegisterUsername"
            placeholder="Username"
            required
          />
          <input
            type="email"
            name="email"
            className="RegisterUsername"
            placeholder="Email"
            required
          />
          <input
            type="password"
            name="password"
            className="RegisterUsername"
            placeholder="Password"
            required
          />
          <button type="submit" className="RegisterButton">
            Register
          </button>
        </form>
      </div>

      <div
        className={
          !loaded
            ? "RegisterRightInitial"
            : clicked
            ? "RegisterRightClicked"
            : "RegisterRight"
        }
      >
        <div
          className={
            !loaded
              ? "RegisterTextsInitial"
              : clicked
              ? "RegisterTextsClicked"
              : "RegisterTexts"
          }
        >
          <h1 className="RegisterHeading">Welcome Back!</h1>
          <p className="RegisterBreadcrumb">Already have an account?</p>
          <button className="RegisterLoginButton" onClick={handleClick}>
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;

// import React, { useEffect, useState } from 'react'
// import "./Register.css"
// import axios from "axios";
// import { useNavigate } from 'react-router-dom'
// const Register = () => {
//   const navigate = useNavigate();
//   const [clicked,Setclicked]=useState(false)
//    const [loaded,setLoaded] = useState(0)
//    const PageLoaded = () =>{
//        setTimeout(()=>{
//          setLoaded(true)
//        },200)
//      }
//      useEffect(()=>{
//        PageLoaded();
//      },[])
//   const handleClick = (e) =>{
//     Setclicked(true)
//     setTimeout(() => {
//       navigate("/login");
//     }, 500);
//   }
//     const [formData, setFormData] = useState({
//     fullName: "",
//     username: "",
//     email: "",
//     password: "",
//   });

//   const handleChange = (e) => {
//     setFormData((prev) => ({
//       ...prev,
//       [e.target.name]: e.target.value,
//     }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const res = await axios.post("http://localhost:5000/api/auth/register", formData);
//       alert(res.data.message);
//     } catch (err) {
//       alert(err.response?.data?.message || "Something went wrong");
//     }
//   };

//   return (
//     <div className='RegisterContainer'>
//       <div className={!loaded?"RegisterLeftInitial":clicked?"RegisterLeftClicked":"RegisterLeft"}>
//         <div className="RegisterDatas">
//           <h1 className="RegisterHeading-2">Registration</h1>
//           <input type="text" className="RegisterUsername" placeholder='Username' />
//           <input type="email" className="RegisterEmail" placeholder='Email'/>
//           <input type="password" className="RegisterPassword" placeholder='Password'/>
//           <button className="RegisterButton" onSubmit={handleSubmit}>Register</button>
//         </div>
//       </div>
//       <div className={!loaded?"RegisterRightInitial":clicked?"RegisterRightClicked":"RegisterRight"}>
//         <div className={!loaded?"RegisterTextsInitial":clicked?"RegisterTextsClicked":"RegisterTexts"}>
//           <h1 className="RegisterHeading">Welcome Back!</h1>
//           <p className="RegisterBreadcrumb">Alredy have an account?</p>
//           <button className="RegisterLoginButton" onClick={(e) => handleClick(e)}>Login</button>
//         </div>

//       </div>

//     </div>
//   )
// }

// export default Register
