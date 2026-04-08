import React from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import { Leaf } from 'lucide-react';
import Home from './pages/Home';
import About from './pages/About';
import Recognition from './pages/Recognition';

function App() {
  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-brand">
          <Leaf size={24} />
          <span>PlantAI</span>
        </div>
        <div className="nav-links">
          <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>Home</NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>About</NavLink>
          <NavLink to="/recognition" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>Disease Recognition</NavLink>
        </div>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/recognition" element={<Recognition />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
