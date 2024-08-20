import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_TYPE = "gpt-4o-mini"

PROMPT_DIR = "prompts"
PROMPT_FILE = "bufo_prompt.md"
EMOJI_LIST_FILE = "bufo_emoji_list.md"

class BufoSuggester:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_prompt = self._load_file(PROMPT_FILE)
        self.emoji_list = self._load_file(EMOJI_LIST_FILE)

    @staticmethod
    def _load_file(filename: str) -> str:
        file_path = os.path.join(PROMPT_DIR, filename)
        with open(file_path, 'r') as file:
            return file.read()

    def get_bufo_suggestions(self, user_input: str) -> str:
        response = self.client.chat.completions.create(
            model=MODEL_TYPE,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": self.emoji_list},
                {"role": "user", "content": user_input}
            ]
        )
        print(response.choices[0].message.content)

        return response.choices[0].message.content


# This is a simple main function to test the BufoSuggester class
def main():
    suggester = BufoSuggester()
    user_text = input("Enter your message: ")
    suggestions = suggester.get_bufo_suggestions(user_text)
    print(f"Suggested Bufo emojis: {suggestions}")

if __name__ == "__main__":
    main()
