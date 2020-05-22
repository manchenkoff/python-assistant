import os

from src.lib.actions import *
from src.lib.assistant import AssistantInterface, Assistant
from src.lib.speech import SpeechInterface, Speech


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
