import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import DisplayGraph from './flaskComms.jsx'

import React from 'react';
import Navbar from './Components/Navbar/Navbar.jsx'



function Page () {
  const [username, setUsername] = useState("x");
  //when writing the get username form, pass it as a return value into setUsername
  const current_theme = localStorage.getItem('current_theme');
  const [theme, setTheme] = useState(current_theme ? current_theme : 'light');

  useEffect(()=>{
    localStorage.setItem('current_theme', theme);
    
  },[theme, username])
  // const Header = () => <header className="p-4 bg-blue-500 text-white">Header</header>;

// const Sidebar = () => (
//   <aside className="p-4 bg-gray-200 w-1/4">Sidebar</aside>
// );

  const MainContent = (props) => (
    <main className="main">
      <section>
        <h1 className="text-label">Enter Instagram Username: </h1>
        <User_Input/>
        <DisplayGraph username={props.username} />
      </section>
    </main>
  );

  // const Footer = () => <footer className="p-4 bg-blue-500 text-white">Footer</footer>;

  const handleEnter = (value) => {
    // alert(`you pressed enter w/: ${value}`);
    console.log(value.value);
    setUsername(value.value)
  };

  const User_Input = ({ label }) => {
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        handleEnter(e.target); // Call onEnter handler when Enter is pressed
      }
    };

  return (
    <div className="input-text">
      <label>{label}</label>
      <input
        type="text"
        className="modern-textbox"
        onKeyDown={handleKeyDown} // Listen for key presses
      />
    </div>
  )
};
  return (
    <div className={`container ${theme}`}>
      <Navbar theme={theme} setTheme={setTheme}/>
    <div className="flex flex-col min-h-screen">
      <MainContent username = {username}/>
      <div className="flex flex-1">
      
      </div>
    </div>
    </div>
  )
};

export default Page;
