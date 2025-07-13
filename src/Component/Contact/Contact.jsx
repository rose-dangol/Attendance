import axios from "axios";
import { useState } from "react";

const Contact = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/login", {
        username,
        password
      });
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  };

  return (
    <div>
      <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Contact;
