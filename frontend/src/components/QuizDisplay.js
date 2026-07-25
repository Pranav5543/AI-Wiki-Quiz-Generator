import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  RotateCcw, 
  BookOpen, 
  Users, 
  MapPin, 
  Building, 
  Lightbulb,
  Clock,
  Target,
  CheckCircle,
  XCircle,
  AlertTriangle
} from 'lucide-react';

const QuizDisplay = ({ quizData, onNewQuiz }) => {
  const [showAnswers, setShowAnswers] = useState(false);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizMode, setQuizMode] = useState(false);
  const [score, setScore] = useState(null);

  // Define shouldShowCorrect at component level
  const shouldShowCorrect = showAnswers || score;

  const handleAnswerSelect = (questionIndex, selectedAnswer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionIndex]: selectedAnswer
    }));
  };

  const calculateScore = () => {
    let correct = 0;
    quizData.quiz.forEach((question, index) => {
      if (userAnswers[index] === question.correct_answer) {
        correct++;
      }
    });
    const percentage = Math.round((correct / quizData.quiz.length) * 100);
    setScore({ correct, total: quizData.quiz.length, percentage });
    setShowAnswers(true);
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyIcon = (difficulty) => {
    switch (difficulty) {
      case 'easy': return <CheckCircle className="h-4 w-4" />;
      case 'medium': return <AlertTriangle className="h-4 w-4" />;
      case 'hard': return <XCircle className="h-4 w-4" />;
      default: return <Target className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{quizData.title}</h1>
          <p className="text-gray-600 mt-2">Generated from Wikipedia article</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={onNewQuiz}
            className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <RotateCcw className="h-4 w-4" />
            <span>New Quiz</span>
          </button>
          <Link
            to="/history"
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <BookOpen className="h-4 w-4" />
            <span>View History</span>
          </Link>
        </div>
      </div>

      {/* Article Summary */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Article Summary</h2>
        <p className="text-gray-700 leading-relaxed">{quizData.summary}</p>
      </div>

      {/* Key Entities */}
      {quizData.key_entities && Object.keys(quizData.key_entities).length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Key Information</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(quizData.key_entities).map(([category, items]) => (
              <div key={category} className="space-y-2">
                <div className="flex items-center space-x-2">
                  {category === 'people' && <Users className="h-5 w-5 text-blue-600" />}
                  {category === 'organizations' && <Building className="h-5 w-5 text-green-600" />}
                  {category === 'locations' && <MapPin className="h-5 w-5 text-red-600" />}
                  {category === 'concepts' && <Lightbulb className="h-5 w-5 text-purple-600" />}
                  <h3 className="font-medium text-gray-900 capitalize">{category}</h3>
                </div>
                <div className="space-y-1">
                  {items.slice(0, 3).map((item, index) => (
                    <div key={index} className="text-sm text-gray-600 bg-gray-50 px-2 py-1 rounded">
                      {item}
                    </div>
                  ))}
                  {items.length > 3 && (
                    <div className="text-xs text-gray-500">+{items.length - 3} more</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quiz Mode Toggle */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Quiz Questions</h2>
          <div className="flex space-x-3">
            <button
              onClick={() => {
                setQuizMode(!quizMode);
                setShowAnswers(false);
                setUserAnswers({});
                setScore(null);
              }}
              className={`px-4 py-2 rounded-lg transition-colors ${
                quizMode 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {quizMode ? 'Exit Quiz Mode' : 'Take Quiz'}
            </button>
            {quizMode && (
              <button
                onClick={calculateScore}
                disabled={Object.keys(userAnswers).length !== quizData.quiz.length}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                Submit Quiz
              </button>
            )}
          </div>
        </div>

        {/* Score Display */}
        {score && (
          <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Quiz Complete!</h3>
              <p className="text-lg text-gray-700">
                You scored {score.correct} out of {score.total} ({score.percentage}%)
              </p>
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${score.percentage}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quiz Questions */}
        <div className="space-y-6">
          {quizData.quiz.map((question, index) => (
            <div key={index} className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900 flex-1">
                  {index + 1}. {question.question}
                </h3>
                <div className={`flex items-center space-x-1 px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(question.difficulty || 'medium')}`}>
                  {getDifficultyIcon(question.difficulty || 'medium')}
                  <span className="capitalize">{question.difficulty || 'medium'}</span>
                </div>
              </div>

              <div className="space-y-3">
                {question.options.map((option, optionIndex) => {
                  const isSelected = userAnswers[index] === optionIndex;
                  const isCorrect = optionIndex === question.correct_answer;
                  
                  let optionClass = "w-full text-left p-4 border rounded-lg transition-all duration-200 ";
                  
                  if (quizMode && !shouldShowCorrect) {
                    optionClass += isSelected 
                      ? "border-blue-500 bg-blue-50 text-blue-900" 
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50";
                  } else if (shouldShowCorrect) {
                    if (isCorrect) {
                      optionClass += "border-green-500 bg-green-50 text-green-900";
                    } else if (isSelected && !isCorrect) {
                      optionClass += "border-red-500 bg-red-50 text-red-900";
                    } else {
                      optionClass += "border-gray-200 bg-gray-50 text-gray-700";
                    }
                  } else {
                    optionClass += "border-gray-200 hover:border-gray-300 hover:bg-gray-50";
                  }

                  return (
                    <button
                      key={optionIndex}
                      onClick={() => quizMode && !shouldShowCorrect && handleAnswerSelect(index, optionIndex)}
                      disabled={!quizMode || shouldShowCorrect}
                      className={optionClass}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium">
                          {String.fromCharCode(65 + optionIndex)}. {option}
                        </span>
                        {shouldShowCorrect && isCorrect && (
                          <CheckCircle className="h-5 w-5 text-green-600" />
                        )}
                        {shouldShowCorrect && isSelected && !isCorrect && (
                          <XCircle className="h-5 w-5 text-red-600" />
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>

              {shouldShowCorrect && (
                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h4 className="font-medium text-blue-900 mb-2">Explanation:</h4>
                  <p className="text-blue-800">{question.explanation || 'This is the correct answer based on the Wikipedia article content.'}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Related Topics */}
      {quizData.related_topics && quizData.related_topics.length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Related Topics</h2>
          <div className="flex flex-wrap gap-3">
            {quizData.related_topics.map((topic, index) => (
              <span
                key={index}
                className="px-4 py-2 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 rounded-full text-sm font-medium hover:from-blue-200 hover:to-purple-200 transition-colors cursor-pointer"
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizDisplay;
