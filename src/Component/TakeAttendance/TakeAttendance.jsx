import React, { useEffect, useState, useRef } from "react";
import "./TakeAttendance.css";
import Dashboard from "../Dashboard/Dashboard";

import CameraAltOutlinedIcon from "@mui/icons-material/CameraAltOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import BoltOutlinedIcon from "@mui/icons-material/BoltOutlined";

const TakeAttendance = () => {
  const [hasCamera, setHasCamera] = useState(null);
  useEffect(() => {
    const checkCamera = async () => {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoInputs = devices.filter(
          (device) => device.kind === "videoinput"
        );
        setHasCamera(videoInputs.length > 0);
      } catch (err) {
        console.error("Error accessing media devices:", err);
        setHasCamera(false);
      }
    };

    checkCamera();
  }, []);
  // open camera
  const videoRef = useRef(null);
  const [cameraStarted, setCameraStarted] = useState(false);

  const handleTakeAttendanceClick = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraStarted(true);
      }
    } catch (error) {
      console.error("Camera access error:", error);
      alert("Unable to access camera.");
    }
  };
  return (
    <div>
      <div className="take-attendance-container">
        <Dashboard />
        <div className="main-content">
          <div className="top-bar">
            <div className="top-bar-title">
              <span className="section-heading">AI Attendance System</span>
              <span className="section-subtext">
                Secure, fast, and accurate attendance tracking system!
              </span>
            </div>
            <div className="top-bar-cameraCheck">
              {hasCamera === null && <span>🔍 Checking..</span>}
              {hasCamera === true && <span>🟢 Camera Ready</span>}
              {hasCamera === false && <span>🔴 No camera</span>}
            </div>
          </div>
          <div className="center-content">
            <div className="left-container">
              <div className="initialize-camera-container">
                <div className="initialize-camera">
                  <div className="camera-icon">
                    <CameraAltOutlinedIcon
                      sx={{
                        fontSize: 50,
                        borderRadius: "8px",
                        padding: "4px",
                      }}
                    />
                  </div>
                  <div className="camera-text">
                    Position yourself in front of the camera.
                  </div>
                </div>
                <div
                  className="take-attendance-btn"
                  onClick={handleTakeAttendanceClick}
                >
                  <CameraAltOutlinedIcon sx={{ fontSize: 28 }} /> Take
                  Attendance
                </div>
                {/* Camera preview */}
                {cameraStarted && (
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    style={{
                      width: "100%",
                      maxWidth: "500px",
                      marginTop: "20px",
                      border: "2px solid red",
                      background: "black",
                    }}
                  />
                )}
                <div className="subtext-section">
                  <div className="face-detect">
                    <VisibilityOutlinedIcon />
                    Face Detection
                  </div>
                  <div className="face-recog">
                    <BoltOutlinedIcon />
                    Instant Recognition
                  </div>
                </div>
              </div>
            </div>

            <div className="right-container">
              <div className="howto-title">...</div>
              <div className="right-gif">
                <img
                  src="/gifs/ho-to-video.gif"
                  alt="My GIF"
                  style={{
                    width: "350px",
                    height: "275px",
                    borderRadius: "15px",
                  }}
                />
              </div>
              <div className="right-userDetails">
                <div className="username typing-text typing-delay-1">User: Rose Dangol <br/>Email: rose@gmail.com <br/> User ID: 28684</div>
                {/* <div className="gmail typing-text typing-delay-2">Email: rose@gmail.com</div>
                <div className="userid typing-text typing-delay-3">User ID: 28684</div> */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TakeAttendance;
