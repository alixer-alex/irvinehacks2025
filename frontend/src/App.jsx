import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import DisplayGraph from './flaskComms.jsx'

import React from 'react';
import Navbar from './Components/Navbar/Navbar.jsx'

const Header = () => <header className="p-4 bg-blue-500 text-white">Header</header>;

const Sidebar = () => (
  <aside className="p-4 bg-gray-200 w-1/4">Sidebar</aside>
);

const MainContent = (props) => (
  <main className="p-4 flex-1">
    <section>
      <h1 className="text-xl font-bold">Main page</h1>
      <p>Home Page</p>
      <DisplayGraph username={props.username} />
    </section>
  </main>
);

const Footer = () => <footer className="p-4 bg-blue-500 text-white">Footer</footer>;

function Page () {
  const [username, setUsername] = useState("");
  //when writing the get username form, pass it as a return value into setUsername
  const current_theme = localStorage.getItem('current_theme');
  const [theme, setTheme] = useState(current_theme ? current_theme : 'light');

  useEffect(()=>{
    localStorage.setItem('current_theme', theme);
  },[theme])

  return (
    <div className={`container ${theme}`}>
      <Navbar theme={theme} setTheme={setTheme}/>
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
      
        <MainContent username = {username}/>
      </div>
      <Footer />
    </div>
    </div>
  )
};

export default Page;
