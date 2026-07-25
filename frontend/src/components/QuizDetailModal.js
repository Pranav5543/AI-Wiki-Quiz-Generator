import React, { useState } from 'react';
import { X, CheckCircle, XCircle, Target, AlertTriangle } from 'lucide-react';

const QuizDetailModal = ({ quiz, onClose }) => {
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
    quiz.quiz.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correct++;
      }
    });
    const percentage = Math.round((correct / quiz.quiz.length) * 100);
    setScore({ correct, total: quiz.quiz.length, percentage });
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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden modal-enter">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{quiz.title}</h2>
            <p className="text-gray-600">Quiz Details</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6">
          {/* Article Summary */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Article Summary</h3>
            <p className="text-gray-700 leading-relaxed">{quiz.summary}</p>
          </div>

          {/* Quiz Mode Toggle */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Quiz Questions</h3>
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
                    disabled={Object.keys(userAnswers).length !== quiz.quiz.length}
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
                  <h4 className="text-xl font-bold text-gray-900 mb-2">Quiz Complete!</h4>
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
            <div className="space-y-4">
              {quiz.quiz.map((question, index) => (
                <div key={index} className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="text-base font-medium text-gray-900 flex-1">
                      {index + 1}. {question.question}
                    </h4>
                    <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(question.difficulty)}`}>
                      {getDifficultyIcon(question.difficulty)}
                      <span className="capitalize">{question.difficulty}</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    {question.options.map((option, optionIndex) => {
                      const isSelected = userAnswers[index] === option;
                      const isCorrect = option === question.answer;
                      
                      let optionClass = "w-full text-left p-3 border rounded-lg transition-all duration-200 text-sm ";
                      
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
                          onClick={() => quizMode && !shouldShowCorrect && handleAnswerSelect(index, option)}
                          disabled={!quizMode || shouldShowCorrect}
                          className={optionClass}
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-medium">
                              {String.fromCharCode(65 + optionIndex)}. {option}
                            </span>
                            {shouldShowCorrect && isCorrect && (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            )}
                            {shouldShowCorrect && isSelected && !isCorrect && (
                              <XCircle className="h-4 w-4 text-red-600" />
                            )}
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {shouldShowCorrect && (
                    <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <h5 className="font-medium text-blue-900 mb-1">Explanation:</h5>
                      <p className="text-blue-800 text-sm">{question.explanation}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Related Topics */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Related Topics</h3>
            <div className="flex flex-wrap gap-2">
              {quiz.related_topics.map((topic, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 rounded-full text-sm font-medium"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizDetailModal;
