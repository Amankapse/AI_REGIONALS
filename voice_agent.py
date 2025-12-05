import threading
import queue
import json
import sys
import time
import pyttsx3
from vosk import Model, KaldiRecognizer
import sounddevice as sd

class VoiceAgent:
    """
    Simple offline voice agent using Vosk + sounddevice.
    Listens continuously and emits keyword commands via a queue.
    """

    def __init__(self, vosk_model_path="models/vosk-model-small-en-us-0.15", samplerate=16000):
        self.model_path = vosk_model_path
        self.samplerate = samplerate
        self._q = queue.Queue()
        self._running = False
        self.engine = pyttsx3.init()
        self._model = None
        self._stream = None
        self._listener_thread = None

    def start(self):
        print("[voice] Loading VOSK model...")
        try:
            self._model = Model(self.model_path)
        except Exception as e:
            print(f"[voice] Failed to load VOSK model at {self.model_path}: {e}")
            raise

        self._running = True
        self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        print("[voice] Started voice listener.")

    def stop(self):
        self._running = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1.0)

    def speak(self, text):
        """ Blocking TTS """
        self.engine.say(text)
        self.engine.runAndWait()

    def _audio_callback(self, indata, frames, time_info, status):
        if not self._running: return
        self._stream_callback_buffer.put(bytes(indata))

    def _listen_loop(self):
        # Use a raw stream and feed to KaldiRecognizer manually
        rec = KaldiRecognizer(self._model, self.samplerate)
        rec.SetWords(False)

        # sounddevice RawInputStream yields raw bytes
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, dtype='int16',
                                   channels=1, callback=self._sounddevice_callback):
                while self._running:
                    try:
                        data = self._buffer.get(timeout=0.5)
                    except queue.Empty:
                        continue
                    if rec.AcceptWaveform(data):
                        res = rec.Result()
                        self._handle_result(res)
                    else:
                        # partial = rec.PartialResult()
                        pass
        except Exception as e:
            print("[voice] Audio stream error:", e)
            self._running = False

    # Implementation detail: sounddevice callback pumps into internal buffer
    def _sounddevice_callback(self, indata, frames, time_info, status):
        if status:
            print("[voice] sounddevice status:", status, file=sys.stderr)
        # indata is bytes-like when dtype int16
        self._buffer.put(bytes(indata))

    def _handle_result(self, res_json_str):
        try:
            j = json.loads(res_json_str)
            text = j.get("text", "").strip()
            if not text:
                return
            print("[voice] Recognized:", text)
            # simple keyword mapping
            if "save" in text or "capture" in text or "snapshot" in text:
                self._q.put(("save", text))
            elif "reject" in text or "fail" in text:
                self._q.put(("reject", text))
            elif "accept" in text or "ok" in text or "pass" in text:
                self._q.put(("accept", text))
            elif "repeat" in text or "say again" in text:
                self._q.put(("repeat", text))
            elif "stop" in text or "quit" in text:
                self._q.put(("stop", text))
            else:
                # generic utterances
                self._q.put(("other", text))
        except Exception as e:
            print("[voice] handle_result error:", e)

    def get_event(self, timeout=0.1):
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def run_in_background(self):
        """Alternative simple runner that doesn't use RawInputStream callback complexities."""
        # We'll implement a simpler blocking stream reader to keep the example portable
        self._buffer = queue.Queue()
        self._stream_thread = threading.Thread(target=self._blocking_stream_reader, daemon=True)
        self._stream_thread.start()
        self._listen_loop()  # this will block until stopped

    def _blocking_stream_reader(self):
        # open blocking stream and feed frames to buffer for recognizer
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000,
                                   dtype='int16', channels=1) as stream:
                while self._running:
                    data = stream.read(4000)[0]
                    self._buffer.put(bytes(data))
        except Exception as e:
            print("[voice] blocking reader error:", e)
            self._running = False
