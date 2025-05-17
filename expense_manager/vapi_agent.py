import os
import openai
import requests
import speech_recognition as sr


class VapiAgent:
    """Voice agent using Vapi for speech and OpenAI for chat."""

    TRANSCRIBE_URL = "https://api.vapi.ai/v1/transcribe"
    SPEAK_URL = "https://api.vapi.ai/v1/speak"

    def __init__(self, openai_api_key: str, vapi_api_key: str):
        openai.api_key = openai_api_key
        self.vapi_api_key = vapi_api_key
        self.recognizer = sr.Recognizer()

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.vapi_api_key}"}

    def listen(self) -> str:
        """Capture audio from the mic and transcribe using Vapi."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        audio_bytes = audio.get_wav_data()
        response = requests.post(
            self.TRANSCRIBE_URL, headers=self.headers, files={"file": ("speech.wav", audio_bytes)}
        )
        response.raise_for_status()
        text = response.json().get("text", "")
        print(f"User said: {text}")
        return text

    def speak(self, text: str) -> None:
        """Send text to Vapi for TTS playback."""
        response = requests.post(self.SPEAK_URL, headers=self.headers, json={"text": text})
        response.raise_for_status()

    def respond(self, prompt: str) -> str:
        if not prompt:
            return ""
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message["content"].strip()
        print(f"Assistant: {answer}")
        self.speak(answer)
        return answer

    def run(self) -> None:
        while True:
            prompt = self.listen()
            if prompt.lower() in {"exit", "quit", "stop"}:
                break
            self.respond(prompt)


def main() -> None:
    okey = os.environ.get("OPENAI_API_KEY")
    vkey = os.environ.get("VAPI_API_KEY")
    if not okey or not vkey:
        raise ValueError("OPENAI_API_KEY and VAPI_API_KEY must be set")
    agent = VapiAgent(okey, vkey)
    agent.run()


if __name__ == "__main__":
    main()
