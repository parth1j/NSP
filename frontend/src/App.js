import React from 'react'
import './App.css';
import AceEditor from "react-ace";
import axios from "axios";
import "ace-builds/src-noconflict/mode-sql";
import "ace-builds/src-noconflict/theme-github";
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
  const [toggle,setToggle] = React.useState(false)
  const [loading,setLoading] = React.useState(false)

  const onSubmit= async ()=>{
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

  const onExecute=()=>{
    setLoading(true)
    try {
      state.outputSql.split("\n").forEach(
        async (query,index)=>{
          const response = await axios.post(
            'http://127.0.0.1:5000/execute',
            {
              query : query,
              table : outputProps[index].table
            }
          )
          console.log(response.data)
          if(response.status!==200){
            throw new Error("Failed to fetch query")
          }
          outputProps[index].result = JSON.stringify(response.data.result)
        }
      )
      setoutputProps([...outputProps])
      setToggle(true)
      setLoading(false)
    } catch (error) {
      setLoading(false)
      window.alert(error)
      console.error(error)
    }
  }

  const onClear=()=>setState(INITIAL_STATE)

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
          }}>Beta</div>
        </div>
      </header>
      <div className='body'>
        <div className='txt'>{
            toggle===false ? (
              <textarea 
                id="txtArea" 
                rows="20" 
                cols="70" 
                value={state.inputText}
                onChange={onChangeInput}></textarea>
            ) : <PostProcess outputProps={outputProps} setToggle={setToggle} />
          }{
            toggle===true ? null : (
              <div className='results'>
                <h4>Get Results for SQL queries</h4>
                <button className='button' id='exe' onClick={onExecute}>Execute</button>
              </div>
            )
          }
        </div>
        <AceEditor
          mode="sql"
          theme="github"
          value={state.outputSql}
          onChange={onChangeOutput}
          name="UNIQUE_ID_OF_DIV"
          editorProps={{ $blockScrolling: true }}
        />
      </div>
    </div>
  );
}

export default App;
