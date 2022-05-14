import React from 'react'
import './App.css';
import axios from "axios";
import PostProcess from './postprocess';

const styles = {
  turn :  {
    display:'flex',
    overflow:'hidden',
    borderRadius:10,
    border: 'solid #000',
    borderWidth: '1px'
  }
}

const URLS = {
  0 : 'http://127.0.0.1:5000/tranx',
  1 : 'http://127.0.0.1:5000/yale'
}

const INITIAL_STATE = {
  inputText : '',
  outputSql : '',
  parser : 1
}

function App() {
  const [state,setState] = React.useState(INITIAL_STATE)
  const [outputProps,setoutputProps] = React.useState([])
  const [loading,setLoading] = React.useState(false)

  const onSubmit= async ()=>{
    setoutputProps([])
    let inputs = state.inputText.split("\n")
    let outputs = ""
    setLoading(true)
    try {
      for(let i=0;i<inputs.length;i++){
        let input = inputs[i];
        const response = await axios.post(
          URLS[state.parser],
          {
            "sentence" : input
          }
        )
        if(response.status!==200){
          throw new Error("Failed to fetch query")
        }
        outputs += response.data.output + "\n"
        outputProps.push({
          ...response.data,
          input : inputs[i],
          output : response.data.output
        })
      }
      setoutputProps(outputProps)
      onChangeOutput(outputs)
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

  const onChangeOutput=(value)=>{
    setState(
      prevState=>({
        ...prevState,
        outputSql :value 
      })
    )
  }
  const onChangeInput=(e)=>{
    setState(
      prevState=>({
        ...prevState,
        inputText : e.target.value
      })
    )
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
              backgroundColor : state.parser===0 ? 'grey' : 'blue',
              width : '100%',
              color : 'white',
              padding : 10,
              fontSize : 20
          }}>Logout</div>
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
          <PostProcess outputProps={outputProps} setoutputProps={setoutputProps}/>
        }
       </div>
      </div>
    </div>
  );
}

export default App;
