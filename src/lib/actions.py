import random
from typing import List

from src.lib.assistant import ActionInterface, AssistantInterface


class DefaultAction(ActionInterface):
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


class HelloAction(ActionInterface):
    def check_context(self, context: str) -> bool:
        return "привет" in context

    async def handle_context(self, context: str):
        await self.assistant.say("Привет!")


class ByeAction(ActionInterface):
    def check_context(self, context: str) -> bool:
        return any(match in context for match in ("пока", "прощай", "закройся"))

    async def handle_context(self, context: str):
        await self.assistant.say("Пока-пока!")


class NameAction(ActionInterface):
    def check_context(self, context: str) -> bool:
        return "как тебя зовут" in context

    async def handle_context(self, context: str):
        await self.assistant.say("Точно хочешь знать?")

        response = await self.assistant.listen()

        if "да" in response:
            await self.assistant.say(f"Меня зовут {self.assistant.get_name()}")
        else:
            await self.assistant.say("Я знала, что передумаешь")
