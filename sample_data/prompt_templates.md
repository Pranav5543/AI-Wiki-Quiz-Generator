# LangChain Prompt Templates

This document contains the prompt templates used for generating quizzes and related topics using the Gemini API via LangChain.

## Quiz Generation Prompt

```
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
{
  "questions": [
    {
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
    }
  ]
}

Generate the quiz now:
```

## Related Topics Generation Prompt

```
Based on this Wikipedia article about "{article_title}", suggest 5 related Wikipedia topics that would be interesting for further reading.

Article summary: {article_summary}

Provide only the topic names, one per line, without explanations.
```

## Prompt Optimization Features

### 1. Context Preparation
- Article title and summary
- Key sections and entities
- Main content text (limited to 4000 characters)
- Structured information extraction

### 2. Difficulty Distribution
- **Easy (2 questions)**: Basic facts, definitions, simple concepts
- **Medium (3 questions)**: Application of concepts, relationships, moderate complexity
- **Hard (3 questions)**: Deep understanding, analysis, complex relationships

### 3. Question Quality Guidelines
- Questions should test comprehension, not just memorization
- Options should be plausible and well-distributed
- Avoid trick questions or overly obscure details
- Focus on important concepts and key information

### 4. Explanation Requirements
- Clear reasoning for correct answers
- Reference to specific article sections when possible
- Educational value for learning
- Concise but informative

## Error Handling and Fallbacks

### JSON Parsing Fallback
If the LLM response cannot be parsed as JSON, the system attempts manual parsing:
1. Extract questions by looking for question patterns
2. Identify options by A), B), C), D) patterns
3. Find answers by "Answer:" or "Correct:" patterns
4. Generate fallback questions if insufficient content

### Fallback Question Generation
If the LLM fails to generate enough questions, the system creates sample questions:
```python
def _generate_fallback_questions(self, count: int) -> List[Dict]:
    """Generate fallback questions if LLM response is insufficient"""
    fallback_questions = []
    for i in range(count):
        fallback_questions.append({
            'question': f"Sample question {i+1} about the article?",
            'options': ["Option A", "Option B", "Option C", "Option D"],
            'answer': "Option A",
            'difficulty': "medium",
            'explanation': "This is a sample explanation."
        })
    return fallback_questions
```

## Performance Optimization

### 1. Content Length Management
- Limit article content to 4000 characters for LLM processing
- Extract most relevant sections and entities
- Prioritize main content over references and citations

### 2. Response Validation
- Validate JSON structure before processing
- Check for required fields in each question
- Ensure proper difficulty distribution
- Verify option completeness

### 3. Caching Strategy
- Store generated quizzes in database
- Prevent duplicate processing of same URLs
- Cache related topics for similar articles
- Implement TTL for cached responses

## Usage Examples

### Basic Quiz Generation
```python
llm_service = LLMQuizGenerator()
quiz_data = llm_service.generate_quiz(article_data)
```

### Related Topics Generation
```python
related_topics = llm_service._generate_related_topics(article_data)
```

### Error Handling
```python
try:
    quiz_data = llm_service.generate_quiz(article_data)
except Exception as e:
    # Log error and provide fallback
    logger.error(f"LLM generation failed: {str(e)}")
    quiz_data = generate_fallback_quiz(article_data)
```
