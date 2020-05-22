import asyncio
import tempfile

from PySide2.QtCore import QFile
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow
from playsound import playsound

from src.form import Ui_window
from src.lib.assistant import AssistantInterface
from src.lib.decorators import async_function
from src.resources import qInitResources


class MainWindow(QMainWindow, Ui_window):
    assistant: AssistantInterface

    def __init__(self, assistant: AssistantInterface):
        super().__init__()
        qInitResources()
        self.setupUi(self)
        self.assistant = assistant
        self.init_handlers()

    def init_handlers(self):
        self.recognize_button.pressed.connect(self.start_recognition)
        self.assistant.on_wake = self.on_assistant_started
        self.assistant.on_sleep = self.on_assistant_finished
        self.assistant.on_assistant_listen = self.on_recognize_started
        self.assistant.on_user_message = self.on_user_text
        self.assistant.on_assistant_message = self.on_assistant_text

    def on_assistant_started(self):
        self.recognize_button.setEnabled(False)

    def on_assistant_finished(self):
        self.recognize_button.setEnabled(True)
        self.recognize_button.setText("Recognize")

    def on_recognize_started(self):
        self.click_sound_concurrently()
        self.recognize_button.setText("Listening...")

    def on_user_text(self, user_text: str):
        self.recognize_button.setText("Processing...")
        self.append_message(f"[You] {user_text}")

    def on_assistant_text(self, assistant_answer: str):
        self.append_message(assistant_answer)

    def append_message(self, message: str):
        self.text_box.appendPlainText(f"{message}\n")

    def start_recognition(self):
        coroutine = self.assistant.handle()
        asyncio.create_task(coroutine)

    @async_function
    def click_sound_concurrently(self):
        resource_path = ":/sounds/click.mp3"

        file = QFile(resource_path)
        file.open(QFile.ReadOnly)

        byte_array = file.readAll()

        file.close()

        with tempfile.NamedTemporaryFile("wb", delete=True) as temp:
            temp.write(byte_array.data())
            playsound(temp.name)

    def closeEvent(self, event: QCloseEvent):
        for task in asyncio.tasks.Task.all_tasks():
            task.cancel()

    async def start(self):
        self.show()
