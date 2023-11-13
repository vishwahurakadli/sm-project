// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavBar from "./components/NavBar";
import HomePage from "./components/HomePage";
import ToxicClassifierPage from './components/ToxicClassifierPage';
import TopicModelingPage from './components/TopicModelingPage';



const App = () => {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/toxic-classifier" element={<ToxicClassifierPage />} />
        <Route path="/topic-modeling" element={<TopicModelingPage />} />
      </Routes>
    </Router>
  );
};

export default App;
