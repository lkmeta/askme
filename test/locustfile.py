from locust import HttpUser, TaskSet, task, between
import random

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Load the expected token from environment variables
EXPECTED_TOKEN = os.getenv("API_TOKEN")

# Updated sample user questions for testing
test_questions = [
    "How can I update my username?",
    "What's the process for recovering a forgotten username?",
    "How do I switch to dark mode in the application?",
    "Is it possible to link multiple email addresses to my account?",
    "How can I export my user data from the platform?",
    "What are the requirements for creating a secure passphrase?",
    "How do I enable biometric login for the mobile app?",
    "What steps should I take to permanently delete my account?",
    "What should I do if I suspect unauthorized access to my account?",
    "How can I manage the frequency of email digests I receive?",
]


class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        # Test the root endpoint
        self.client.get("/")

    @task(2)
    def ask_question(self):
        # Pick a random question from the list
        question = random.choice(test_questions)
        self.client.post(
            "/ask-question",
            json={"user_question": question},
            headers={"Authorization": "Bearer " + EXPECTED_TOKEN},
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(
        1, 5
    )  # Simulates a wait time between 1 and 5 seconds between tasks
