# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject,
                            QSize, Qt)
from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import *


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
