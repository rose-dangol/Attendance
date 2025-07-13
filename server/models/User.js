const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  fullName: {
    type: String,
    required: true,
    trim: true,
  },
  username: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
  },
  registeredAt: {
    type: Date,
    default: Date.now,
  },
  role: {
    type: String,
    enum: ["student", "teacher", "admin"],
    default: "student",
  }
});

module.exports = mongoose.model("User", userSchema);
