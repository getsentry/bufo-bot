from bufo_suggester import BufoSuggester


def main():
    suggester = BufoSuggester()
    user_text = input("Enter your message: ")
    suggestions = suggester.get_bufo_suggestions(user_text)
    validated_suggestions = suggester.validate_bufos_suggestions(suggestions)
    response = suggester.build_bufo_suggestions_response(validated_suggestions)

    print(f"Suggested Bufo emojis: {response}")
