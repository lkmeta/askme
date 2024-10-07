from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from app.services.config import settings
from app.utils.logger import logger


# A client to interact with OpenAI's ChatGPT model
class OpenAIClient:
    def __init__(self):
        # Initialize the OpenAI chat model with API key and model name
        self.chat_model = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4o",
            temperature=0.7,
        )

    def get_answer(self, user_question: str) -> str:
        """
        Send a user question to OpenAI's chat model and return the response.
        """
        try:
            logger.info(f"Sending question to OpenAI API: {user_question}")
            messages = [
                HumanMessage(content=user_question)
            ]  # Wrap the question in a message
            response = self.chat_model(messages)  # Get response from OpenAI chat model
            answer = response.content.strip()  # Extract and clean the response content
            logger.info("Received answer from OpenAI API.")
            return answer
        except Exception as e:
            # Log and return an error message in case of failure
            logger.error(f"Error communicating with OpenAI API: {e}")
            return "An error occurred while fetching the answer from OpenAI API."


# Instantiate the OpenAI client for use in other modules
openai_client = OpenAIClient()
