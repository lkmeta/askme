from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from app.services.config import settings
from app.utils.logger import logger


class OpenAIClient:
    def __init__(self):
        self.chat_model = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.7,
        )

    def get_answer(self, user_question: str) -> str:
        try:
            logger.info(f"Sending question to OpenAI API: {user_question}")
            messages = [HumanMessage(content=user_question)]
            response = self.chat_model(messages)
            answer = response.content.strip()
            logger.info("Received answer from OpenAI API.")
            return answer
        except Exception as e:
            logger.error(f"Error communicating with OpenAI API: {e}")
            return "An error occurred while fetching the answer from OpenAI API."


openai_client = OpenAIClient()
