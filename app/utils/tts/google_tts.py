from google.cloud import texttospeech


class Text2SpeachGoogleApiModel:
    def __init__(self):
        self.model = None
        self.voice_constant_kwargs = {
            "ssml_gender": texttospeech.SsmlVoiceGender.MALE,
            "language_code": "en-US",
            "name": "en-US-Neural2-A",
        }
        self.audio_constant_kwargs = {
            "audio_encoding": texttospeech.AudioEncoding.LINEAR16,
            "sample_rate_hertz": 16000,
            "speaking_rate": 0.95,
        }

    def load(self, **kwargs):
        self.model = texttospeech.TextToSpeechClient()

    def process(self, text: str, voice_kwargs: dict, audio_kwargs: dict):
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            {**self.voice_constant_kwargs, **voice_kwargs}
        )  # voice_kwargs overrides voice_constant_kwargs
        audio_config = texttospeech.AudioConfig(
            {**self.audio_constant_kwargs, **audio_kwargs}
        )  # audio_kwargs overrides audio_constant_kwargs
        response = self.model.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        return response.audio_content
