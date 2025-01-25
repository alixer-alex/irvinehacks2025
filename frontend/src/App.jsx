import { useState } from 'react'
import './App.css'
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import './comms.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <label for="user_name">Enter Your Instagramm Username: </label>
      
      <input type="text" id="name" name="name" required minlength="4" maxlength="8" size="10" />
    </>
  )
}

export default App();
