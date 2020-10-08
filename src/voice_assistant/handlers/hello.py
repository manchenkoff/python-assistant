from voice_assistant.assistant import HandlerInterface


class HelloHandler(HandlerInterface):
    def check_context(self, context: str) -> bool:
        return "привет" in context

    async def handle_context(self, context: str):
        await self.assistant.say("Привет!")
