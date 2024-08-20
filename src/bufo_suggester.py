import os
from wsgiref import validate

import anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_TYPE = "gpt-4o-mini"

PROMPT_DIR = "prompts"
PROMPT_FILE = "bufo_prompt.md"
EMOJI_LIST_FILE = "bufo_emoji_list.txt"


class BufoSuggester:
    def __init__(self, client_type: str | None = "openai"):
        if client_type == "openai":
            self.client_type = client_type
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        elif client_type == "anthropic":
            self.client_type = client_type
            self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        else:
            raise ValueError("Invalid client type")

        instructions = self._load_file(PROMPT_FILE)
        emojis = self._load_file(EMOJI_LIST_FILE)
        self.emoji_list = emojis.split()

        self.system_prompt = instructions + "\n\n" + emojis


    @staticmethod
    def _load_file(filename: str) -> str:
        file_path = os.path.join(PROMPT_DIR, filename)
        with open(file_path, 'r') as file:
            return file.read()

    def get_bufo_suggestions(self, user_input: str) -> str:
        if self.client_type == "openai":
            response = self.client.chat.completions.create(
                model=MODEL_TYPE,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content

        elif self.client_type == "anthropic":
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_input
                            }
                        ]
                    }
                ]
            )
            print(message.content)
            return message.content

        return ""

    def validate_bufos_suggestions(self, suggestions: str) -> str:
        emojis = suggestions.split()
        validated_emojis = [emoji for emoji in emojis if emoji in self.emoji_list]
        return "\n".join([f":{emoji}: `:{emoji}:`" for emoji in validated_emojis])


# This is a simple main function to test the BufoSuggester class
def main():
    suggester = BufoSuggester()
    user_text = input("Enter your message: ")
    suggestions = suggester.get_bufo_suggestions(user_text)
    validated_suggestions = suggester.validate_bufos_suggestions(suggestions)

    print(f"Suggested Bufo emojis: {validated_suggestions}")


if __name__ == "__main__":
    main()
