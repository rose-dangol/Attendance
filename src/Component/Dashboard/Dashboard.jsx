import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";
// import logo from "../../images/logo.png";
// import lady from "../../images/lady.png";

// menu icons
import HomeIcon from "@mui/icons-material/Home";
import AddAPhotoIcon from "@mui/icons-material/AddAPhoto";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import PersonAddAltIcon from "@mui/icons-material/PersonAddAlt";

// toggle icons
import KeyboardDoubleArrowLeftIcon from "@mui/icons-material/KeyboardDoubleArrowLeft";
import KeyboardDoubleArrowRightIcon from "@mui/icons-material/KeyboardDoubleArrowRight";

const Dashboard = () => {
  const [drop, setDrop] = useState(false);
  const [arrow, setArrow] = useState(false);
  const dropClicked = (e) => {
    setDrop(false);
    setArrow(false);
    // console.log("bye");
  };
  const crossClicked = (e) => {
    setDrop(true);
    setTimeout(() => {
      setArrow(true);
    }, 600);
    // console.log("cross");
  };
  const routeLogin = () => {
    navigate("/login");
  };
  return (
    <>
      {arrow ? (
        <div className="open" onClick={(e) => dropClicked(e)}>
          <KeyboardDoubleArrowRightIcon style={{ fontSize: 50 }} />
        </div>
      ) : (
        ""
      )}

      <div className={drop ? "dashboard-Drop" : "dashboard-container"}>
        <div className="dashboard-wrapper">
          <div className="dashboard-top">
            <div className="dashboard-logo-title">
              <div className="dashboard-logo">
                <img
                  src={"/images/logo.png"}
                  alt="Logo"
                  style={{ height: "62px", width: "70px" }}
                />
              </div>
              <div className="dashboard-title">Attendify</div>
            </div>
            <div
              className="dashboard-dropdown"
              onClick={(e) => {
                setTimeout(() => {
                  crossClicked(e);
                }, 700);
              }}
            >
              <KeyboardDoubleArrowLeftIcon style={{ fontSize: 30 }} />
            </div>
          </div>
          <div className="dashboard-line"></div>
          <div className="dashboard-center">
            <div className="dashboard-menu">
              <div className="dashboard-icon">
                <HomeIcon />
              </div>
              <div className="dashboard-menu-data">Home</div>
            </div>
            <div className="dashboard-menu">
              <div className="dashboard-icon">
                <AddAPhotoIcon />
              </div>
              <div className="dashboard-menu-data">Take Attendance</div>
            </div>
            <div className="dashboard-menu">
              <div className="dashboard-icon">
                <ReceiptLongIcon />
              </div>
              <div className="dashboard-menu-data">Attendance Log</div>
            </div>
            <div className="dashboard-menu">
              <div className="dashboard-icon">
                <PersonAddAltIcon />
              </div>
              <div className="dashboard-menu-data">Add New User</div>
            </div>
          </div>
        </div>
        <div className="dashboard-bottom">
          <div className="dashboard-profile">
            <img
              src={"/images/lady.png"}
              alt="Logo"
              style={{
                height: "100%",
                width: "100%",
                objectFit: "cover", // Apply here
                borderRadius: "50%", // Make image circular too
              }}
            />
          </div>
          {/* <Link></Link> */}
          <Link to="../Login" className="dashboard-logout">
            <i class="fa-solid fa-arrow-right-from-bracket"></i> LogOut
          </Link>
          {/* <button className="dashboard-logout">
            <a href="./Login">
              <i class="fa-solid fa-arrow-right-from-bracket"></i> LogOut
            </a>
          </button> */}
          {/* <button className="dashboard-logout"><Link to="../Login"><i class="fa-solid fa-arrow-right-from-bracket"></i> LogOut</Link></button> */}
          {/* <Link to="../Login" className="dashboard-logout"><i class="fa-solid fa-arrow-right-from-bracket"></i>LogOut</Link> */}
        </div>
      </div>
    </>
  );
};

export default Dashboard;
