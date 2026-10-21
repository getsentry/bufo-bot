from __future__ import annotations

import logging
import os
import random

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk import set_user
from slack_bolt import App

from bufo_suggester import BufoSuggester

sentry_sdk.init(
    dsn="https://82cca006fe375b5ff101d7d5c6764c47@o4506792933130240.ingest.us.sentry.io/4507827653246976",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
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
    """
:bufo-blank-stare_0_0::bufo-blank-stare_1_0:
:bufo-blank-stare_0_1::bufo-blank-stare_1_1:
    """,
    """
:bufo-wider-01::bufo-wider-02::bufo-wider-03::bufo-wider-04:
    """,
]

# Custom responses for "{something} me" pattern
CUSTOM_RESPONSES = {
    "raj": [
        "can i bum a scroll :bufo-pleading:",
    ],
    "cathy": [
        "migratino :cocktail:",
    ],
    "christina": [
        ":bufo-pog-surprise: :bufo-pog-surprise: :bufo-pog-surprise: !! poggers !! :bufo-pog-surprise: :bufo-pog-surprise: :bufo-pog-surprise:",
    ],
    "mifu": [
        "i'm going to trap everyone in fire again :fire_elmo:",
    ],
}

HOME_TAB_VIEW = {
    "type": "home",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Welcome to BufoBot! 🐸",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "BufoBot is your friendly neighborhood Bufo emoji assistant. Here's what I can do for you:",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*1. Suggest Bufo Emojis* 🎭\nUse `/bufo [your text]` to get Bufo emoji suggestions related to your text.",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*2. Display Big Bufos* 🖼️\nType `/bigbufo` to summon a large Bufo emoji display.",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*3. Mention Me* 💬"},
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "• `@BufoBot random`: I'll respond with a random Bufo emoji.",
                }
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "• `@BufoBot bigbufo`: I'll show you a big Bufo composition.",
                }
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "• `@BufoBot react`: In a thread, I'll react to the parent message with relevant Bufos.",
                }
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "• `@BufoBot [any text]`: I'll suggest Bufo emojis related to your text.",
                }
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Let's make your Slack conversations more Bufo-tastic! 🐸✨",
            },
        },
    ],
}


def escape_mrkdwn(text: str) -> str:
    # Slack renders <!channel>, <!here> and <url|label> in bot messages even with
    # parse=none, so user text must be escaped before it is echoed back publicly.
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@app.event("app_home_opened")
def update_home_tab(event):
    try:
        # Call the views.publish method using the WebClient passed to the handler
        app.client.views_publish(
            user_id=event["user"],
            view=HOME_TAB_VIEW,
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.command("/bufohelp")
def bufo_help(ack, respond):
    ack()
    respond(
        text="Here's how you can use BufoBot:\n"
        "`/bufo [your text]`: Get Bufo emoji suggestions related to your text (only you can see it)\n"
        "`/bigbufo`: BIGBUFO (only you can see it)\n"
        "`@BufoBot random`: Get a random bufo\n"
        "`@BufoBot bigbufo [optional: excited, stare, wide]`: BIG BUFO\n"
        "`@BufoBot [any text]`: Bufobot will react with bufos"
    )


@app.command("/bufo")
def bufo(ack, respond, command):
    ack()
    set_user({"id": command["user_id"]})
    user_input = command["text"]

    # Send an ephemeral thinking message
    if not command["channel_id"].startswith("D"):
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
def handle_app_mention(say, event, context):
    set_user({"id": event["user"]})
    bot_user_id = context["bot_user_id"]

    # Remove the bot mention from the text
    full_text = event["text"]
    user_input = full_text.replace(f"<@{bot_user_id}>", "").strip().lower()

    if user_input == "random":
        emoji = random.choice(bufo_suggester.emoji_list)
        say(f":{emoji}:")
    elif user_input == "bigbufo":
        emoji = BIG_BUFOS[0]
        say(f"{emoji}")
    elif user_input == "bigbufo excited":
        emoji = BIG_BUFOS[1]
        say(f"{emoji}")
    elif user_input == "bigbufo stare":
        emoji = BIG_BUFOS[2]
        say(f"{emoji}")
    elif user_input == "bigbufo wide":
        emoji = BIG_BUFOS[3]
        say(f"{emoji}")
    # Check for "{something} me" pattern
    elif user_input.endswith(" me"):
        # Extract the action part (everything before " me")
        action = user_input[:-3].strip()
        if action in CUSTOM_RESPONSES:
            response = random.choice(CUSTOM_RESPONSES[action])
            say(response)
        else:
            # Fallback for unknown actions
            say(
                f"🐸 I don't know what {escape_mrkdwn(action)} means, "
                "but here's a bufo anyway! :bufo-good-vibe:"
            )
    # if mentioned with a message, react to the message with bufos
    else:
        suggested_emojis = bufo_suggester.get_bufo_suggestions(user_input)
        validated_suggestions = bufo_suggester.validate_bufos_suggestions(
            suggested_emojis
        )
        validated_suggestions = random.sample(
            validated_suggestions, min(5, len(validated_suggestions))
        )

        for emoji in validated_suggestions:
            try:
                app.client.reactions_add(
                    channel=event["channel"],
                    timestamp=event["ts"],
                    name=emoji,
                )
            except Exception as e:
                logger.error(f"Error adding reaction: {e}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
