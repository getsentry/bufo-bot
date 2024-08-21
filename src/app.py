from __future__ import annotations

import os
import random

from bufo_suggester import BufoSuggester
from dotenv import load_dotenv
from slack_bolt import App

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
    ":bufo-riding-goose:",
]

BIG_BUFOS = [
    """
:bigbufo_0_0::bigbufo_1_0::bigbufo_2_0::bigbufo_3_0:
:bigbufo_0_1::bigbufo_1_1::bigbufo_2_1::bigbufo_3_1:
:bigbufo_0_2::bigbufo_1_2::bigbufo_2_2::bigbufo_3_2:
:bigbufo_0_3::bigbufo_1_3::bigbufo_2_3::bigbufo_3_3:
    """,
    """
:yay-bufo-1::yay-bufo-2:
:yay-bufo-3::yay-bufo-4:
    """,
]


@app.command("/bufo")
def bufo(ack, respond, command):
    ack()
    user_input = command["text"]

    # Send an ephemeral thinking message
    app.client.chat_postEphemeral(
        channel=command["channel_id"],
        user=command["user_id"],
        text=f"Thinking... {random.choice(THINKING_EMOJIS)}",
    )

    # Get OpenAI response for the user input
    suggested_emojis = bufo_suggester.get_bufo_suggestions(user_input)
    validated_suggestions = bufo_suggester.validate_bufos_suggestions(suggested_emojis)

    output_str = f"Bufos for `{user_input}`:\n{validated_suggestions}"

    respond(text=output_str)


@app.command("/bigbufo")
def big_bufo(ack, respond, command):
    ack()
    respond(text=random.choice(BIG_BUFOS))


@app.event("app_mention")
def handle_app_mention(body, say, event):
    user_input = event["text"].lower()

    if "random" in user_input:
        emoji = random.choice(bufo_suggester.emoji_list)
        say(f":{emoji}:")

    if "bigbufo" in user_input:
        emoji = random.choice(BIG_BUFOS)
        say(f"{emoji}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
