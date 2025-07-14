import userRouter from '../backend-node/routes/auth.js'
import express from "express";
import connectDB from './config/db.js';
import dotenv from 'dotenv';
import cors from 'cors'



// const connectDB = require("./config/db");
// const dotenv = require("dotenv");
// const cors = require("cors");

dotenv.config();
connectDB();

const app = express();
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", userRouter);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
