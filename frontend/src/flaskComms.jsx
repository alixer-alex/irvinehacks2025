import React, { useState, useEffect } from 'react';

function App() {
    const [currentTime, setCurrentTime] = useState(0);
  
    useEffect(() => {
      fetch('/time').then(res => res.json()).then(data => {
        setCurrentTime(data.time);
      });
    }, []);
    return currentTime;
  }
  
  export default App;