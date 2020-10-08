import asyncio
import os
import sys
from asyncio import AbstractEventLoop

from asyncqt import QEventLoop
from dotenv import load_dotenv
from PySide2.QtWidgets import QApplication

from voice_assistant.container import Container
from voice_assistant.window import MainWindow


def init_environment():
    env_path = '../.env'

    if getattr(sys, 'frozen', False):
        env_path = os.path.join(os.path.dirname(sys.executable), env_path)

    load_dotenv(env_path)


def start_application():
    app = QApplication(sys.argv)

    event_loop: AbstractEventLoop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    container = Container()

    window = MainWindow(container.assistant)

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
    init_environment()
    start_application()
