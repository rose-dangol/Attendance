// "this is where I tell my app how to talk to the database"

import mongoose from "mongoose";

const connectDB = async () => {
    try {
        const conn = await mongoose.connect(
            'mongodb+srv://rose:rosedangol5@cluster0.rrrmghg.mongodb.net/attendancesys?retryWrites=true&w=majority&appName=Cluster0'
        );
        console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (error) {
        console.error('MongoDB connection error:', error);
        process.exit(1);
    }   
};

export default connectDB;