from vosk import Model, KaldiRecognizer
import json
import pyaudio
import winsound

class MultilingualVosk:
    """
        Interface for managingVosk speech recognition models.
        Currently supported : English, German, Russian, French, Japanese

        Inputs:
        -------
        - initial_lang (str): Language code to initialize the recognizer (default: 'en').
        - self.stream: Audio captured from the microphone by PyAudio.

        Outputs:
        --------
        - yield text (str): Transcribed speech.
        - Language switching: Change language model by command.

        Methods:
        --------
        - load_model(lang): Loads the Vosk model for the specified language, lang - model language.
        - switch_language(lang): Switches the language model, lang - model language.
        - listen_continuous(): Continuoes stream listening and output until stopped.
        - get_language_code(lang_name): Return list of language models.
        - recognize_once(): Performs single-shot speech recognition and returns the transcription.
        - cleanup(): Releases audio resources.
    """
    def __init__(self, initial_lang='en'):
        self.models = {}
        self.supported_languages = ['en', 'de', 'ru', 'fr', 'ja']

        self.model_paths = {
            'en': "models/vosk-model-en-us-0.22",
            'de': "models/vosk-model-de-0.21",
            'ru': "models/vosk-model-ru-0.42",
            'fr': "models/vosk-model-fr-0.22",
            'ja': "models/vosk-model-ja-0.22"
        }

        self.current_lang = initial_lang
        self.load_model(initial_lang)
        self.rec = KaldiRecognizer(self.models[self.current_lang], 16000)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=512
        )
        self.stream.start_stream()

    def load_model(self, lang):
        if lang not in self.models:
            try:
                print(f"Loading {lang} model...")
                self.models[lang] = Model(self.model_paths[lang])
                print(f"{lang} model loaded successfully")
            except Exception as e:
                print(f"Error loading {lang} model: {e}")
                return False
        return True

    def switch_language(self, lang):
        if lang in self.supported_languages:
            if self.load_model(lang):
                self.current_lang = lang
                self.rec = KaldiRecognizer(self.models[lang], 16000)
                print(f"Switched to {lang}")
                return True
        print(f"Language {lang} not supported or failed to load")
        return False

    def listen_continuous(self):
        print(f"Listening in {self.current_lang}... (Ctrl+C to stop)")
        print("Say 'switch to [language]' to change language")

        winsound.Beep(440, 500)

        try:
            while True:
                data = self.stream.read(4000, exception_on_overflow=False)

                if len(data) == 0:
                    break

                if self.rec.AcceptWaveform(data):
                    print(self.rec.Result())

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.cleanup()

    def get_language_code(self, lang_name):
        lang_mapping = {
            'english': 'en',
            'german': 'de',
            'russian': 'ru',
            'french': 'fr',
            'japanese': 'ja'
        }
        return lang_mapping.get(lang_name.lower())

    def recognize_once(self):
        print(f"Listening for speech in {self.current_lang}...")

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get('text', '').strip()
                if text:
                    return text

    def cleanup(self):
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'p'):
            self.p.terminate()