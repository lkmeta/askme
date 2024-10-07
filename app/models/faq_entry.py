from pydantic import BaseModel


# Structure for a FAQ entry with a question and an answer
class FAQEntry(BaseModel):
    question: str  # The question in the FAQ
    answer: str  # The corresponding answer in the FAQ
