import asyncio
import tempfile

from playsound import playsound
from PySide2.QtCore import QCoreApplication, QFile, QMetaObject, QSize, Qt
from PySide2.QtGui import QCloseEvent, QFont
from PySide2.QtWidgets import QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from voice_assistant.assistant import AssistantInterface
from voice_assistant.decorators import async_function
from voice_assistant.resources import qInitResources


class Ui_window(object):
    def setupUi(self, window):
        if not window.objectName():
            window.setObjectName(u"window")
        window.resize(420, 700)
        window.setMinimumSize(QSize(420, 700))
        window.setMaximumSize(QSize(420, 720))
        window.setWindowTitle(u"Voice Assistant")
        window.setAutoFillBackground(False)
        window.setStyleSheet(u"background-color: #B0BEC5;")
        self.central_widget = QWidget(window)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text_box = QPlainTextEdit(self.central_widget)
        self.text_box.setObjectName(u"text_box")
        self.text_box.setMaximumSize(QSize(16777215, 600))
        font = QFont()
        font.setFamily(u"Helvetica")
        font.setPointSize(18)
        self.text_box.setFont(font)
        self.text_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.text_box.setStyleSheet(u"background-color: #ffffff;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 7px 6px;")
        self.text_box.setUndoRedoEnabled(False)
        self.text_box.setReadOnly(True)

        self.verticalLayout.addWidget(self.text_box)

        self.recognize_button = QPushButton(self.central_widget)
        self.recognize_button.setObjectName(u"recognize_button")
        self.recognize_button.setEnabled(True)
        self.recognize_button.setMinimumSize(QSize(140, 40))
        self.recognize_button.setMaximumSize(QSize(140, 40))
        self.recognize_button.setFont(font)
        self.recognize_button.setAutoFillBackground(False)
        self.recognize_button.setStyleSheet(u"QPushButton#recognize_button:disabled {\n"
                                            "	background-color: #cccccc;\n"
                                            "	border-radius: 10px;\n"
                                            "	color: #000000;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton#recognize_button {\n"
                                            "	background-color: #0077c2;\n"
                                            "	border-radius: 10px;\n"
                                            "	color: #eeeeee;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton#recognize_button:pressed {\n"
                                            "	background-color: #81C784;\n"
                                            "}")

        self.verticalLayout.addWidget(self.recognize_button, 0, Qt.AlignHCenter)

        window.setCentralWidget(self.central_widget)

        self.retranslateUi(window)

        QMetaObject.connectSlotsByName(window)

    # setupUi

    def retranslateUi(self, window):
        self.text_box.setPlaceholderText(QCoreApplication.translate("window",
                                                                    u"\u041e\u0436\u0438\u0434\u0430\u043d\u0438\u0435 \u043a\u043e\u043c\u0430\u043d\u0434...",
                                                                    None))
        self.recognize_button.setText(QCoreApplication.translate("window", u"Recognize", None))
        # if QT_CONFIG(shortcut)
        self.recognize_button.setShortcut(QCoreApplication.translate("window", u"Return", None))
        # endif // QT_CONFIG(shortcut)
        pass
    # retranslateUi


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
