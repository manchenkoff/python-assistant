import random
from typing import List

from voice_assistant.assistant import HandlerInterface, AssistantInterface


class DefaultHandler(HandlerInterface):
    error_messages: List[str]

    def __init__(self, assistant: AssistantInterface):
        super().__init__(assistant)

        self.error_messages = [
            "Не поняла вас",
            "Кажется, я не знаю такой команды",
            "Я не могу помочь с этим"
        ]

    def check_context(self, context: str) -> bool:
        return True

    async def handle_context(self, context: str):
        await self.assistant.say(random.choice(self.error_messages))
