import React, { useState } from 'react';
import './App.css';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [teacher, setTeacher] = useState(null);

  const handleLogin = (teacherData) => {
    setTeacher(teacherData);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setTeacher(null);
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <Dashboard teacher={teacher} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;