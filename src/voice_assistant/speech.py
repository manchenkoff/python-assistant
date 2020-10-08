import tempfile
from abc import ABC, abstractmethod
from typing import Optional

from gtts import gTTS
from playsound import playsound
from speech_recognition import AudioData, Microphone, Recognizer, RequestError, UnknownValueError, WaitTimeoutError

from voice_assistant.decorators import async_function


class SpeechInterface(ABC):
    @abstractmethod
    async def listen(self) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def say(self, message: str):
        raise NotImplementedError


class SpeechRecognitionError(Exception):
    pass


class Speech(SpeechInterface):
    language: str
    recognizer: Recognizer
    recognizer_method: str

    def __init__(self, language: str, method: str):
        self.recognizer = Recognizer()
        self.language = language
        self.recognizer_method = method

    @async_function
    def _get_audio_from_microphone(self):
        with Microphone() as source:
            try:
                return self.recognizer.listen(source, timeout=3.5)
            except WaitTimeoutError:
                return None

    @async_function
    def _convert_speech_to_text(self, audio: AudioData):
        func = getattr(self.recognizer, self.recognizer_method)

        try:
            return func(audio, language=self.language)
        except UnknownValueError:
            raise SpeechRecognitionError("Unknown value")
        except RequestError:
            raise SpeechRecognitionError("Request error")

    @async_function
    def _convert_text_to_speech(self, text: str):
        return gTTS(text, lang=self.language)

    @async_function
    def _play_concurrently(self, speech_data: gTTS):
        with tempfile.NamedTemporaryFile("wb", delete=True) as temp:
            speech_data.save(temp.name)
            playsound(temp.name)

    async def listen(self) -> Optional[str]:
        voice_audio = await self._get_audio_from_microphone()

        if not voice_audio:
            return None

        try:
            return await self._convert_speech_to_text(voice_audio)
        except SpeechRecognitionError:
            return None

    async def say(self, message: str):
        speech_data: gTTS = await self._convert_text_to_speech(message)
        await self._play_concurrently(speech_data)
