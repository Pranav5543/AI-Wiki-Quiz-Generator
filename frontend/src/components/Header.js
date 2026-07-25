import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BookOpen, History, Brain } from 'lucide-react';

const Header = ({ activeTab, setActiveTab }) => {
  const location = useLocation();

  const isActive = (path) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <header className="bg-white shadow-lg border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Wiki Quiz</h1>
              <p className="text-xs text-gray-500">AI Powered Platform</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex space-x-1">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                isActive('/') 
                  ? 'bg-blue-100 text-blue-700 font-medium' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              }`}
              onClick={() => setActiveTab('generate')}
            >
              <BookOpen className="h-4 w-4" />
              <span>Generate Quiz</span>
            </Link>
            
            <Link
              to="/history"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                isActive('/history') 
                  ? 'bg-blue-100 text-blue-700 font-medium' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              }`}
              onClick={() => setActiveTab('history')}
            >
              <History className="h-4 w-4" />
              <span>Past Quizzes</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
