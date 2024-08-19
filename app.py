from __future__ import annotations

import os

from slack_bolt import App

# Use the package we installed

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",
                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home tab_* :tada:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app.",
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Click me!"},
                            },
                        ],
                    },
                ],
            },
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.event("app_mention")
def respond(client, event, logger):
    print(client)
    print(event)
    print(logger)
    client.chat_postEphemeral(
        user=event["user"],
        channel=event["channel"],
        text="Hello!",
    )


# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


@app.command("/bufo")
def bufo(ack, respond, command):
    # Acknowledge command request
    ack()
    respond("Bufo bufo")


# Ready? Start your app!
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
