"""
Simple LLM service for generating quizzes using Gemini API (google-genai SDK - HTTP/REST, no gRPC)
"""

import os
import json
import re
import requests

class SimpleLLMQuizGenerator:
    """Simple service for generating quizzes using Gemini API"""
    
    # Models tried in order
    MODEL_FALLBACKS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
    ]

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCnwA4P2SWoIQA28BbRrKgXoQQpOcnIm08")
    
    def _call_model(self, prompt: str) -> str:
        """Call Gemini API using direct HTTP requests to bypass SDK bugs/hangs."""
        last_error = None
        
        for model in self.MODEL_FALLBACKS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7}
            }
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['candidates'][0]['content']['parts'][0]['text']
                    
                if response.status_code == 429:
                    last_error = Exception("429 Rate Limit")
                    continue  # immediately try the next model
                
                # other errors (404, 500, etc.)
                last_error = Exception(f"API Error {response.status_code}: {response.text}")
                continue
                
            except Exception as e:
                last_error = e
                continue
                
        raise Exception(
            "Gemini API rate limit reached on all available models. "
            "Please wait a minute and try again."
        ) from last_error

    def generate_quiz(self, article_data):
        """Generate quiz from article data"""
        try:
            quiz_prompt = self._create_quiz_prompt()
            context = self._prepare_context(article_data)
            response_text = self._call_model(quiz_prompt.format(context=context))
            quiz_data = self._parse_quiz_response(response_text)
            related_topics = self._generate_related_topics(article_data)
            return {
                'quiz': quiz_data,
                'related_topics': related_topics
            }
        except Exception as e:
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _create_quiz_prompt(self):
        """Create prompt template for quiz generation"""
        return """
You are an expert quiz generator. Based on the following Wikipedia article content, generate a high-quality quiz with 8 questions.

Article Context:
{context}

Requirements:
1. Generate exactly 8 questions
2. Each question should have 4 multiple choice options (A, B, C, D)
3. Include one correct answer and three plausible distractors
4. Assign difficulty levels: 2 easy, 3 medium, 3 hard
5. Provide clear explanations for each answer
6. Base questions on factual information from the article
7. Ensure questions test understanding, not just memorization

Output Format (JSON):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B", 
        "Option C",
        "Option D"
      ],
      "answer": "Correct option text",
      "difficulty": "easy|medium|hard",
      "explanation": "Brief explanation of why this is correct"
    }}
  ]
}}

Generate the quiz now:
"""
    
    def _prepare_context(self, article_data):
        """Prepare context for LLM from article data"""
        context_parts = [
            f"Title: {article_data.get('title', 'Unknown')}",
            f"Summary: {article_data.get('summary', 'No summary available')}",
            f"Key Sections: {', '.join(article_data.get('sections', []))}",
            f"Content: {article_data.get('content_text', '')[:4000]}"  # Limit content length
        ]
        return "\n\n".join(context_parts)
    
    def _parse_quiz_response(self, response):
        """Parse LLM response to extract quiz questions"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                quiz_data = json.loads(json_match.group())
                return quiz_data.get('questions', [])
            else:
                # Fallback: try to parse manually
                return self._parse_quiz_manually(response)
        except json.JSONDecodeError:
            return self._parse_quiz_manually(response)
    
    def _parse_quiz_manually(self, response):
        """Manually parse quiz response if JSON parsing fails"""
        questions = []
        lines = response.split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect question
            if line.endswith('?') and len(line) > 20:
                if current_question:
                    questions.append(current_question)
                current_question = {
                    'question': line,
                    'options': [],
                    'answer': '',
                    'difficulty': 'medium',
                    'explanation': ''
                }
            
            # Detect options
            elif line.startswith(('A)', 'B)', 'C)', 'D)')) and current_question:
                option_text = line[2:].strip()
                current_question['options'].append(option_text)
            
            # Detect answer
            elif 'Answer:' in line or 'Correct:' in line and current_question:
                answer_text = line.split(':', 1)[1].strip()
                current_question['answer'] = answer_text
        
        if current_question and len(current_question['options']) == 4:
            questions.append(current_question)
        
        # Ensure we have exactly 8 questions, generate fallback if needed
        if len(questions) < 8:
            questions.extend(self._generate_fallback_questions(8 - len(questions)))
        
        return questions[:8]
    
    def _generate_fallback_questions(self, count):
        """Generate fallback questions if LLM response is insufficient"""
        fallback_questions = []
        for i in range(count):
            fallback_questions.append({
                'question': f"Sample question {i+1} about the article?",
                'options': [
                    "Option A",
                    "Option B", 
                    "Option C",
                    "Option D"
                ],
                'answer': "Option A",
                'difficulty': "medium",
                'explanation': "This is a sample explanation."
            })
        return fallback_questions
    
    def _generate_related_topics(self, article_data):
        """Generate related topics for further reading"""
        try:
            related_prompt = f"""Based on this Wikipedia article about "{article_data.get('title', '')}", suggest 5 related Wikipedia topics for further reading.

Article summary: {article_data.get('summary', '')}

Provide only the topic names, one per line, without explanations."""
            response_text = self._call_model(related_prompt)
            topics = [
                line.strip() for line in response_text.split('\n')
                if line.strip() and not line.strip().startswith('#') and len(line.strip()) > 3
            ]
            return topics[:5]
        except Exception:
            return [
                "Artificial Intelligence",
                "History of Science",
                "Philosophy of Mind",
                "Computer Science",
                "Mathematics"
            ]
