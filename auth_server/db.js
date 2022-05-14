const mongoose = require('mongoose')
const { Schema } = mongoose

const UserSchema = new Schema({
    userName: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    }
})

const QuerySchema = new Schema({
    query : {
        type: String,
        required: true
    },
    result: {
        type: String,
        required: true
    },
    user : {
        type : Schema.Types.ObjectId,
        ref: 'User'
    }
})


const User = mongoose.model('User', UserSchema)
const Query = mongoose.model('Query', QuerySchema)

module.exports = {
    userModel : User,
    queryModel : Query
}