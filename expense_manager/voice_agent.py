import os
import openai
import speech_recognition as sr
import pyttsx3


class VoiceAgent:
    """A voice-powered agent that transcribes user input and responds using GPT."""

    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""

    def respond(self, prompt: str) -> str:
        if not prompt:
            return ""
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message["content"].strip()
        print(f"Assistant: {answer}")
        self.tts_engine.say(answer)
        self.tts_engine.runAndWait()
        return answer

    def run(self):
        while True:
            prompt = self.listen()
            if prompt.lower() in {"exit", "quit", "stop"}:
                break
            self.respond(prompt)


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    agent = VoiceAgent(api_key)
    agent.run()


if __name__ == "__main__":
    main()
