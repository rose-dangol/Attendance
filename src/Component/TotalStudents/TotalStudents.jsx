import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
const TotalStudents = () => {
const [students, setStudents] = useState([]);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/auth/getAll");
        setStudents(res.data);
      } catch (error) {
        console.error("Failed to fetch students", error);
      }
    };
    fetchStudents();
  }, [students]);
  return (
    <div>
      <h2>Registered Students</h2>
      <div className="studentDetail">
        {students.length === 0 ? (
          <p>No students found.</p>
        ) : (
          students.map((student) => (
            <div key={student._id} className="">
              <p>Username:{student.username} </p>
              <p> Email: {student.email} </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TotalStudents;
