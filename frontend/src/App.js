import React from 'react'
import './App.css';
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-sql";
import "ace-builds/src-noconflict/theme-github";

const styles = {
  turn :  {
    display:'flex',
    overflow:'hidden',
    borderRadius:10,
    border: 'solid #000',
    borderWidth: '1px'
  }
}

const INITIAL_STATE = {
  inputText : '',
  outputSql : '',
  parser : 0
}

function App() {
  const [state,setState] = React.useState(INITIAL_STATE)

  const onSubmit=()=>{

  }

  const onClear=()=>setState(INITIAL_STATE)

  const toggleHandler = (option)=>setState(
    prevState=>({
      ...prevState,
      parser : option
    })
  )

  const onChangeOutput=(e)=>{
    setState(
      prevState=>({
        ...prevState,
        outputSql : e.target.value
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
        <div><h3>TexttoSQL</h3></div>
        <div className="commands">
          <button className='button' id='clear' onClick={onClear}>Clear</button>
          <button className='button' id='run' onClick={onSubmit}>Run</button>
        </div>
        <div style={styles.turn}>
          <div style={{
              backgroundColor : state.parser===1 ? 'grey' : 'blue',
              width : '100%',
              padding : 10,
              fontSize:20
          }} onClick={()=>toggleHandler(0)}>Tranx</div>
          <div style={{
              backgroundColor : state.parser===0 ? 'grey' : 'blue',
              width : '100%',
              color : 'white',
              padding : 10,
              fontSize : 20
          }}onClick={()=>toggleHandler(1)}>Yale</div>
        </div>
      </header>
      <div className='body'>
        <div className='txt'>
          <textarea 
            id="txtArea" 
            rows="20" 
            cols="70" 
            draggable={false}
            value={state.inputText}
            onChange={onChangeInput}></textarea>
          <div className='results'>
            <h4>Results to be displayed here</h4>
          </div>
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
