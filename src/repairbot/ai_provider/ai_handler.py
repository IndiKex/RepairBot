from repairbot.ai_provider.ai_provider import AIProvider


class AIHandler:
    def __init__(self):
        self.ai_provider = AIProvider()

    def query(self, question: str) -> str:
        interaction = self.ai_provider.query(question)
        return self.ai_provider.interaction2answer(interaction)
