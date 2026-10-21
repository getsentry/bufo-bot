# bufo-bot

Slack Bufo Bot (Hackweek 2024)

This project suggests Bufo emojis based on user input.

## How it works

The text you send via `/bufo` or by mentioning the bot is forwarded to an LLM
through [OpenRouter](https://openrouter.ai) to pick matching emoji names. The
model's reply is filtered against the static list in
`prompts/bufo_emoji_list.txt`, so only known Bufo emoji ever make it back into
Slack. Errors and performance data are reported to Sentry.

## Setup

1. Clone the repository
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenRouter API key, Slack API token, and signing secret:

   ```bash
   OPENROUTER_API_KEY=your_api_key_here
   SLACK_BOT_TOKEN=your_bot_token_here
   SLACK_SIGNING_SECRET=your_signing_secret_here
   ```

5. Run the app:

   ```bash
   python src/app.py
   ```
