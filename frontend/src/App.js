import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import GenerateQuiz from './components/GenerateQuiz';
import QuizHistory from './components/QuizHistory';
import QuizDetail from './components/QuizDetail';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Header activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route 
              path="/" 
              element={<GenerateQuiz />} 
            />
            <Route 
              path="/history" 
              element={<QuizHistory />} 
            />
            <Route 
              path="/quiz/:id" 
              element={<QuizDetail />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
