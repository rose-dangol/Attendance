// "If someone tries to register, here's what we check, save, or return."

import User from "../models/User.js";
import bcrypt from "bcrypt";

export const register = async (req, res) => {
  try {
    const name = req.body.username; // name = Rose     username= prashant,krisha, jeeswan, ujan, manjit, Rose
    const repeatedUsername = await User.findOne({ username: name });
    if (repeatedUsername) {
      return res.status(400).send("Username already exists!!");
    }
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(req.body.password, salt);
    const user = new User({
      fullName: req.body.fullName,
      email: req.body.email,
      password: hashedPassword,
      username: req.body.username,
    });
    await user.save();
    return res.status(200).send("user registered successfully");
  } catch (error) {
    return res.status(500).send(error);
  }
};

export const login = async (req, res) => {
  console.log("Login route hit ✅");
  try {
    const username = req.body.username;
    const validation = await User.findOne({ username: username });
    if (!validation) {
      return res.status(404).send("user not found!!");
    }
    const validpassword = await bcrypt.compare(
      req.body.password,
      validation.password
    );
    if (!validpassword) {
      return res.status(800).send("Wrong password hanis vai!!");
    }
    return res.status(200).send(validation);
  } catch (err) {
    return res.status(500).send(err);
  }
};
export const deleteUser = async (req, res) => {
  try {
    const deleteID = req.body.id;
    // const userExist = await User.findOne({_id:deleteID});
    const userExist = await User.findById(deleteID);
    if (!userExist) {
      return res.status(404).send("User not found");
    }
    // await User.deleteOne({id:deleteID});
    await userExist.deleteOne();
    return res.status(111).send("User deleted");
  } catch (e) {
    return res.status(404).send("User not deleted");
  }
};
export const getAllStudent = async (req, res) => {
  try {
    const students = await User.find();
    res.status(200).json(students);
  } catch (err) {
    res.status(404).send(err.message);
  }
};
export const addNewUser = async (req, res) => {
  try {
    console.log("🚀 addNewUser endpoint hit");
    const { fullName, email, username, password, role } = req.body;
    const repeatedUsername = await User.findOne({ username });
    if (repeatedUsername) {
      return res.status(400).send("Username already exists!");
    }
    const repeatedEmail = await User.findOne({ email });
    if (repeatedEmail) {
      return res.status(400).send("Email already registered!");
    }
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    const user = new User({
      fullName,
      email,
      password: hashedPassword,
      username,
      role,
    });
    await user.save();
    return res.status(201).send("User registered successfully");
  } catch (error) {
    console.error("Error registering user:", error);
    return res.status(500).send("Something went wrong. Please try again later.");
  }
};
/*
  try{
    const name = req.body.username;
    const repeatedUsername = await User.findOne({username:name})
    if(repeatedUsername){
      return res.status(400).send("Username already exists!!")
    }
        const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(req.body.password, salt)
    const user = new User ({
      fullName: req.body.fullName,
      email: req.body.email,
      password: hashedPassword,
      username: req.body.username,
      role: req.body.role,
    })
    await user.save();
    return res.status(200).send("user registered successfully")
  }catch(error){
    return res.status(500).send(error)
  }
*/
