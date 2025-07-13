const mongoose = require("mongoose");

const attendanceSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
  },
  status: {
    type: String,
    enum: ["present", "absent", "late"],
    default: "present",
  },
  recordedBy: {
    type: String, // e.g., "FaceRecognitionSystem"
    default: "FaceRecognitionSystem",
  },
});

module.exports = mongoose.model("Attendance", attendanceSchema);
