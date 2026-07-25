import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Search, Loader2, ExternalLink, CheckCircle, AlertCircle } from 'lucide-react';
import QuizDisplay from './QuizDisplay';
import { generateQuiz, validateUrl } from '../services/api';

const GenerateQuiz = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [validating, setValidating] = useState(false);
  const [quizData, setQuizData] = useState(null);
  const [error, setError] = useState('');
  const [urlValid, setUrlValid] = useState(null);

  // Validate URL against the backend, trimming whitespace first
  const validateUrlValue = useCallback(async (rawUrl) => {
    const trimmed = rawUrl.trim();
    if (!trimmed) {
      setUrlValid(null);
      setValidating(false);
      return;
    }
    setValidating(true);
    try {
      const response = await validateUrl(trimmed);
      setUrlValid(response.valid);
      if (!response.valid) {
        setError('Please enter a valid Wikipedia article URL. Make sure it starts with https://en.wikipedia.org/wiki/');
      }
    } catch (err) {
      setUrlValid(false);
      setError(`Failed to validate URL: ${err.message}`);
    } finally {
      setValidating(false);
    }
  }, []);

  // Debounce validation: fires 500ms after the user stops typing
  useEffect(() => {
    setUrlValid(null);
    setError('');
    if (!url.trim()) return;
    setValidating(true);
    const timer = setTimeout(() => {
      validateUrlValue(url);
    }, 500);
    return () => clearTimeout(timer);
  }, [url, validateUrlValue]);

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
    setQuizData(null);
  };

  // Called when user clicks one of the example URL buttons
  const handleExampleClick = (exampleUrl) => {
    setUrl(exampleUrl);
    setQuizData(null);
    setError('');
  };

  const handleGenerateQuiz = async (e) => {
    e.preventDefault();
    if (!url.trim() || !urlValid) return;
    const trimmedUrl = url.trim();

    setLoading(true);
    setError('');
    setQuizData(null);

    try {
      const response = await generateQuiz(trimmedUrl);
      setQuizData(response);
    } catch (err) {
      const detail = err.message || '';
      const isRateLimit = detail.toLowerCase().includes('rate limit') || detail.includes('429') || detail.toLowerCase().includes('quota');
      setError(isRateLimit
        ? '⏳ Gemini API rate limit reached. Please wait 1–2 minutes and try again.'
        : detail || 'Failed to generate quiz. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewQuiz = () => {
    setUrl('');
    setQuizData(null);
    setError('');
    setUrlValid(null);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {!quizData ? (
        <div className="space-y-8">
          {/* Header */}
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Generate AI-Powered Quiz
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Enter a Wikipedia article URL and let our AI generate a comprehensive quiz 
              with questions, answers, and explanations.
            </p>
          </div>

          {/* URL Input Form */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <form onSubmit={handleGenerateQuiz} className="space-y-6">
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  Wikipedia Article URL
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    id="url"
                    value={url}
                    onChange={handleUrlChange}
                    placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
                    className={`block w-full pl-10 pr-12 py-4 border rounded-xl text-lg transition-all duration-200 ${
                      urlValid === false 
                        ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                        : urlValid === true 
                        ? 'border-green-300 focus:border-green-500 focus:ring-green-500'
                        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                    } focus:ring-2 focus:ring-opacity-50`}
                    disabled={loading}
                  />
                  {validating && (
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                    </div>
                  )}
                  {!validating && urlValid === true && (
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                  )}
                  {!validating && urlValid === false && (
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <AlertCircle className="h-5 w-5 text-red-500" />
                    </div>
                  )}
                </div>
                
                {urlValid === true && (
                  <p className="mt-2 text-sm text-green-600 flex items-center">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    Valid Wikipedia URL detected
                  </p>
                )}
                
                {urlValid === false && (
                  <p className="mt-2 text-sm text-red-600 flex items-center">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    Please enter a valid Wikipedia article URL
                  </p>
                )}
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={!url.trim() || !urlValid || loading}
                className={`w-full py-4 px-6 rounded-xl text-lg font-medium transition-all duration-200 ${
                  !url.trim() || !urlValid || loading
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'btn-primary text-white hover:shadow-lg transform hover:-translate-y-0.5'
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                    Generating Quiz...
                  </div>
                ) : (
                  'Generate Quiz'
                )}
              </button>
            </form>
          </div>

          {/* Example URLs */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Try these examples:</h3>
            <div className="grid md:grid-cols-2 gap-4">
              {[
                {
                  title: "Alan Turing",
                  url: "https://en.wikipedia.org/wiki/Alan_Turing",
                  description: "British mathematician and computer scientist"
                },
                {
                  title: "Machine Learning",
                  url: "https://en.wikipedia.org/wiki/Machine_learning",
                  description: "Field of artificial intelligence"
                },
                {
                  title: "Photosynthesis",
                  url: "https://en.wikipedia.org/wiki/Photosynthesis",
                  description: "Process by which plants convert light to energy"
                },
                {
                  title: "Renaissance",
                  url: "https://en.wikipedia.org/wiki/Renaissance",
                  description: "Cultural movement in European history"
                }
              ].map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example.url)}
                  className="text-left p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 group"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 group-hover:text-blue-700">
                        {example.title}
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">{example.description}</p>
                    </div>
                    <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-blue-500" />
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <QuizDisplay quizData={quizData} onNewQuiz={handleNewQuiz} />
      )}
    </div>
  );
};

export default GenerateQuiz;
