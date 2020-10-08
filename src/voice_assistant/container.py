import os

from voice_assistant.actions import *
from voice_assistant.assistant import Assistant, AssistantInterface
from voice_assistant.speech import Speech, SpeechInterface


class Container:
    @property
    def speech(self) -> SpeechInterface:
        return Speech(
            os.getenv("APP_LANGUAGE"),
            os.getenv("ASSISTANT_METHOD")
        )

    @property
    def assistant_actions(self):
        return [
            HelloAction,
            ByeAction,
            NameAction,
            DefaultAction,  # Always last
        ]

    @property
    def assistant(self) -> AssistantInterface:
        return Assistant(
            os.getenv("ASSISTANT_NAME"),
            os.getenv("APP_LANGUAGE"),
            self.speech,
            self.assistant_actions
        )
