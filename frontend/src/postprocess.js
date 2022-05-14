import React from 'react'
import './App.css';
import AceEditor from "react-ace";
import axios from "axios";
import "ace-builds/src-noconflict/mode-sql";
import "ace-builds/src-noconflict/theme-github";

const OutputComponent = ({data})=>{
    const [value,setValue] = React.useState(data.output);
    const [result,setResult] = React.useState(data.result);
    const [loading,setLoading] = React.useState(false);

    const onChangeOutput = (event)=>setValue(event.target.value)
    
    const onExecute = async ()=>{
        setLoading(true)
        try {
            const response = await axios.post(
            'http://127.0.0.1:5000/execute',
            {
                query : value,
                table :data.table
            }
            )
            console.log(response.data)
            if(response.status!==200){
                throw new Error("Failed to fetch query")
            }
          setResult(JSON.stringify(response.data.result))
          setLoading(false)
        } catch (error) {
          setLoading(false)
          window.alert(error)
          console.error(error)
        }
      }
    return (
        <div style={{
            padding : 5,
            margin : 5,
            textAlign : 'center',
            borderRadius : 10,
            backgroundColor : '#c8cfca'
        }}>
            <div>
            <textarea 
                id="txtArea" 
                rows="5" 
                cols="70" 
                value={value}
                onChange={(event)=>onChangeOutput(event)}/>
            
            </div>
            <div className='App-header'>
                <button className='button-small' id='clear'>Save</button>
                <button className='button-small' id='run' onClick={onExecute}>Execute</button>
            </div>
            <div><p>{result}</p></div>
        </div>
    )
}
function PostProcess({outputProps}) {
  return (
    <div>
        <div style={{
            display : 'flex',
            justifyContent:'space-between',
            alignItems : 'center',
            color : 'white'
        }}>
            <h3>Results</h3>
        </div>
        {
            outputProps.map(
                (prop)=><OutputComponent data={prop}/>
            )
        }
    </div>
  );
}

export default PostProcess;
