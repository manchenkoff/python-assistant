from voice_assistant.assistant import HandlerInterface


class NameHandler(HandlerInterface):
    def check_context(self, context: str) -> bool:
        return "как тебя зовут" in context

    async def handle_context(self, context: str):
        await self.assistant.say("Точно хочешь знать?")

        response = await self.assistant.listen()

        if "да" in response:
            await self.assistant.say(f"Меня зовут {self.assistant.get_name()}")
        else:
            await self.assistant.say("Я знала, что передумаешь")
