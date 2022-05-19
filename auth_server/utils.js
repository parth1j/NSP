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
    FAILED_FETCH_QUERY : 'Failed to get queries',
    FAILED_POST_QUERY : 'Failed to save query',
    FAILED_PUT_QUERY : 'Failed to update query',
    FAILED_DELETE_QUERY : 'Failed to delete query'
}

module.exports = {
    endpoints,
    errorMessages
}