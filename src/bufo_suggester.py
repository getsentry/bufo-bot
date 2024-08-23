import os
import random

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_TYPE = "gpt-4o-mini"

PROMPT_DIR = "prompts"
PROMPT_FILE = "bufo_prompt.md"
EMOJI_LIST_FILE = "bufo_emoji_list.txt"


class BufoSuggester:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        instructions = self._load_file(PROMPT_FILE)
        emojis = self._load_file(EMOJI_LIST_FILE)
        self.emoji_list = emojis.split()

        self.system_prompt = instructions + "\n\n" + emojis

    @staticmethod
    def _load_file(filename: str) -> str:
        file_path = os.path.join(PROMPT_DIR, filename)
        with open(file_path, "r") as file:
            return file.read()

    def get_bufo_suggestions(self, user_input: str) -> str:
        response = self.client.chat.completions.create(
            model=MODEL_TYPE,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ],
        )
        return response.choices[0].message.content

    def validate_bufos_suggestions(self, suggestions: str) -> list[str]:
        emojis = suggestions.split()
        validated_emojis = [emoji for emoji in emojis if emoji in self.emoji_list]
        return random.sample(validated_emojis, min(5, len(validated_emojis)))

    def build_bufo_suggestions_response(self, validated_bufo_suggestions: str) -> str:
        return "\n".join(
            [f":{emoji}: `:{emoji}:`" for emoji in validated_bufo_suggestions]
        )


# This is a simple main function to test the BufoSuggester class
def main():
    suggester = BufoSuggester()
    user_text = input("Enter your message: ")
    suggestions = suggester.get_bufo_suggestions(user_text)
    validated_suggestions = suggester.validate_bufos_suggestions(suggestions)
    response = suggester.build_bufo_suggestions_response(validated_suggestions)

    print(f"Suggested Bufo emojis: {response}")


if __name__ == "__main__":
    main()
