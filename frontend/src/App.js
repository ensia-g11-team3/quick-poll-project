import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CreatePoll from './components/CreatePoll';
import PollView from './components/PollView';
import PollResults from './components/PollResults';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<CreatePoll />} />
          <Route path="/poll/:pollLink" element={<PollView />} />
          <Route path="/poll/:pollLink/results" element={<PollResults />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

