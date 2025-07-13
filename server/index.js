
const express = require("express");
const connectDB = require('./db.js')
const userSchema = require('./models/User.js')
const attendanceSchema = require('./models/Attendance.js')

const app = express()

connectDB()

app.listen(5000, () => {
    console.log("Server is running on port 5000");
    });