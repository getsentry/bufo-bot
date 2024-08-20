# bufo-bot

Slack Bufo Bot (Hackweek 2024)

This project suggests Bufo emojis based on user input.

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

4. Create a `.env` file in the project root and add your OpenAI & Slack API token and signing secret:

   ```bash
   OPENAI_API_KEY=your_api_key_here
   SLACK_BOT_TOKEN=your_bot_token_here
   SLACK_SIGNING_SECRET=your_signing_secret_here
   ```
