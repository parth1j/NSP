import axios from "axios"
const BASE_URL = 'http://localhost:7000'
const INF_URL = 'http://localhost:5000'
const LOGIN_URL = `${BASE_URL}/users/login`
const REGISTER_URL = `${BASE_URL}/users/register`
const QUERY_BASE_URL =(_id)=> `${BASE_URL}/query/${_id}`
const POST_QUERY_URL = `${BASE_URL}/query`
const GENERATE_QUERY_URL = `${INF_URL}/yale`
const EXECUTE_QUERY_URL = `${INF_URL}/execute`

export const generateQuery = (sentence)=>{
    return new Promise((resolve,reject)=>{
        axios.post(
            GENERATE_QUERY_URL,
            {
              "sentence" : sentence
            }
          ).then(
            response=>{
                if(response.status!==200){
                    reject("Failed to fetch query")
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const executeQuery = (query,table)=>{
    return new Promise((resolve,reject)=>{
        axios.post(
            EXECUTE_QUERY_URL,
            {
                query : query,
                table : table
            }
          ).then(
            response=>{
                if(response.status!==200){
                    reject("Failed to fetch query")
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const loginUser = (data)=>{
    return new Promise((resolve,reject)=>{
        axios.post(LOGIN_URL,data).then(
            response=>{
                if(response.status!==200){
                    reject(response.data.message)
                }
                if(response.error===true){
                    reject(response.data.message)
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const registerUser = (data)=>{
    return new Promise((resolve,reject)=>{
        axios.post(REGISTER_URL,data).then(
            response=>{
                if(response.status!==200){
                    reject(response.data.message)
                }
                if(response.error===true){
                    reject(response.data.message)
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const getUserQueries = (_id,token)=>{
    return new Promise((resolve,reject)=>{
        let config = {
            headers: { 
                authorization: `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        };
        axios.get(QUERY_BASE_URL(_id),config).then(
            response=>{
                if(response.status!==200){
                    reject(response.data.message)
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const postQuery = (body,token)=>{
    return new Promise((resolve,reject)=>{
        let config = {
            headers: { 
                authorization: `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        };
        axios.post(POST_QUERY_URL,body,config).then(
            response=>{
                if(response.status!==200){
                    reject(response.data.message)
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}

export const deleteQuery = (_id,token)=>{
    return new Promise((resolve,reject)=>{
        let config = {
            headers: { 
                authorization: `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        };
        axios.delete(QUERY_BASE_URL(_id),config).then(
            response=>{
                if(response.status!==200){
                    reject(response.data.message)
                }
                resolve(response)
            }
        ).catch(
            error=>{
                reject(error)
            }
        )
    })
}