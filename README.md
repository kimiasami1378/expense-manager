# Expense Manager Voice Agent

This prototype provides a voice-based assistant for managing expenses. Audio is
captured from the microphone, transcribed with OpenAI's latest models, processed
with GPT‑4o and spoken back to the user. If a `VAPI_API_KEY` is provided, the
agent will send responses to Vapi for text‑to‑speech, otherwise it falls back to
OpenAI's TTS service.

## Requirements

- Python 3.8+
- The packages listed in `requirements.txt`
- `OPENAI_API_KEY` exported in the environment
- Optional: `VAPI_API_KEY` for Vapi TTS

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
