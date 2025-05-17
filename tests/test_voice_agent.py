import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# Dummy modules for external dependencies
sys.modules['speech_recognition'] = types.ModuleType('speech_recognition')
sys.modules['openai'] = types.ModuleType('openai')
sys.modules['openai'].OpenAI = MagicMock
sys.modules['playsound'] = types.ModuleType('playsound')
sys.modules['playsound'].playsound = MagicMock()
sys.modules['requests'] = types.ModuleType('requests')
sys.modules['requests'].post = MagicMock()

from expense_manager.agents.voice_agent import VoiceAgent


class TestVoiceAgent(unittest.TestCase):
    @patch("expense_manager.agents.voice_agent.sr")
    @patch("expense_manager.agents.voice_agent.requests")
    @patch("expense_manager.agents.voice_agent.playsound")
    @patch("expense_manager.agents.voice_agent.OpenAI")
    def test_run_once(self, mock_openai_cls, mock_playsound, mock_requests, mock_sr):
        recognizer = MagicMock()
        recognizer.listen.return_value = MagicMock(get_wav_data=lambda: b"wav")
        mock_sr.Recognizer.return_value = recognizer
        mock_sr.Microphone.return_value.__enter__.return_value = MagicMock()

        openai_instance = MagicMock()
        openai_instance.audio.transcriptions.create.return_value = "hello"
        openai_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="hi"))]
        )
        openai_instance.audio.speech.create.return_value = MagicMock(stream_to_file=MagicMock())
        mock_openai_cls.return_value = openai_instance

        agent = VoiceAgent("key")
        with patch.object(agent, "listen", return_value="exit"):
            agent.run()
        mock_playsound.assert_not_called()


if __name__ == "__main__":
    unittest.main()
