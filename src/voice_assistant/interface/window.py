import asyncio
import tempfile

from playsound import playsound
from PySide2.QtCore import QFile, QMetaObject, QSize, Qt
from PySide2.QtGui import QCloseEvent, QFont
from PySide2.QtWidgets import QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from voice_assistant.assistant import AssistantInterface
from voice_assistant.decorators import async_function
from voice_assistant.interface.resources import qInitResources


class MainWindow(QMainWindow):
    font: QFont
    vertical_layout: QVBoxLayout
    central_widget: QWidget
    text_box: QPlainTextEdit
    recognize_button: QPushButton

    assistant: AssistantInterface

    def __init__(self, assistant: AssistantInterface):
        super().__init__()

        qInitResources()

        self.assistant = assistant

        self.build_layout()
        self.init_handlers()

    def build_layout(self):
        self.setup_window()
        self.setup_styles()
        self.setup_font()

        self.build_central_widget()
        self.build_vertical_layout()
        self.build_text_box()
        self.build_recognize_button()

        QMetaObject.connectSlotsByName(self)

    def setup_window(self):
        window_size = QSize(420, 700)

        self.setObjectName("window")
        self.resize(window_size)
        self.setMinimumSize(window_size)
        self.setMaximumSize(window_size)
        self.setWindowTitle(u"Voice Assistant")
        self.setAutoFillBackground(False)

    def setup_styles(self):
        file = QFile(":/styles/style.css")
        file.open(QFile.ReadOnly)

        byte_array = file.readAll()

        file.close()

        self.setStyleSheet(byte_array.data().decode())

    def setup_font(self):
        self.font = QFont()
        self.font.setFamily(u"Helvetica")
        self.font.setPointSize(18)

    def build_central_widget(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setSizePolicy(size_policy)

        self.setCentralWidget(self.central_widget)

    def build_vertical_layout(self):
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName(u"vertical_layout")

    def build_text_box(self):
        text_box_size = QSize(420, 600)

        self.text_box = QPlainTextEdit(self.central_widget)
        self.text_box.setObjectName(u"text_box")
        self.text_box.setMaximumSize(text_box_size)
        self.text_box.setFont(self.font)
        self.text_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.text_box.setUndoRedoEnabled(False)
        self.text_box.setReadOnly(True)
        self.text_box.setPlaceholderText("Waiting for your question...")

        self.vertical_layout.addWidget(self.text_box)

    def build_recognize_button(self):
        button_size = QSize(140, 40)

        self.recognize_button = QPushButton(self.central_widget)
        self.recognize_button.setObjectName(u"recognize_button")
        self.recognize_button.setEnabled(True)
        self.recognize_button.setMinimumSize(button_size)
        self.recognize_button.setMaximumSize(button_size)
        self.recognize_button.setFont(self.font)
        self.recognize_button.setAutoFillBackground(False)
        self.recognize_button.setText("Recognize")
        self.recognize_button.setShortcut("Return")

        self.vertical_layout.addWidget(self.recognize_button, 0, Qt.AlignHCenter)

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
        self.async_play_sound()
        self.recognize_button.setText("Listening...")

    def on_user_text(self, user_text: str):
        self.recognize_button.setText("Processing...")
        self.append_message(f"[You] {user_text}")

    def on_assistant_text(self, assistant_answer: str):
        signed_text = f"[{self.assistant.get_name()}] {assistant_answer}"
        self.append_message(signed_text)

    def append_message(self, message: str):
        self.text_box.appendPlainText(f"{message}\n")

    def start_recognition(self):
        coroutine = self.assistant.handle()
        asyncio.create_task(coroutine)

    @async_function
    def async_play_sound(self):
        file = QFile(":/sounds/click.mp3")
        file.open(QFile.ReadOnly)

        byte_array = file.readAll()

        file.close()

        with tempfile.NamedTemporaryFile("wb", delete=True) as temp:
            temp.write(byte_array.data())
            playsound(temp.name)

    def closeEvent(self, event: QCloseEvent):
        for task in asyncio.all_tasks():
            task.cancel()

        asyncio.get_running_loop().stop()

    async def start(self):
        self.show()
