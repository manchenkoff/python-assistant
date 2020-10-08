import asyncio
import os
import sys
from asyncio import AbstractEventLoop

from asyncqt import QEventLoop
from dotenv import load_dotenv
from PySide2.QtWidgets import QApplication

from voice_assistant.assistant import Assistant
from voice_assistant.handlers import *
from voice_assistant.interface.window import MainWindow
from voice_assistant.speech import Speech


def init_environment():
    env_path = '../.env'

    if getattr(sys, 'frozen', False):
        env_path = os.path.join(os.path.dirname(sys.executable), env_path)

    load_dotenv(env_path)


def create_assistant() -> Assistant:
    handlers = [
        HelloHandler,
        ByeHandler,
        NameHandler,
        DefaultHandler,  # Always last
    ]

    speech_system = Speech(
        os.getenv("APP_LANGUAGE"),
        os.getenv("ASSISTANT_METHOD")
    )

    return Assistant(
        os.getenv("ASSISTANT_NAME"),
        os.getenv("APP_LANGUAGE"),
        speech_system,
        handlers
    )


def run_app():
    init_environment()

    app = QApplication(sys.argv)

    event_loop: AbstractEventLoop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    window = MainWindow(create_assistant())

    try:
        with event_loop:
            event_loop.create_task(
                window.start()
            )
            event_loop.run_forever()
    except KeyboardInterrupt:
        print("App terminated")
    finally:
        if not event_loop.is_closed():
            event_loop.close()


if __name__ == '__main__':
    run_app()
