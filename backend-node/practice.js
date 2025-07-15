import User from "../models/User.js"

export const registerAUser = async (req, res)=>{
    try{
        const name = req.body.username;
        const repeats = await User.findOne({username:name});
        if(repeats){
            return res.status(400).send("user already exists")
        }
        const user = new User({
            fullName: req.body.fullName,
            username: req.body.username,
            email: req.body.email,
            password: req.body.password
        })
        await user.save();
        return res.status(200).send("User registered")
    }catch(error){
        return res.status(200).send(error)
    }
}

export const register= async (req, res) => {
    const name = req.body.username;
    const repeatedUsername = await User.findOne({username:name})
    if(repeatedUsername){
        return res.status(400).send("Already");
    }
    const key = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(req.body.password,key);
    const user=new User({
        fullName:req.body.fullName,
        password :  hashedPassword
    })
    await user.save();
}


export const login = async (req, res) =>{
    try{
        const validate = await User.findOne ({username:req.body.username});
        if(!validate){
            return res.status(404),send("USer not found")
        }
        const validpassword = await bcrypt.compare(req.body.password, validate.password);
    }catch(error){

    }
}

export const deleteUser = async (req, res) => {
    try{
        const deleteID = req.body.id;
        const userExist = await User.findOne({id:deleteID});
        if(!userExist){
            return res.status(404),send("USer not found")
        }
        await User.deleteOne({id:deleteID});
        return res.status(111),send("User deleted")
    }catch(e){
        return res.status(404).send("User not deleted")
    }

}