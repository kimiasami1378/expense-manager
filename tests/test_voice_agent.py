import sys
import types
import unittest
from unittest.mock import patch, MagicMock

# Create dummy modules for external dependencies so the import works
sys.modules['openai'] = types.ModuleType('openai')
sys.modules['speech_recognition'] = types.ModuleType('speech_recognition')
sys.modules['pyttsx3'] = types.ModuleType('pyttsx3')

from expense_manager.voice_agent import VoiceAgent


class TestVoiceAgent(unittest.TestCase):
    @patch("expense_manager.voice_agent.sr")
    @patch("expense_manager.voice_agent.openai")
    @patch("expense_manager.voice_agent.pyttsx3")
    def test_run_once(self, mock_tts, mock_openai, mock_sr):
        recognizer = MagicMock()
        recognizer.listen.return_value = "audio"
        recognizer.recognize_google.return_value = "hello"
        mock_sr.Recognizer.return_value = recognizer
        microphone = MagicMock()
        mock_sr.Microphone.return_value.__enter__.return_value = microphone

        mock_openai.ChatCompletion.create.return_value = MagicMock(
            choices=[MagicMock(message={"content": "hi there"})]
        )
        engine = MagicMock()
        mock_tts.init.return_value = engine

        agent = VoiceAgent("key")
        with patch.object(agent, "listen", return_value="exit"):
            agent.run()
        engine.say.assert_not_called()


if __name__ == "__main__":
    unittest.main()
