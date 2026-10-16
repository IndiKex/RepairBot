import os

from dotenv import load_dotenv
from google import genai


class AIProvider:
    def __init__(self):
        load_dotenv("secrets.env")
        api_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.5-flash"

    def query(self, question: str):
        interaction = self.client.interactions.create(model=self.model, input=question)
        return interaction

    def interaction2answer(self, interaction) -> str:
        for step in interaction.steps:
            if step.type == "model_output":
                for content_block in step.content:
                    if content_block.type == "text":
                        return content_block.text
        return ""
