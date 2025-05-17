import argparse
import os

from expense_manager.voice_agent import VoiceAgent
from expense_manager.vapi_agent import VapiAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the expense voice agent")
    parser.add_argument(
        "--vapi", action="store_true", help="Use the Vapi-based voice agent"
    )
    args = parser.parse_args()

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    if args.vapi:
        vapi_key = os.environ.get("VAPI_API_KEY")
        if not vapi_key:
            raise ValueError("VAPI_API_KEY environment variable not set")
        agent = VapiAgent(openai_key, vapi_key)
    else:
        agent = VoiceAgent(openai_key)

    agent.run()


if __name__ == "__main__":
    main()
