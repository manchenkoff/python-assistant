import tempfile
from abc import abstractmethod, ABC
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

from gtts import gTTS
from playsound import playsound
from speech_recognition import AudioData, Microphone, Recognizer, UnknownValueError, RequestError, WaitTimeoutError

from src.lib.decorators import async_function


class SpeechInterface(ABC):
    @abstractmethod
    async def listen(self) -> Union[str, None]:
        raise NotImplementedError

    @abstractmethod
    async def say(self, message: str) -> None:
        raise NotImplementedError


class Speech(SpeechInterface):
    language: str
    recognizer: Recognizer
    recognizer_method: str
    recording_executor: ThreadPoolExecutor

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
    def _recognize_text_from_audio(self, audio: AudioData):
        func = getattr(self.recognizer, self.recognizer_method)

        try:
            return func(audio, language=self.language)
        except UnknownValueError:
            return "ERROR: Unknown value"
        except RequestError:
            return "ERROR: Request error"

    @async_function
    def _convert_text_to_speech(self, text: str):
        return gTTS(text, lang=self.language)

    @async_function
    def _play_concurrently(self, voice_audio):
        with tempfile.NamedTemporaryFile("wb", delete=True) as temp:
            voice_audio.save(temp.name)
            playsound(temp.name)

    async def listen(self) -> Union[str, None]:
        voice_audio = await self._get_audio_from_microphone()

        if not voice_audio:
            return None

        voice_text = await self._recognize_text_from_audio(voice_audio)

        return voice_text

    async def say(self, message: str) -> None:
        voice_audio = await self._convert_text_to_speech(message)
        await self._play_concurrently(voice_audio)
