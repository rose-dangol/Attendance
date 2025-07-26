import React, { useRef, useState } from "react";

const CameraTest = () => {
  const videoRef = useRef(null);
  const [cameraStarted, setCameraStarted] = useState(false);
  const [stream, setStream] = useState(null);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setCameraStarted(true);
      setStream(mediaStream); // Save stream for cleanup later

      // Delay to ensure <video> is rendered before attaching
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
          console.log("🎥 Stream attached");
        }
      }, 100);
    } catch (err) {
      console.error("❌ Camera error:", err);
      alert("Unable to access the camera.");
    }
  };

  // Optional: stop camera if component unmounts
  React.useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [stream]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>🎥 Camera Test</h2>
      <button
        onClick={startCamera}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#1976d2",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          marginBottom: "20px",
        }}
      >
        Start Camera
      </button>

      {cameraStarted ? (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{
            width: "100%",
            maxWidth: "600px",
            border: "2px solid #1976d2",
            borderRadius: "8px",
            backgroundColor: "black",
          }}
        />
      ) : (
        <div
          style={{
            width: "100%",
            maxWidth: "600px",
            height: "340px",
            border: "2px dashed gray",
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#777",
          }}
        >
          Camera not started yet
        </div>
      )}
    </div>
  );
};

export default CameraTest;
