from voice_assistant.assistant import HandlerInterface


class ByeHandler(HandlerInterface):
    def check_context(self, context: str) -> bool:
        return any(match in context for match in ("пока", "прощай", "закройся"))

    async def handle_context(self, context: str):
        await self.assistant.say("Пока-пока!")
