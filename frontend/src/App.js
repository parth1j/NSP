import React from 'react'
import './App.css';
import { Route, Routes } from "react-router-dom";
import Auth from "./auth";
import Home from "./home";

function App() {
  const [token,setToken] = React.useState(localStorage.getItem('token'))
  return (
    <Routes>
      <Route path="/" exact element={<Auth token={token} setToken={setToken}/>}/>
      <Route path="/home" exact element={<Home token={token} setToken={setToken}/>}/>
    </Routes>
  );
}

export default App;
