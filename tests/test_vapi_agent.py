import sys
import types
import unittest
from unittest.mock import patch, MagicMock

# Dummy modules for external dependencies
sys.modules.setdefault('openai', types.ModuleType('openai'))
sr_module = types.ModuleType('speech_recognition')
sr_module.Recognizer = MagicMock()
sr_module.Microphone = MagicMock()
sys.modules.setdefault('speech_recognition', sr_module)
requests_module = types.ModuleType('requests')
requests_module.post = lambda *args, **kwargs: None
sys.modules.setdefault('requests', requests_module)
sys.modules.setdefault('pyttsx3', types.ModuleType('pyttsx3'))

from expense_manager.vapi_agent import VapiAgent


class TestVapiAgent(unittest.TestCase):
    @patch('expense_manager.vapi_agent.requests.post')
    @patch('expense_manager.vapi_agent.openai')
    def test_run_once_exit(self, mock_openai, mock_post):
        agent = VapiAgent('ok', 'vk')
        with patch.object(agent, 'listen', return_value='exit'):
            with patch.object(agent, 'speak') as mock_speak:
                agent.run()
        mock_speak.assert_not_called()
        mock_post.assert_not_called()
        mock_openai.ChatCompletion.create.assert_not_called()


if __name__ == '__main__':
    unittest.main()
