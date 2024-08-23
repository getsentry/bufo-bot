from __future__ import annotations

import logging
import os
import random

import sentry_sdk
from dotenv import load_dotenv
from slack_bolt import App

from bufo_suggester import BufoSuggester

sentry_sdk.init(
    dsn="https://82cca006fe375b5ff101d7d5c6764c47@o4506792933130240.ingest.us.sentry.io/4507827653246976",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


logger = logging.getLogger(__name__)

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

    # Get response for the user input
    suggested_emojis = bufo_suggester.get_bufo_suggestions(user_input)
    validated_suggestions = bufo_suggester.validate_bufos_suggestions(suggested_emojis)
    response = bufo_suggester.build_bufo_suggestions_response(validated_suggestions)

    output_str = f"Bufos for `{user_input}`:\n{response}"

    respond(text=output_str)


@app.command("/bigbufo")
def big_bufo(ack, respond):
    ack()
    respond(text=random.choice(BIG_BUFOS))


@app.event("app_mention")
def handle_app_mention(say, event):
    user_input = event["text"].lower()

    if "random" in user_input:
        emoji = random.choice(bufo_suggester.emoji_list)
        say(f":{emoji}:")
    elif "bigbufo" in user_input:
        emoji = random.choice(BIG_BUFOS)
        say(f"{emoji}")
    elif "react" in user_input:
        # Check if the mention is in a thread
        if "thread_ts" in event:
            # Get the parent message
            parent_message = app.client.conversations_history(
                channel=event["channel"],
                latest=event["thread_ts"],
                limit=1,
                inclusive=True,
            )["messages"][0]

            suggested_emojis = bufo_suggester.get_bufo_suggestions(
                parent_message["text"]
            )
            validated_suggestions = bufo_suggester.validate_bufos_suggestions(
                suggested_emojis
            )
            validated_suggestions = random.sample(
                validated_suggestions, min(5, len(validated_suggestions))
            )

            # React to the parent message with the suggested bufos
            for emoji in validated_suggestions:
                try:
                    app.client.reactions_add(
                        channel=event["channel"],
                        timestamp=parent_message["ts"],
                        name=emoji,
                    )
                except Exception as e:
                    logger.error(f"Error adding reaction: {e}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
