from __future__ import annotations

import os

from dotenv import load_dotenv
from slack_bolt import App

from bufo_suggester import BufoSuggester

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

bufo_suggester = BufoSuggester()


@app.command("/bufo")
def bufo(ack, respond, command):
    ack()
    user_input = command['text']

    # Get OpenAI response for the user input
    suggested_emojis = bufo_suggester.get_bufo_suggestions(user_input)
    validated_suggestions = bufo_suggester.validate_bufos_suggestions(suggested_emojis)

    # Respond with the suggested emojis
    respond(f"Bufos for `{user_input}`:\n{validated_suggestions}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
