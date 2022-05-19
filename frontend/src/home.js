import React from 'react'
import './App.css';
import { Navigate, useNavigate } from "react-router";
import PostProcess from './postprocess';
import jwtDecode from "jwt-decode";
import {generateQuery, getUserQueries} from './url'

const styles = {
  turn :  {
    display:'flex',
    overflow:'hidden',
    textAlign : 'center',
    borderRadius:10,
    border: 'solid #000',
    borderWidth: '1px'
  }
}


const INITIAL_STATE = {
  inputText : `What are the maximum and minimum budget of the department ?\nList the creation year, name and budget of each department .`
}

function Home(props) {
  const {token,setToken} = props
  const user_name = token!==null ? jwtDecode(token).userName : "User Name"
  const [state,setState] = React.useState(INITIAL_STATE)
  const [outputProps,setoutputProps] = React.useState([])
  const [loading,setLoading] = React.useState(false)
  const history = useNavigate()

  const onSubmit= async ()=>{
    let inputs = state.inputText.split("\n")
    let props = []
    setLoading(true)
    try {
      for(let i=0;i<inputs.length;i++){
        let input = inputs[i];
        const response = await generateQuery(input)
        console.log(response.data.output)
        props.push({
          ...response.data,
          input : inputs[i],
          query :response.data.output
        })
      }
      setoutputProps(props)
      setLoading(false)
    } catch (error) {
      setLoading(false)
      window.alert(error)
      console.error(error)
    }
  }


  const onClear=()=>{
    setState(INITIAL_STATE)
    setoutputProps([])
  }

  const onLogout = ()=>{
    setToken(null);
    localStorage.removeItem('token')
    history('/')
  }

  const onChangeInput=(e)=>{
    setState(
      prevState=>({
        ...prevState,
        inputText : e.target.value
      })
    )
  }

  const getpastData = async ()=>{
    try {
      const response = await getUserQueries(jwtDecode(token)._id,token);
      setoutputProps(response.data)
    } catch (error) {
        console.log(error)
        window.alert(error)
    }
  }

  if(token===null){
    return <Navigate to = '/'/>
}

  return (
    <div className="App">
      <header className="App-header">
        <div><h3>TexttoSQL</h3></div>{
          loading===true ? (
            <h4>Constructing query...Please wait</h4>
          ) : (
            <div className="commands">
              <button className='button' id='clear' onClick={onClear}>Clear</button>
              <button className='button' id='run' onClick={onSubmit}>Run</button>
            </div>
          )
        }
        <div style={styles.turn}>
            <div style={{
              backgroundColor : 'grey' ,
              textAlign : 'center',
              color : 'white',
              padding : 10,
              fontSize : 15
          }}>{user_name}</div>
          <div style={{
              backgroundColor : 'blue',
              color : 'white',
              padding : 10,
              fontSize : 20
          }} onClick={onLogout} >Logout</div>
        </div>
      </header>
      <div className='body'>
        <div className='txt'>
          <textarea 
            id="txtArea" 
            rows="30" 
            cols="70" 
            value={state.inputText}
            onChange={onChangeInput}/>
        </div>
       <div>
       {
          outputProps.length===0 ? 
          <div>
            <p style={{color:'white'}}>Type some query in english assertive or interrogative form.</p>
          </div>
          :
          <PostProcess outputProps={outputProps} token={token} setoutputProps={setoutputProps}/>
        }
       </div>
      </div>
      <div style={{
        position : 'fixed',
        right: 2,
        bottom : 10
      }}>
        <button className='button' id='clear' onClick={getpastData}>Show past queries</button>
      </div>
    </div>
  );
}

export default Home;
