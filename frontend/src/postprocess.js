import React from 'react'
import './App.css';

function PostProcess({outputProps,onChangeOutput,setoutputProps,setToggle}) {
  const onSelectColumn =(value,index)=>{
        var textarea = document.getElementById("textArea");  
        var prefix = (textarea.value).substring(0,textarea.selectionStart);
        let suffix = (textarea.value).substring(textarea.selectionEnd);
        let replacement = prefix+value+suffix;
        outputProps[index].output = replacement;
        let result = ""
        outputProps.forEach((prop)=>{result += prop.output + '\n'})
        setoutputProps(outputProps)
        onChangeOutput(result)
  }
  
  const onChange = (value,index) =>{
    outputProps[index].output = value;
    let result = ""
    outputProps.forEach((prop)=>{result += prop.output + '\n'})
    setoutputProps(outputProps)
    onChangeOutput(result)
  }
  
  return (
    <div>
        <div style={{
            display : 'flex',
            justifyContent:'space-between',
            alignItems : 'center',
            color : 'white'
        }}>
            <h3>Replace col tags with columns</h3>
            <button className='button' id='exe' onClick={()=>setToggle(false)}>Close</button>
        </div>
        {
            outputProps.map(
                (prop,index)=>(
                    <div style={{
                        padding : 5,
                        margin : 5,
                        textAlign : 'center',
                        borderRadius : 10,
                        backgroundColor : '#c8cfca'
                    }}>
                        <p><textarea 
                            id="textArea" 
                            cols="70" 
                            value={prop.output} 
                            onChange = {(e)=>onChange(e.target.value,index)}
                        /></p>
                        <div style={{
                            display :'flex',
                            maxWidth : 530,
                            overflow : 'auto' 
                        }}>
                            {
                                prop.columns.map(
                                    (column)=>(
                                        <div style={{
                                            color : 'white',
                                            padding : 5,
                                            margin : 5,
                                            borderRadius : 10,
                                            backgroundColor : 'blue'
                                        }} onClick={()=>onSelectColumn(column,index)}>
                                            <h6>{column}</h6>
                                        </div>
                                    )
                                )
                            }
                        </div>
                    </div>
                )
            )
        }
    </div>
  );
}

export default PostProcess;
