COLOR_HEADER=\e[92m
COLOR=\e[93m
END=\033[0m
PROJECT_NAME := VoiceAssistant

.SILENT: help gui clean build

help:
	printf "$(COLOR_HEADER)$(PROJECT_NAME) management\n\n" && \
	printf "$(COLOR)make help$(END)\t Show this message\n" && \
	printf "$(COLOR)make gui$(END)\t Build GUI\n" && \
	printf "$(COLOR)make build$(END)\t Build application distributive directory\n"

gui:
	@pyside2-uic resources/forms/window.ui -o src/form.py
	@pyside2-rcc resources/resources.qrc -o src/resources.py

clean:
	@rm -Rf ./build ./dist ./resources/audio/temp/*

build: clean
	@pyinstaller main.spec