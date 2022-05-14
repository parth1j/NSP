const endpoints = {
    BASE : '/',
    LOGIN : '/login',
    REGISTER : '/register'
}

const errorMessages = {
    FAILED_LOGIN : 'Failed to login user',
    FAILED_REGISTER : 'Failed to register user',
    WRONG_USERNAME: 'Wrong username',
    WRONG_PASSWORD : 'Wrong password',
    USER_EXISTS : 'User already exists',
    UNAUTHORIZED : 'Access is unauthorized',
    FAILED_FETCH_USER : 'Failed to get users'
}

module.exports = {
    endpoints,
    errorMessages
}