import os
import tempfile
import requests
import speech_recognition as sr
from playsound import playsound
from openai import OpenAI


class VoiceAgent:
    """Voice agent using OpenAI for transcription and chat, with optional Vapi TTS."""

    SYSTEM_PROMPT = (
        "You are an expense management assistant. "
        "Provide helpful responses that comply with standard financial policies "
        "and company expense rules."
    )

    def __init__(self, openai_api_key: str, vapi_api_key: str | None = None):
        self.openai = OpenAI(api_key=openai_api_key)
        self.recognizer = sr.Recognizer()
        self.vapi_api_key = vapi_api_key

    def _speak(self, text: str) -> None:
        if self.vapi_api_key:
            requests.post(
                "https://api.vapi.ai/v1/tts",
                headers={"Authorization": f"Bearer {self.vapi_api_key}"},
                json={"text": text},
                timeout=10,
            )
            return
        speech = self.openai.audio.speech.create(
            model="tts-1-hd",
            voice="alloy",
            input=text,
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            speech.stream_to_file(tmp.name)
            playsound(tmp.name)

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.get_wav_data())
            tmp.flush()
            transcription = self.openai.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=open(tmp.name, "rb"),
                response_format="text",
            )
        text = transcription
        print(f"User said: {text}")
        return text

    def respond(self, prompt: str) -> str:
        if not prompt:
            return ""
        completion = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        answer = completion.choices[0].message.content.strip()
        print(f"Assistant: {answer}")
        self._speak(answer)
        return answer

    def run(self) -> None:
        while True:
            prompt = self.listen().lower()
            if prompt in {"exit", "quit", "stop"}:
                break
            self.respond(prompt)


def main() -> None:
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    vapi_key = os.environ.get("VAPI_API_KEY")
    agent = VoiceAgent(openai_key, vapi_key)
    agent.run()


if __name__ == "__main__":
    main()
