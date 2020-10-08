from abc import ABC, abstractmethod
from typing import List, Optional

from voice_assistant.speech import SpeechInterface


class AssistantInterface(ABC):
    @abstractmethod
    async def handle(self, question: Optional[str] = None) -> str:
        raise NotImplementedError

    @abstractmethod
    async def listen(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def say(self, text: str) -> None:
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError

    def on_wake(self):
        pass

    def on_sleep(self):
        pass

    def on_assistant_listen(self):
        pass

    def on_user_message(self, text: str):
        pass

    def on_assistant_message(self, text: str):
        pass


class HandlerInterface(ABC):
    assistant: AssistantInterface

    def __init__(self, assistant: AssistantInterface):
        self.assistant = assistant

    @abstractmethod
    def check_context(self, context: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def handle_context(self, context: str):
        raise NotImplementedError


class Assistant(AssistantInterface):
    name: str
    language: str
    speech: SpeechInterface
    handlers: List[HandlerInterface]

    def __init__(self, name: str, language: str, speech_service: SpeechInterface, handlers: List[type]):
        self.name = name
        self.language = language
        self.speech = speech_service
        self._bind_handlers(handlers)

    def _bind_handlers(self, actions: List[type]):
        self.handlers = [x(self) for x in actions]

    def get_name(self) -> str:
        return self.name

    async def listen(self) -> Optional[str]:
        self.on_assistant_listen()
        user_text = await self.speech.listen()

        if user_text:
            self.on_user_message(user_text)

        return user_text

    async def say(self, text: str) -> None:
        self.on_assistant_message(text)
        await self.speech.say(text)

    async def handle(self, question: Optional[str] = None):
        self.on_wake()

        if question:
            await self.say(question)

        user_text = await self.listen()

        if user_text:
            await self._process_message(user_text)

        self.on_sleep()

    async def _process_message(self, message: str):
        context = message.strip().lower()

        for action in self.handlers:
            if action.check_context(context):
                await action.handle_context(context)
                break
