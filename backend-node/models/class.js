// // class.model.js
// import mongoose from "mongoose";

// const classSchema = new mongoose.Schema({
//   name: {
//     type: String,
//     required: true,
//   },
//   department: {
//     type: String, // e.g., "Computer Science"
//   },
//   semester: {
//     type: String, // e.g., "7th Semester"
//   },
//   members: [{
//     type: mongoose.Schema.Types.ObjectId,
//     ref: "User", // references students/teachers
//   }]
// }, { timestamps: true });

// export default mongoose.model("Class", classSchema);
