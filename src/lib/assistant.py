from abc import abstractmethod, ABC
from typing import Union, List

from src.lib.speech import SpeechInterface


class AssistantInterface(ABC):
    @abstractmethod
    async def handle(self, question: Union[str, None] = None) -> str:
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


class ActionInterface(ABC):
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
    _name: str
    _language: str
    _voice: SpeechInterface
    _actions: List[ActionInterface]

    def __init__(self, name: str, language: str, speech_service: SpeechInterface, action_classes: List[type]):
        self._name = name
        self._language = language
        self._voice = speech_service
        self._bind_actions(action_classes)

    def _bind_actions(self, actions: List[type]):
        self._actions = [x(self) for x in actions]

    def get_name(self) -> str:
        return self._name

    async def listen(self) -> Union[str, None]:
        self.on_assistant_listen()
        user_text = await self._voice.listen()

        if user_text:
            self.on_user_message(user_text)

        return user_text

    async def say(self, text: str) -> None:
        signed_text = f"[{self._name}] {text}"
        self.on_assistant_message(signed_text)
        await self._voice.say(text)

    async def handle(self, question: Union[str, None] = None) -> None:
        self.on_wake()

        if question:
            await self.say(question)

        user_text = await self.listen()

        if user_text:
            await self._process_message(user_text)

        self.on_sleep()

    async def _process_message(self, message: str):
        context = message.strip().lower()

        for action in self._actions:
            if action.check_context(context):
                await action.handle_context(context)
                break
