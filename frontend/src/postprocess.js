import React from 'react'
import './App.css';

function PostProcess({outputProps,setToggle}) {
  
  return (
    <div>
        <div style={{
            display : 'flex',
            justifyContent:'space-between',
            alignItems : 'center',
            color : 'white'
        }}>
            <h3>Results</h3>
            <button className='button' id='exe' onClick={()=>setToggle(false)}>Close</button>
        </div>
        {
            outputProps.map(
                (prop)=>(
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
                            disabled
                        /></p>
                        <div>
                            {JSON.stringify(prop.result)}
                        </div>
                    </div>
                )
            )
        }
    </div>
  );
}

export default PostProcess;
