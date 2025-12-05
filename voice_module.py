# voice_module.py
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

VOICE_MODEL_PATH = "models/vosk-model-small-en"

def voice_listener(callback=None):
    """
    Listens for voice commands using Vosk ASR.
    `callback` executes when a command is captured.
    """
    model = Model(VOICE_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        audio_queue.put(bytes(indata))

    print("🎤 Voice assistant active... Say something.")

    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                           dtype='int16', channels=1, callback=audio_callback):

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")

                if text and callback:
                    callback(text)

                print("You said:", text)
