import React from "react";
import { registerUser, loginUser } from "./url";
import { useNavigate } from 'react-router-dom';
import { Navigate } from "react-router";

const styles = {
    root : {
        display :'flex',
        width : '100%',
        height : '100%',
        justifyContent :'space-around',
        alignItems : 'center'
    },
    parent : {
        width : '100%',
        height : '100%',
        justifyContent :'center',
        alignItems : 'center'
    },
    form : {
        padding:15,
        borderRadius:10,
        border: 'solid grey',
        borderWidth: '1px',
    },
    temp : {
        textAlign : 'center'
    },
    textField : {
        padding:10,
        borderRadius : 10,
    },
    sendButton : {
        margin:10,
        padding:10,
        borderRadius : 10,
        width : '100px',
        backgroundColor:'grey',
        color:'black'
    },
    text : {color:'white',textAlign:'center'}
}

const Auth = (props)=>{
    const {token,setToken} = props
    const [inputData,setInputData] = React.useState({
        userName : '',
        password : '',
        confirm_password : ''
    });
    const [loading,setLoading] = React.useState(false);
    const [isSignUp,setSignUp] = React.useState(false);
    const history = useNavigate();

    const onSubmit = async (event)=>{
        event.preventDefault();
        setLoading(true)
        if(inputData.userName==='' || inputData.password===''){
            window.alert("Please put all the required values")
            return;
        }
        let data = {
            userName: inputData.userName,
            password : inputData.password
        }
        if(isSignUp===true){
            if(inputData.password!==inputData.confirm_password){
                window.alert("Passwords do not match")
                return;
            }
            try {
                const response = await registerUser(data)
                setLoading(false)
                if(response.data.token===undefined){
                    throw new Error(response.data.message)
                }
                localStorage.setItem('token',response.data.token)
                setToken(response.data.token)
                history('/home')
            } catch (error) {
                setLoading(false)
                window.alert(error)
            }
        } else {
            try {
                const response = await loginUser(data)
                setLoading(false)
                if(response.data.token===undefined){
                    throw new Error(response.data.message)
                }
                console.log(response)
                localStorage.setItem('token',response.data.token)
                setToken(response.data.token)
                history('/home')
            } catch (error) {
                setLoading(false)
                window.alert(error)
            }
        }
    }

    const onClickh5 = ()=>setSignUp(!isSignUp)
    
    if(token){
        return <Navigate to='/home'/>
    }
    const displayForm = ()=>(
        <div style={styles.form}>
            <div style={styles.temp}>
                <input type='text' 
                    placeholder='Enter User Name' 
                    name='name'
                    style={styles.textField} 
                    value={inputData.userName}
                    onChange={(event)=>setInputData({
                        ...inputData,
                        userName : event.target.value
                    })}/>
            </div>
            <br/>
            <div style={styles.temp}>
                <input type='password' 
                    placeholder='Enter Password' 
                    name='password'
                    style={styles.textField} 
                    value={inputData.password}
                    onChange={(event)=>setInputData({
                        ...inputData,
                        password : event.target.value
                    })}/>
            </div>
            <br/>
            { isSignUp===true ? (
                <div style={styles.temp}>
                    <input type='password' 
                        placeholder='Reenter Password' 
                        name='confirm_password'
                        style={styles.textField} 
                        value={inputData.confirm_password}
                        onChange={(event)=>setInputData({
                            ...inputData,
                            confirm_password : event.target.value
                        })}/>
                </div>
            ) : null }
            <div style={styles.temp}> 
               {
                   loading===false ? 
                   <button style={styles.sendButton} onClick={(e)=>onSubmit(e)}>{ isSignUp===true ? 'Sign Up' : 'Login'}</button>
                   : <div>{isSignUp===true ? 'Signing Up...' : 'Logging in...'}</div>
               }
            </div>
            <br/>
            <div onClick={()=>onClickh5()}>
                <h5 style={styles.text}>{ isSignUp===true ? 'Sign In if already registered' : 'Create an account'}</h5>
            </div> 
        </div>
    )
    return (
        <div style={styles.parent}>
            <div style={styles.root}>
            <div style={styles.temp}>
                <h1 style={{...styles.text,fontSize:40}}>TexttoSQL</h1>
                <p style={{color : 'grey',maxWidth:300,textAlign:'center'}}>
                    Convert assertive and interrogative english sentences to executable SQL queries.
                    Execute against a public domain specific database.
                </p>
            </div>
            {displayForm()}
        </div>
        </div>
    );
}

export default Auth;