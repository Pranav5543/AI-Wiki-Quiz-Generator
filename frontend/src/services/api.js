/**
 * API service for communicating with the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  console.log('API Request:', { url, config });

  try {
    const response = await fetch(url, config);
    console.log('API Response:', { status: response.status, ok: response.ok });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('API Error:', errorData);
      throw new ApiError(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status
      );
    }

    const data = await response.json();
    console.log('API Success:', data);
    return data;
  } catch (error) {
    console.error('API Request Error:', error);
    if (error instanceof ApiError) {
      throw error;
    }
    // Check if it's a network error
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new ApiError('Network error: Unable to connect to the server. Please check if the backend is running.', 0);
    }
    throw new ApiError(`Network error: ${error.message}`, 0);
  }
};

// Quiz generation endpoints
export const generateQuiz = async (url) => {
  return apiRequest('/quiz/generate', {
    method: 'POST',
    body: JSON.stringify({ url }),
  });
};

export const validateUrl = async (url) => {
  return apiRequest('/quiz/validate-url', {
    method: 'POST',
    body: JSON.stringify({ url }),
  });
};

export const getQuizById = async (id) => {
  return apiRequest(`/quiz/${id}`);
};

// History endpoints
export const getQuizHistory = async (page = 1, limit = 10) => {
  return apiRequest(`/history/?page=${page}&limit=${limit}`);
};

export const getQuizDetail = async (id) => {
  return apiRequest(`/history/${id}`);
};

export const deleteQuiz = async (id) => {
  return apiRequest(`/history/${id}`, {
    method: 'DELETE',
  });
};

export const getStats = async () => {
  return apiRequest('/history/stats/summary');
};

// Health check
export const healthCheck = async () => {
  return apiRequest('/health');
};

export default {
  generateQuiz,
  validateUrl,
  getQuizById,
  getQuizHistory,
  getQuizDetail,
  deleteQuiz,
  getStats,
  healthCheck,
};
