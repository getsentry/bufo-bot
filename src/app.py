from __future__ import annotations

import os
import random
from dotenv import load_dotenv
from slack_bolt import App

from bufo_suggester import BufoSuggester

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

bufo_suggester = BufoSuggester()

THINKING_EMOJIS = [
    ":bufo-coin:",
    ":bufo-extra-cool:",
    ":bufo-gets-downloaded-from-the-cloud:",
    ":bufo-good-vibe:",
    ":bufo-assists-with-the-landing:",
    ":bufo-typing:",
    ":bufo-loading:",
    ":bufo-wards-off-the-evil-spirits:",
    ":bufo-matrix:",
    ":bufo-pushes-to-prod:",
    ":bufo-poof:",
    ":bufo-took-too-much:",
    ":bufo-riding-goose:"
]

@app.command("/bufo")
def bufo(ack, respond, command):
    ack()
    user_input = command['text']

    # Send an ephemeral thinking message
    app.client.chat_postEphemeral(
        channel=command['channel_id'],
        user=command['user_id'],
        text=f"Thinking... {random.choice(THINKING_EMOJIS)}",
    )

    # Get OpenAI response for the user input
    suggested_emojis = bufo_suggester.get_bufo_suggestions(user_input)
    validated_suggestions = bufo_suggester.validate_bufos_suggestions(suggested_emojis)

    output_str = f"Bufos for `{user_input}`:\n{validated_suggestions}"

    respond(text=output_str)

@app.event("app_mention")
def handle_app_mention(body, say, event):
    user_input = event['text']

    if "random" in user_input:
        emoji = random.choice(bufo_suggester.emoji_list)
        say(f":{emoji}:")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
