# Expense Manager Voice Agent

This prototype demonstrates a voice-powered agent for documenting expenses. Two implementations are provided:

* **VoiceAgent** - uses local speech recognition and text-to-speech libraries.
* **VapiAgent** - uses [Vapi](https://vapi.ai) APIs for speech input and output.

Both agents send transcribed text to OpenAI and read the response aloud.

## Requirements

- Python 3.8+
- The packages listed in `requirements.txt`
- `OPENAI_API_KEY` exported in the environment
- If using Vapi, also export `VAPI_API_KEY`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Agent

By default the local `VoiceAgent` is used:

```bash
python main.py
```

To run the Vapi-backed agent:

```bash
python main.py --vapi
```

Say "exit" to stop the program.

## Tests

Unit tests use mocks so they run without audio hardware or network access:

```bash
python -m unittest discover -v tests
```
