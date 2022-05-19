import React from 'react'
import './App.css';
import jwtDecode from 'jwt-decode';
import {deleteQuery, executeQuery, postQuery} from './url'

const OutputComponent = ({data,token,outputProps,setoutputProps})=>{
    const condition = "_id" in data;
    const [value,setValue] = React.useState(data.query);
    const [result,setResult] = React.useState(data.result);
    const [loading,setLoading] = React.useState(false);
    const [saved,setSaved] = React.useState(false);

    const onChangeOutput = (event)=>setValue(event.target.value)

    const onSave = async ()=>{
        let data = {
            query : value,
            result : JSON.stringify(result),
            user : jwtDecode(token)._id
        }
        try {
            await postQuery(data,token)
            setSaved(true)
        } catch (error) {
            window.alert(error)
            console.log(error)
        }
        
    }

    const displayResult = (result)=>{
        result = condition===true ?  JSON.parse(result) : result
        let headers = result.header
        let body = result.body
        return (
            <table>
                <thead>
                    <tr>
                        {headers.map(header=><th>{header}</th>)}
                    </tr>
                </thead>
                <tbody>
                {
                    body.map(
                        row=>(
                            <tr>{row.map(item=><td>{item}</td>)}</tr>
                        )
                    )
                }
                </tbody>    
            </table>
        )
    }
    const onDelete = async ()=>{
        try {
            await deleteQuery(data._id,token)
            setoutputProps(outputProps.filter(prop=>prop._id!==data._id))
        } catch (error) {
            window.alert(error)
            console.error(error)
        }
    }
    const onExecute = async ()=>{
        setLoading(true)
        try {
          const response = await executeQuery(value,data.table)
          setResult(response.data.result)
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
                <button className='button-small' id='clear' disabled={saved===true || condition===true} onClick={onSave}>
                    {saved===true || condition===true? 'Saved' : 'Save'}
                </button>
                {
                    saved===true || condition===true?
                    <button className='button-small' id='run' onClick={onDelete}>Delete</button>:
                    <button className='button-small' id='run' onClick={onExecute}>Execute</button>
                }
                
            </div>
            <div style={{alignItems:'center',maxHeight:200,overflow:'auto'}}>{result===undefined? null : displayResult(result)}</div>
        </div>
    )
}


function PostProcess({outputProps,token,setoutputProps}) {
  return (
    <div>
        <div style={{
            display : 'flex',
            justifyContent:'space-between',
            alignItems : 'center',
            maxHeight : 300,
            overflow : 'auto',
            color : 'white'
        }}>
            <h3>Results</h3>
        </div>
       <div style={{
           maxHeight:500,
           overflow : 'auto'
       }}>
        {
            outputProps.map(
                (prop)=><OutputComponent 
                    data={prop} 
                    token={token}
                    outputProps={outputProps}
                    setoutputProps={setoutputProps}/>
            )
        }
       </div>
    </div>
  );
}

export default PostProcess;
