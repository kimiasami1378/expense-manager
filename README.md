# Expense Manager Voice Agent

This prototype demonstrates a basic voice-powered agent for documenting expenses. The agent listens to speech from the microphone, transcribes it, sends the text to OpenAI's API for a response and speaks the answer back to the user. The code uses `speech_recognition` for voice input and `pyttsx3` for text-to-speech.

## Requirements

- Python 3.8+
- The packages listed in `requirements.txt`
- An OpenAI API key exported as `OPENAI_API_KEY`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Agent

```bash
python main.py
```

Say "exit" to stop the program.

## Tests

Unit tests use mocks so they run without audio hardware or network access:

```bash
pytest -q
```
