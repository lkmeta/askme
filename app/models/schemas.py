from pydantic import BaseModel


# Model representing a user's request containing a question
class QuestionRequest(BaseModel):
    question: str  # The user's question to be processed


# Model representing the response with an answer
class AnswerResponse(BaseModel):
    question: str  # The original question asked by the user
    answer: str  # The answer to the question
    source: str  # Source of the answer ('faq' or 'openai')
    similarity_score: float = None  # Similarity score if applicable (optional)
